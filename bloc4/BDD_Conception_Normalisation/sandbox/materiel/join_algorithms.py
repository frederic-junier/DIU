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
    return [t1 + t2 for t1 in table1 for t2 in table2 if t1[attr1] == t2[attr2]]


def join_hash2(table1, attr1, table2, attr2):
    """L'algorithme de jointure en deux étapes :
          1. construction d'un index sur table1 via un dictionnaire :
             à chaque valeur de attr1, on associe **la liste** des index des
             tuples de table1 qui ont cette valeur
          2. scan de table2 :
             pour chaque tuple, on va chercher AVEC L'INDEX la liste
             des tuples de table1 qui on la valeur de attr2 pour attr1
             On fait attention aux collisions de hash et on ajoute les
             tuples au résultat.

        https://en.wikipedia.org/wiki/Hash_join#Classic_hash_join

        CONTRAT: pas de préconditions sur les entrées"""
    res = []
    index = dict()
    for k, t1 in enumerate(table1):
        val = t1[attr1]
        #pour gérer les collisions de hash
        #on stocke dans index[val] une liste de listes dont le premier élément est t1[attr1]
        #et dont les éléments suivants sont les index des tuples de table1 qui ont même
        #même valeur val pour l'attribut d'index attr1
        if val in index:
            for l in  index[val]:
                if l[0] == val:
                    l.append(k)
                    break
        else:
            index[val] = [[val, k]]
    for t2 in table2:
        val = t2[attr2]
        if val in index:
            for l in index[val]:
                if l[0] == val:
                    for k in l[1:]:
                        res.append(table1[k] + t2)
    return res

def join_hash(table1, attr1, table2, attr2):
    """L'algorithme de jointure en deux étapes :
          1. construction d'un index sur table1 via un dictionnaire :
             à chaque valeur de attr1, on associe **la liste** des index des
             tuples de table1 qui ont cette valeur
          2. scan de table2 :
             pour chaque tuple, on va chercher AVEC L'INDEX la liste
             des tuples de table1 qui on la valeur de attr2 pour attr1
             On fait attention aux collisions de hash et on ajoute les
             tuples au résultat.

        https://en.wikipedia.org/wiki/Hash_join#Classic_hash_join

        CONTRAT: pas de préconditions sur les entrées"""
    # en fait, comme les dictionnaires Python utilisent des tables de hash
    # il suffit d'un dictionnaire qui sert d'index (un peu comme pour le
    # décorateur memoize) pour implémenter cet algorithme
    #hash_table = defaultdict(list)
    #pass
    res = []
    index = dict()
    for k, t1 in enumerate(table1):
        val = t1[attr1]
        #pour gérer les collisions de hash
        #on stocke dans index[val] une liste de listes dont le premier élément est t1[attr1]
        #et dont les éléments suivants sont les index des tuples de table1 qui ont même
        #même valeur val pour l'attribut d'index attr1
        if val in index:
            index[val].append(k)
        else:
            index[val] = [k]
    for t2 in table2:
        val = t2[attr2]
        if val in index:
            for k in index[val]:
                res.append(table1[k] + t2)
    return res




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

    res = []
    n1 = len(table1)
    n2 = len(table2)
    ind1 = ind2 = 0
    while ind1 < n1 and ind2 < n2:
        t1, t2 = table1[ind1], table2[ind2]
        if t1[attr1] < t2[attr2]:
            ind1 += 1
        elif t1[attr1] > t2[attr2]:
            ind2 += 1
        else:
            ind3 = ind2
            while ind3 < n2 and table2[ind3][attr2] == t1[attr1]:
                res.append(t1 + table2[ind3])
                ind3 += 1
            ind1 += 1
    return res

"""
fjunier@fjunier:~/Git/DIU-Junier/bloc4/BDD_Conception_Normalisation/sandbox$ pytest-3 -v
============================= test session starts ==============================
platform linux -- Python 3.6.9, pytest-3.3.2, py-1.5.2, pluggy-0.6.0 -- /usr/bin/python3
cachedir: .cache
rootdir: /home/fjunier/Git/DIU-Junier/bloc4/BDD_Conception_Normalisation/sandbox, inifile:
plugins: Faker-4.1.0
collected 3 items

join_algorithms_test.py::test_join_nested_loop PASSED                    [ 33%]
join_algorithms_test.py::test_join_hash PASSED                           [ 66%]
join_algorithms_test.py::test_join_merge PASSED                          [100%]

=========================== 3 passed in 0.07 seconds ===========================
"""




def benchmark(size_1=1000, nb_val_1=100,
              size_2=1000, nb_val_2=100,
              nb_repeat=100,
              bench_loop=True, bench_hash=True, bench_merge=True):
    """Compare les différentes implémentations"""


    sample_1 = [(i, randrange(nb_val_1)) for i in range(size_1)]
    sample_2 = [(randrange(nb_val_2), 'A'+str(j)) for j in range(size_2)]

    if bench_loop:
        time_loop = timeit(lambda: join_nested_loop(sample_1, 1, sample_2, 0), number=nb_repeat)
        print('Temps pour une exécution de join_nested_loop : ' + str(time_loop))

    if bench_hash:
        time_hash = timeit(lambda: join_hash(sample_1, 1, sample_2, 0), number=nb_repeat)
        print('Temps pour une exécution de join_hash        : ' + str(time_hash))

    if bench_merge:
        time_sort = timeit(lambda: sample_1.sort(key=lambda x: x[1]), number=nb_repeat)
        time_sort += timeit(lambda: sample_2.sort(key=lambda x: x[0]), number=nb_repeat)
        time_merge = timeit(lambda: join_merge(sample_1, 1, sample_2, 0), number=nb_repeat)
        print('Temps pour une exécution des tris            : ' + str(time_sort))
        print('Temps pour une exécution de join_merge       : ' + str(time_merge))

"""
Test avec join_hash première version
In [2]: benchmark()
Temps pour une exécution de join_nested_loop : 6.241203233000078
Temps pour une exécution de join_hash        : 0.16518595900015498
Temps pour une exécution des tris            : 0.020488148000140427
Temps pour une exécution de join_merge       : 0.3143313499999749
"""

"""
Test avec join_hash seconde version
In [4]: benchmark()
Temps pour une exécution de join_nested_loop : 6.2457434129999
Temps pour une exécution de join_hash        : 0.162923426000134
Temps pour une exécution des tris            : 0.02036094400023103
Temps pour une exécution de join_merge       : 0.2916302970002107
"""
