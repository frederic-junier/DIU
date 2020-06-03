""" Un module pour illustrer les principaux alogorithmes de jointure en Python
    On ne gèrera ici le cas nominal d'utilisation des fonctions où
    attr1 et attr2 sont LES INDEX EXISTANT des attributs
"""


from random import randrange
from timeit import timeit
from collections import defaultdict
# voir https://docs.python.org/3.6/library/collections.html#collections.defaultdict
# est utile pour le hash join en initialisant à la liste vide


def join_nested_loop(table1, attr1, table2, attr2):
    """L'algorithme naif de jointure par deux boucles imbriquées :
       pour chaque tuple de tabl1, on va lire toute la table2
       et produire un résultat à chaque fois que tup1[attr1] == tup2[attr2]
       https://en.wikipedia.org/wiki/Nested_loop_join

       CONTRAT: pas de préconditions sur les entrées"""

    pass


def join_hash(table1, attr1, table2, attr2):
    """L'algorithme de jointure en deux étapes :
          1. construction d'un index sur table1 via un dictionnaire :
             à chaque valeur de attr1, on associe **la liste** des index des
             tuples de table1 qui ont cette valeur
          2. scan de table2 :
             pour chaque tuple, on va chercher AVEC L'INDEX la liste
             des tuples de table1 qui on la valeur de attr2 pour attr1
             on ajoute les tuples au résultat (pas de besoin de vérifier
             les collisions car Python s'en charge pour nous avec le dictionnaire)

        https://en.wikipedia.org/wiki/Hash_join#Classic_hash_join

        CONTRAT: pas de préconditions sur les entrées

        Pour expliciter l'étape 1, sur le jeu d'essai des tests, on
        devrait obtenir le dictionnaire suivant qui dit qu'on peut
        trouver un tuple ayant valeur 'Jonah' à l'index 0 de la table1,
        'Alan' aux index 1 et 2, etc. soit :
            'Jonah': [0],
            'Alan': [1, 2],
            'Peppa': [3],
            'Glory': [4],
            'Popeye': [5, 6]

        Comme on utilise un defaultdict, pour toutes les autres
        clef le dictionnaire renverra []
        """


    # en fait, comme les dictionnaires Python utilisent des tables de hash
    # il suffit d'un dictionnaire qui sert d'index (un peu comme pour le
    # décorateur memoize) pour implémenter cet algorithme
    hash_table = defaultdict(list)
    pass



def join_merge(table1, attr1, table2, attr2):
    """L'algorithme de jointure sort-merge qui s'appuie sur des tables SUPPOSEES TRIEES
       https://en.wikipedia.org/wiki/Sort-merge_join
       Son principe est assez similaire à l'étape "merge" du merge sort
       https://en.wikipedia.org/wiki/Merge_sort

       On avance en // sur table1 et table2 avec 2 index ind1 et ind2
        - si table1[ind1][attr1] est avant table2[ind2][attr2]
          on incrémente ind1
        - si table2[ind2][attr2] est avant table1[ind1][attr1]
          on incrémente ind2
        - si les tuples sur lesquels on se trouve respectent la condition
                table1[ind1][attr1] == table2[ind2][attr2]
           alors avec une boucle locale, on va chercher tous les tuples
           de table2 satisfont la condition et ajouter au résultat.
           ensuite on incrémente ind1

       CONTRAT : le trie des entrées est à la charge des utilisateurs,
                 le comportement n'est pas garanti sinon"""

    pass

def benchmark(size_1=1000, nb_val_1=100,
              size_2=1000, nb_val_2=100,
              nb_repeat=100,
              bench_loop=True, bench_hash=True, bench_merge=True):
    """Compare les différentes implémentations"""


    sample_1 = [(i, randrange(nb_val_1)) for i in range(size_1)]
    sample_2 = [(randrange(nb_val_2), 'A'+str(j)) for j in range(size_2)]

    if bench_loop:
        time_loop = timeit(lambda: join_nested_loop(sample_1, 1, sample_2, 0), number=nb_repeat)
        print(f'Temps pour une exécution de join_nested_loop : {1000*time_loop/nb_repeat} ms')

    if bench_hash:
        time_hash = timeit(lambda: join_hash(sample_1, 1, sample_2, 0), number=nb_repeat)
        print(f'Temps pour une exécution de join_hash        : {1000*time_hash/nb_repeat} ms')

    if bench_merge:
        time_sort = timeit(lambda: sample_1.sort(key=lambda x: x[1]), number=nb_repeat)
        time_sort += timeit(lambda: sample_2.sort(key=lambda x: x[0]), number=nb_repeat)
        time_merge = timeit(lambda: join_merge(sample_1, 1, sample_2, 0), number=nb_repeat)
        print(f'Temps pour une exécution des tris            : {1000*time_sort/nb_repeat} ms')
        print(f'Temps pour une exécution de join_merge       : {1000*time_merge/nb_repeat} ms')
