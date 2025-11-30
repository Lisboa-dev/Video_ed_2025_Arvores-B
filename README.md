# 📘 B-Tree em Python --- Implementação Completa e Modularizada

Este repositório contém uma implementação educacional e totalmente
funcional de uma **Árvore B (B-Tree)** em Python, incluindo:

-   Inserção\
-   Busca\
-   Divisão de nós (split)\
-   Impressão estruturada\
-   Modularização em duas classes (`BTree` e `BTreeNode`)\
-   Exemplo completo de uso no arquivo `main.py`

A implementação segue as regras clássicas da Árvore B, ideal para
estudos de Estruturas de Dados, vídeos explicativos e projetos
acadêmicos.

## 📂 Estrutura do Projeto

    /
    ├── btree_node.py   # Implementa os nós da Árvore B
    ├── btree.py        # Implementa a Árvore B em si
    ├── main.py         # Exemplo de uso (executável)
    └── README.md       # Este arquivo

## 🧠 O que é uma Árvore B?

Uma **Árvore B** é uma árvore balanceada utilizada em sistemas de
arquivos, bancos de dados e estruturas de índice.\
Ela garante:

-   busca eficiente\
-   escrita e leitura em disco otimizadas\
-   balanceamento automático\
-   alta capacidade por nó

É uma evolução da Árvore Binária de Busca, mas permite **vários filhos
por nó**.

## 🧩 Funcionalidades da Implementação

### 🟦 `BTreeNode`

-   Armazena chaves e filhos\
-   Controla limites de chaves por nó\
-   Divide-se automaticamente quando cheio (`split_child`)\
-   Realiza a operação de inserção sem overflow (`insert_non_full`)

### 🟧 `BTree`

-   Gerencia a raiz\
-   Insere valores\
-   Divide a raiz quando necessário\
-   Permite busca\
-   Imprime a árvore em níveis

## ▶️ Como Executar

1.  Certifique-se de que os arquivos estão no mesmo diretório.
2.  Execute:

``` bash
python main.py
```

O programa irá:

-   Criar uma Árvore B de grau 3\
-   Inserir diversos valores\
-   Imprimir a árvore de forma hierárquica

## 📝 Exemplo de Uso (trecho de `main.py`)

``` python
from btree import BTree

def main():
    tree = BTree(t=3)  # Grau mínimo da Árvore B

    valores = [10, 20, 5, 6, 12, 30, 7, 17]

    for v in valores:
        tree.insert(v)

    print("Árvore B:")
    tree.print_tree()

if __name__ == "__main__":
    main()
```

## 🔎 Busca

``` python
resultado = tree.search(12)

if resultado:
    print("Valor encontrado!")
else:
    print("Valor não está na árvore.")
```

## 💡 Observações Importantes

-   O código foi mantido **didático**, priorizando clareza.\
-   A implementação suporta **qualquer tipo comparável** (int, float,
    str etc.).\
-   A API pode servir como base para:
    -   trabalhos acadêmicos\
    -   vídeos educativos\
    -   bootcamps sobre estruturas de dados\
    -   simulação de índices de banco de dados

## 🤝 Contribuindo

Sugestões, melhorias e implementações adicionais (remoção, merge de
árvores, visualização gráfica etc.) são bem-vindas!


