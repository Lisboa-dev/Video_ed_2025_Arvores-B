from typing import List, Optional, TypeVar, Generic

from btree_node import BTreeNode, T

class BTree(Generic[T]):
    def __init__(self, t: int):
        """
        Inicializa uma B-Tree com grau mínimo t.
        t: grau mínimo (cada nó terá no máximo 2*t - 1 chaves).
        """
        if t < 2:
            # validação básica: t precisa ser >= 2 para a B-Tree fazer sentido
            raise ValueError("Grau mínimo t deve ser pelo menos 2.")
        self.t = t
        # raiz inicialmente vazia (nenhum nó criado)
        self.root: Optional[BTreeNode[T]] = None

    def traverse(self) -> List[T]:
        """
        Retorna uma lista com a travessia em ordem (in-order) da árvore.
        Monta a lista delegando a operação ao nó raiz.
        """
        out: List[T] = []
        if self.root is not None:
            # delega a travessia para o nó raiz; ele preenche 'out'
            self.root.traverse(out)
        return out

    def contains(self, k: T) -> bool:
        """
        Verifica se a chave k existe na árvore.
        Retorna True se encontrada, False caso contrário.
        """
        if self.root is None:
            # árvore vazia -> não contém nada
            return False
        # root.search retorna o nó onde a chave foi encontrada (ou None)
        return self.root.search(k) is not None

    def insert1(self, k: T) -> None:
        """
        Insere a chave k na árvore.
        Observação: nome do método é 'insert1' (talvez queira renomear para 'insert').
        """
        if self.root is None:
            # caso simples: árvore vazia -> criamos a raiz como folha contendo k
            self.root = BTreeNode(self.t, True)
            self.root.keys[0] = k
            self.root.n = 1
            return

        r = self.root
        # se a raiz está cheia (tem 2*t - 1 chaves), precisamos dividi-la
        if r.n == 2 * self.t - 1:
            # cria um novo nó s que será a nova raiz (não-folha)
            s = BTreeNode(self.t, False)
            s.children[0] = r  # antiga raiz vira filho 0 de s
            # divide o filho r (cheio) colocando a chave mediana em s
            s.split_child(0, r)
            # escolher qual filho de s irá receber a nova chave k
            i = 0
            # se a primeira chave de s for menor que k, vamos para o filho 1
            if s.keys[0] is not None and s.keys[0] < k:
                i = 1
            # insere no filho apropriado (que agora com certeza não está cheio)
            s.children[i].insert_non_full(k)
            # atualiza a raiz para s
            self.root = s
        else:
            # raiz não está cheia -> inserir normalmente a partir da raiz
            r.insert_non_full(k)

    def remove(self, k: T) -> None:
        """
        Remove a chave k da árvore, se existir.
        Delegação para o nó raiz; depois ajusta a raiz caso ela fique vazia.
        """
        if self.root is None:
            # árvore vazia -> nada a fazer
            return
        # pede à raiz para remover k (lógica complexa fica em BTreeNode.remove)
        self.root.remove(k)
        # se após a remoção a raiz ficou sem chaves...
        if self.root.n == 0:
            # se raiz for folha, árvore vira vazia (root = None)
            if self.root.leaf:
                self.root = None
            else:
                # caso contrário, promove o único filho como nova raiz
                self.root = self.root.children[0]

    def pretty_print(self) -> None:
        """
        Imprime a árvore por níveis (debug / visualização).
        Função interna recursiva _pp faz o trabalho.
        """
        def _pp(node: Optional[BTreeNode[T]], level: int) -> None:
            if node is None:
                return
            # imprime o nível e as chaves válidas do nó
            print(f"Level {level}: ", [node.keys[i] for i in range(node.n)])
            # se não for folha, desce pelos filhos
            if not node.leaf:
                for i in range(node.n + 1):
                    _pp(node.children[i], level + 1)
        # chama o recursivo a partir da raiz, nível 0
        _pp(self.root, 0)
