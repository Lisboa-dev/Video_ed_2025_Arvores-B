README — Árvore B (implementações em Java e Python)

Projeto com implementações didáticas de uma Árvore B (operações completas: busca, inserção com split, remoção com borrow/merge, travessia). Vem com versão em Java (modularizada) e em Python (modularizada). Foco educativo — bom para estudos, experimentos e adaptação.

📁 Estrutura do repositório
/project-root
├─ java/
│  ├─ BTreeNode.java
│  ├─ BTree.java
│  └─ Main.java
│
├─ python/
│  ├─ btree_node.py
│  ├─ btree.py
│  └─ main.py
│
└─ README.md   <-- este arquivo


Observação: se você consolidou tudo em um único arquivo Python/Java, ajuste os comandos de execução conforme indicado abaixo.

🧾 Descrição rápida

O que é: Uma estrutura de dados balanceada ideal para índices e armazenamento em disco.

Operações implementadas: search/contains, insert (com split), remove (com borrow e merge), traverse (in-order), e funções auxiliares de debug (prettyPrint / pretty_print).

Grau mínimo t: controle a capacidade dos nós. Exemplos usam t = 3.

💻 Requisitos
Java

JDK 11+ recomendado.

Para compilar/executar (linha de comando):

# dentro da pasta java/
javac *.java
java Main

Python

Python 3.8+ (tipagem usada, mas código roda sem checagem estática).

Recomendado usar venv.

# criar e ativar venv (Unix)
python3 -m venv .venv
source .venv/bin/activate

# Windows PowerShell
python -m venv .venv
.venv\Scripts\Activate.ps1


Executar o exemplo:

# dentro da pasta python/
python main.py

🚀 Uso (exemplos)
Java

Main.java contém um exemplo que insere valores, imprime travessia, remove chaves e imprime a estrutura.

Python

main.py executa uma sequência semelhante (inserções, travessia, remoções e buscas).

Para usar em código próprio:

from btree import BTree
tree = BTree
tree.insert(10)
tree.insert(5)
print(tree.traverse())

🐞 Troubleshooting (erro comum)

Erro reportado pelo usuário:

TypeError: BTree.insert() missing 1 required positional argument: 'k'


Causas prováveis e como diagnosticar:

Import errado / conflito de nomes

Verifique se não há múltiplos arquivos com o mesmo nome (btree.py, BTree.py, btree (copy).py, etc.) no PYTHONPATH ou no diretório.

Cheque __pycache__ e reinicie a execução.

Método sobrescrito acidentalmente

Confirme que a assinatura em btree.py é def insert(self, k: T) -> None: (em Python) ou public void insert(T k) (Java).

Diagnóstico rápido em tempo de execução (Python)
Cole no REPL ou no seu main.py antes de usar:

import btree
print(btree.BTree.insert.__code__.co_argcount)     # deve mostrar 2
print(btree.BTree.insert.__code__.co_varnames)     # deve incluir ('self', 'k')


Se o co_argcount e co_varnames não mostrarem ('self','k'), significa que a função insert carregada não é a que você espera.

Exemplo de re-setup simples

Delete __pycache__, feche/abra o editor, e execute python main.py novamente.

Se o problema persistir, rode a versão monolítica (tudo em um arquivo) para isolar imports.

⚙️ Notas de implementação & limitações

Python: usa listas com None para espaço fixo nos nós (similar a arrays estáticos). Tipagem via TypeVar é para auxílio estático apenas — não afeta runtime.

Genéricos / T vs int: não causam conflito com int. Você pode instanciar BTree[int] sem problemas. Type hints não alteram o comportamento em tempo de execução.

Uso em produção: este código é didático. Para produção considere:

persistência/serialização (nós em disco),

gerenciamento de memória eficiente,

concorrência/locks,

cobertura com testes unitários.

✅ Tests & sugestões

Adicionar testes (pytest / JUnit):

Python: crie tests/test_btree.py com cenários de inserção/remoção/busca/ordenação.

Java: use JUnit para testar operações em diferentes ordens t.

Validações adicionáveis:

checar invariantes após cada inserção/remoção (ex.: cada nó tem t-1 a 2*t-1 chaves, folhas no mesmo nível).

🔁 Alternativa para evitar conflitos (Python)

Se estiver enfrentando conflito de import, gere um único arquivo single_btree.py contendo BTreeNode, BTree e main — isso evita problemas com imports e __pycache__.

📚 Referências e leitura

Capítulos sobre B-Trees em livros de estruturas de dados (ex.: Introduction to Algorithms — Cormen et al.).

Documentação/implementações de B+ usadas em bancos de dados (para entender variações).

🧾 Licença

Sinta-se livre para usar, estudar e modificar o código. Se for publicar, mencione a fonte / autor original conforme desejar.

✍️ Créditos

Implementações fornecidas como exemplo didático por este assistente (base conceitual: algoritmos clássicos de B-Tree).
