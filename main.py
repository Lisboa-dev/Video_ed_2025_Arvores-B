# main.py
from btree import BTree

def main():
    # grau mínimo t = 3 (cada nó pode ter até 5 chaves)
    tree = BTree(3)

    vals = [10, 20, 5, 6, 12, 30, 7, 17, 3, 4, 25, 27, 26]
    for v in vals:
        tree.insert1(v)

    print("Travessia (in-order):", tree.traverse())
    print("\nEstrutura:")
    tree.pretty_print()

    print("\nRemovendo 6, 13, 7, 4:")
    tree.remove(6)
    tree.remove(13)  # não existe
    tree.remove(7)
    tree.remove(4)

    print("Travessia depois de remoções:", tree.traverse())
    print("\nEstrutura depois de remoções:")
    tree.pretty_print()

    print("\nBuscas:")
    print("Contém 12?", tree.contains(12))
    print("Contém 99?", tree.contains(99))

if __name__ == "__main__":
    main()
