# btree_node.py
from typing import List, Optional, TypeVar, Generic

T = TypeVar("T")

class BTreeNode(Generic[T]):
    def __init__(self, t: int, leaf: bool):
        self.t = t                 # grau mínimo
        self.leaf = leaf           # é folha?
        self.keys: List[Optional[T]] = [None] * (2 * t - 1)   # espaço para chaves
        self.children: List[Optional["BTreeNode[T]"]] = [None] * (2 * t)  # ponteiros para filhos
        self.n: int = 0            # número atual de chaves

    def traverse(self, out: List[T]) -> None:
        """Percorre in-order e adiciona chaves a out."""
        for i in range(self.n):
            if not self.leaf and self.children[i] is not None:
                self.children[i].traverse(out)
            out.append(self.keys[i])
        if not self.leaf and self.children[self.n] is not None:
            self.children[self.n].traverse(out)

    def search(self, k: T) -> Optional["BTreeNode[T]"]:
        """Retorna o nó que contém a chave k, ou None."""
        i = 0
        while i < self.n and self.keys[i] is not None and k > self.keys[i]:
            i += 1
        if i < self.n and self.keys[i] is not None and self.keys[i] == k:
            return self
        if self.leaf:
            return None
        child = self.children[i]
        if child is None:
            return None
        return child.search(k)

    def find_key(self, k: T) -> int:
        """Encontra o índice da primeira chave >= k."""
        idx = 0
        while idx < self.n and self.keys[idx] is not None and self.keys[idx] < k:
            idx += 1
        return idx

    # ---------- Inserção helpers ----------
    def insert_non_full(self, k: T) -> None:
        i = self.n - 1
        if self.leaf:
            # desloca chaves e insere
            while i >= 0 and self.keys[i] is not None and self.keys[i] > k:
                self.keys[i + 1] = self.keys[i]
                i -= 1
            self.keys[i + 1] = k
            self.n += 1
        else:
            # encontra filho onde inserir
            while i >= 0 and self.keys[i] is not None and self.keys[i] > k:
                i -= 1
            i += 1
            child = self.children[i]
            if child is None:
                # cria filho vazio (não devia ocorrer em árvore corretamente mantida)
                child = BTreeNode(self.t, True)
                self.children[i] = child
            if child.n == 2 * self.t - 1:
                self.split_child(i, child)
                if self.keys[i] is not None and self.keys[i] < k:
                    i += 1
            self.children[i].insert_non_full(k)

    def split_child(self, i: int, y: "BTreeNode[T]") -> None:
        """Divide y (que está cheio) em y e z, e insere z em children[i+1]."""
        t = self.t
        z = BTreeNode(t, y.leaf)
        z.n = t - 1
        # copia chaves finais de y para z
        for j in range(t - 1):
            z.keys[j] = y.keys[j + t]
            y.keys[j + t] = None
        # copia filhos se existirem
        if not y.leaf:
            for j in range(t):
                z.children[j] = y.children[j + t]
                y.children[j + t] = None
        y.n = t - 1
        # mover filhos do nó atual para abrir espaço
        for j in range(self.n, i, -1):
            self.children[j + 1] = self.children[j]
        self.children[i + 1] = z
        # mover chaves do nó atual
        for j in range(self.n - 1, i - 1, -1):
            self.keys[j + 1] = self.keys[j]
        # copiar chave do meio de y para este nó
        self.keys[i] = y.keys[t - 1]
        y.keys[t - 1] = None
        self.n += 1

    # ---------- Remoção helpers ----------
    def remove(self, k: T) -> None:
        idx = self.find_key(k)
        # caso 1: a chave está neste nó
        if idx < self.n and self.keys[idx] is not None and self.keys[idx] == k:
            if self.leaf:
                self.remove_from_leaf(idx)
            else:
                self.remove_from_non_leaf(idx)
        else:
            # caso 2: a chave não está neste nó
            if self.leaf:
                # chave não existe
                return
            # determina se a chave está no último filho
            flag = (idx == self.n)
            child = self.children[idx]
            if child is None:
                return
            if child.n < self.t:
                self.fill(idx)
            # após fill, pode ser que o layout tenha mudado
            if flag and idx > self.n:
                # o filho anterior agora contém a chave de interesse
                if self.children[idx - 1] is not None:
                    self.children[idx - 1].remove(k)
            else:
                if self.children[idx] is not None:
                    self.children[idx].remove(k)

    def remove_from_leaf(self, idx: int) -> None:
        # remove chave e desloca
        for i in range(idx + 1, self.n):
            self.keys[i - 1] = self.keys[i]
        self.keys[self.n - 1] = None
        self.n -= 1

    def remove_from_non_leaf(self, idx: int) -> None:
        k = self.keys[idx]
        # caso A: filho anterior (idx) tem >= t chaves -> predecessor
        if self.children[idx] is not None and self.children[idx].n >= self.t:
            pred = self.get_predecessor(idx)
            self.keys[idx] = pred
            self.children[idx].remove(pred)
        # caso B: filho seguinte tem >= t chaves -> successor
        elif self.children[idx + 1] is not None and self.children[idx + 1].n >= self.t:
            succ = self.get_successor(idx)
            self.keys[idx] = succ
            self.children[idx + 1].remove(succ)
        # caso C: ambos têm t-1 chaves -> merge
        else:
            self.merge(idx)
            if self.children[idx] is not None:
                self.children[idx].remove(k)

    def get_predecessor(self, idx: int) -> T:
        cur = self.children[idx]
        while cur is not None and not cur.leaf:
            cur = cur.children[cur.n]
        return cur.keys[cur.n - 1]  # type: ignore

    def get_successor(self, idx: int) -> T:
        cur = self.children[idx + 1]
        while cur is not None and not cur.leaf:
            cur = cur.children[0]
        return cur.keys[0]  # type: ignore

    def fill(self, idx: int) -> None:
        # tenta emprestar do irmão anterior
        if idx != 0 and self.children[idx - 1] is not None and self.children[idx - 1].n >= self.t:
            self.borrow_from_prev(idx)
        # tenta emprestar do irmão seguinte
        elif idx != self.n and self.children[idx + 1] is not None and self.children[idx + 1].n >= self.t:
            self.borrow_from_next(idx)
        else:
            # faz merge com um irmão
            if idx != self.n:
                self.merge(idx)
            else:
                self.merge(idx - 1)

    def borrow_from_prev(self, idx: int) -> None:
        child = self.children[idx]
        sibling = self.children[idx - 1]
        if child is None or sibling is None:
            return
        # desloca chaves de child para direita
        for i in range(child.n - 1, -1, -1):
            child.keys[i + 1] = child.keys[i]
        if not child.leaf:
            for i in range(child.n, -1, -1):
                child.children[i + 1] = child.children[i]
        # traz chave do pai para child
        child.keys[0] = self.keys[idx - 1]
        if not child.leaf:
            child.children[0] = sibling.children[sibling.n]
        # move chave do sibling para o pai
        self.keys[idx - 1] = sibling.keys[sibling.n - 1]
        sibling.keys[sibling.n - 1] = None
        child.n += 1
        sibling.n -= 1

    def borrow_from_next(self, idx: int) -> None:
        child = self.children[idx]
        sibling = self.children[idx + 1]
        if child is None or sibling is None:
            return
        # chave do pai vai para o fim de child
        child.keys[child.n] = self.keys[idx]
        if not child.leaf:
            child.children[child.n + 1] = sibling.children[0]
        # primeira chave de sibling sobe para o pai
        self.keys[idx] = sibling.keys[0]
        # shift left em sibling
        for i in range(1, sibling.n):
            sibling.keys[i - 1] = sibling.keys[i]
        if not sibling.leaf:
            for i in range(1, sibling.n + 1):
                sibling.children[i - 1] = sibling.children[i]
        sibling.keys[sibling.n - 1] = None
        sibling.children[sibling.n] = None
        child.n += 1
        sibling.n -= 1

    def merge(self, idx: int) -> None:
        child = self.children[idx]
        sibling = self.children[idx + 1]
        if child is None or sibling is None:
            return
        t = self.t
        # mover chave do pai para child
        child.keys[t - 1] = self.keys[idx]
        # copiar chaves de sibling para child
        for i in range(sibling.n):
            child.keys[i + t] = sibling.keys[i]
        # copiar filhos
        if not child.leaf:
            for i in range(sibling.n + 1):
                child.children[i + t] = sibling.children[i]
        # shift left nas chaves do pai
        for i in range(idx + 1, self.n):
            self.keys[i - 1] = self.keys[i]
        # shift left nos filhos do pai
        for i in range(idx + 2, self.n + 1):
            self.children[i - 1] = self.children[i]
        child.n += sibling.n + 1
        self.keys[self.n - 1] = None
        self.children[self.n] = None
        self.n -= 1
