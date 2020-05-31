
# coding: utf-8

# DIU bloc 4 : "Bases de données : création de schémas et normalisation" : TP sur les algorithmes de jointure
# ====================================================
# 
# Dans ce TP, on va s'intéresser **aux algorithmes de jointures**, c'est-à-dire aux algorithmes exécutés par les moteurs des SGBDs quand ils traduisent des requêtes comme la suivante :
# 
# ```sql
# SELECT *
# FROM table1 JOIN table2 ON table1.attr1 == table2.attr2
# ```
# 
# Il existe plusieurs algorithmes de jointure et l'optimiseur de requêtes du SGBD va tâcher de choisir le _meilleur_, vis-à-vis de statistiques sur les données et surtout des **index** disponibles sur les tables.
# Le but du TP est ainsi de comprendre ces algorithmes fondamentaux et de les comparer entre eux puis de les comparer face à deux de SQLite 3.
# 
# **Remarque** la comparaison de performance (_benchmark_) est un exercice complexe car de nombreux paramètres très différents contribuent à la performance finale (matériel, OS, I/O disques ou d'affichage, efficacité de la compilation/interprétation du langage de programmation, caches, temps d'initialisation etc.).
# 
# Implanter les algorithmes classiques de jointure en Python
# -----------------------------------------------------------
# 
# Le fichier [`join_algorithms.py`](join_algorithms.py) contient le squelette à remplir pour les trois algorithmes, à savoir _nested loop_, _hash join_ et _merge join_. Ces algorithmes font la même chose et ont la même signature `def algo(table1, attr1, table2, attr2):` :
# 
# * `table1` et `table2` sont des listes (Python) de tuples (Python). Il n'y a pas de garanties d'ordre sur ces listes;
# * `attr1` (resp. `attr2`) est _l'indice_ (entier) de l'attribut de `table1` (resp. de `tablee`) sur lequel on fait la jointure;
# * ces algorithmes retournent tous une liste de tuples, comme l'aurait fait la requête SQL.
# 
# 
# Le fichier [`join_algorithms_test.py`](join_algorithms_test.py) donne un exemple d'entrées et de résultats attendus.
# 
# **EXERCICE** : compléter la fonction `join_nested_loop` et tester votre implantation avec `pytest-3` et les tests fournis.
# 
# **EXERCICE** : compléter la fonction `join_hash` et tester votre implantation avec `pytest-3` et les tests fournis.
# 
# **EXERCICE (POUR ALLER PLUS LOIN)** : compléter la fonction `join_merge` et tester votre implantations avec `pytest-3` et les tests fournis. Vous n'êtes pas obligé de faire cet exercice pour passer à la suite.
# 
# 
# 

# In[53]:


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


# ```
# fjunier@fjunier:~/Git/DIU-Junier/bloc4/BDD_Conception_Normalisation/sandbox$ pytest-3 -v
# ============================= test session starts ==============================
# platform linux -- Python 3.6.9, pytest-3.3.2, py-1.5.2, pluggy-0.6.0 -- /usr/bin/python3
# cachedir: .cache
# rootdir: /home/fjunier/Git/DIU-Junier/bloc4/BDD_Conception_Normalisation/sandbox, inifile:
# plugins: Faker-4.1.0
# collected 3 items
# 
# join_algorithms_test.py::test_join_nested_loop PASSED                    [ 33%]
# join_algorithms_test.py::test_join_hash PASSED                           [ 66%]
# join_algorithms_test.py::test_join_merge PASSED                          [100%]
# 
# =========================== 3 passed in 0.07 seconds ===========================
# ```

# 
# Comparer algorithmes implantés en Python
# ----------------------------------------
# 
# On peut maintenant comparer la performance des algorithmes avec la fonction fournie `benchmark`.Pour la fonction `join_merge` on compte séparément le temps pris pour le tris des tables.
# En effet, cette étape peut-être _amortie_ car elle est utile pour d'autre opérations que la jointure, comme les clauses `ORDER BY` ou `GROUP BY`.
# 
# **EXERCICE** : comprendre ce que fait la fonction `benchmark` (vous pouvez ajouter des commentaires par exempl)e avant de l'exécuter. 
# 
# Avec les paramètres par défaut de `benchmark`, on obtient les résultats suivants sur une machine portable (Dual Core Intel i7-5600U CPU @ 2.60GHz, 8GB RAM).
# 
# ```
# Temps pour une exécution de join_nested_loop : 4.8441446340002585
# Temps pour une exécution de join_hash        : 0.1884105869976338
# Temps pour une exécution des tris            : 0.018489982991013676
# Temps pour une exécution de join_merge       : 0.3174076739960583
# ```
# 
# **EXERCICE (POUR ALLER PLUS LOIN)** : jouer avec les paramètres pour trouver un cas qui soit défavorable à `join_hash` mais favorable à `join_merge`. Sans tenir compte du temps de tri, on peut trouver des cas avec un facteur 10x en faveur de `join_merge`. _Indice_ : remarquez que les rôles de `table1` et `table2` sont asymétriques faire en sorte de passer du temps dans l'étape de construction d'index de `join_hash`.
# 

# In[54]:


def benchmark(size_1=1000, nb_val_1=100,
              size_2=1000, nb_val_2=100,
              nb_repeat=100,
              bench_loop=True, bench_hash=True, bench_merge=True):
    """Compare les différentes implémentations"""

    #échantillon 1  
    sample_1 = [(i, randrange(nb_val_1)) for i in range(size_1)]
    #échantillon 2
    sample_2 = [(randrange(nb_val_2), 'A'+str(j)) for j in range(size_2)]

    if bench_loop:
        #temps d'exécution moyen sur nb_repeat tours de boucles 
        #pour l'exécution de la jointure avec join_nested_loop
        #sur la correspondance des attibuts d'index 1 de sample_1 et 0 de sample_2 
        #le domaine de sample_1[0] est  randrange(nb_val_1)
        #le domaine de sample_2[0] est  randrange(nb_val_2)
        time_loop = timeit(lambda: join_nested_loop(sample_1, 1, sample_2, 0), number=nb_repeat)
        print('Temps pour une exécution de join_nested_loop : ' + str(time_loop))

    if bench_hash:
        #temps d'exécution moyen sur nb_repeat tours de boucles 
        #pour l'exécution de la jointure avec join_hash
        time_hash = timeit(lambda: join_hash(sample_1, 1, sample_2, 0), number=nb_repeat)
        print('Temps pour une exécution de join_hash        : ' + str(time_hash))

    if bench_merge:
        #temps d'exécution du tri de sample_1
        time_sort = timeit(lambda: sample_1.sort(key=lambda x: x[1]), number=nb_repeat)
        #temps d'exécution du tri de sample_2
        time_sort += timeit(lambda: sample_2.sort(key=lambda x: x[0]), number=nb_repeat)
        #temps d'exécution moyen sur nb_repeat tours de boucles 
        #pour l'exécution de la jointure avec join_merge
        time_merge = timeit(lambda: join_merge(sample_1, 1, sample_2, 0), number=nb_repeat)
        print('Temps pour une exécution des tris            : ' + str(time_sort))
        print('Temps pour une exécution de join_merge       : ' + str(time_merge))


# In[55]:


benchmark()


# ```
# Test avec join_hash première version
# In [2]: benchmark()
# Temps pour une exécution de join_nested_loop : 6.241203233000078
# Temps pour une exécution de join_hash        : 0.16518595900015498
# Temps pour une exécution des tris            : 0.020488148000140427
# Temps pour une exécution de join_merge       : 0.3143313499999749
# ```
# 
# ```
# Test avec join_hash seconde version
# In [4]: benchmark()
# Temps pour une exécution de join_nested_loop : 6.2457434129999
# Temps pour une exécution de join_hash        : 0.162923426000134
# Temps pour une exécution des tris            : 0.02036094400023103
# Temps pour une exécution de join_merge       : 0.2916302970002107
# ```

# ## Analyse de complexité 
# 
# Soit `m` le nombre de lignes dans la jointure. Ce nombre est majoré par `max(nb_val_1, nb_val_2)`
# 
# * Complexité de `join_nested_loop` : `O(size_1 * size_2)`
# * Complexité de `join_hash` :  `O(size_1 * n + size_2 * n)` (majoration grossière) où `n` est le nombre maximal de tuple de l'échantillon `sample_1` qui ont la même valeur sur l'attribut 1 (longueur maximale d'une liste d'indexs stockée dans l'index/table de hash) : la valeur de `n` est d'autant plus grande que le domaine de `sample_1[1]` de taille `nb_val_1` est grand. On peut donc prendre comme majorant `O(size_1 * nb_val_1 + size_2 * nb_val_1)` 
# * Complexité de `join_merge` (sans compter le tri des tables) :  `O(size_1 + size_2 + size_2 * m)` où `m` est le nombre de lignes dans la jointure.
# 
# 
# Si `size_1 == size_2` et `nb_val_1 == nb_val_2`, comme les valeurs sont choisies selon une loi uniforme dans `[0;nb_val_1]`,   les complexités de `join_hash` et `join_merge` doivent avoir  des majorants du même ordre de grandeur, qui vont différer par une constante. On remarque que `join_hash` est plus rapide : les tests d'égalité sont remplacés par des calculs de `hash` dans la phase de construction de l'index puis dans la phase de scan de `sample_2`.
# 
# Si on augmente la taille de `nb_val_1`, on augmente la valeur  de `n`  le nombre maximal de tuple de l'échantillon `sample_1` qui ont la même valeur sur l'attribut 1 et la complexité de `join_hash` 

# In[56]:


for size_2 in [10**k for k in range(2, 5)]:    
    for nb_val_2 in [10**k for k in range(2, 4)]:
        for size_1 in [10**k for k in range(2, 5)]: 
            for nb_val_1 in [10**k for k in range(2, 7)]:
                print(f"size_1 = {size_1}, nb_val_1={nb_val_1}, size_2 = {size_2},  nb_val_2={nb_val_2}")
                benchmark(bench_loop=False, size_1 = size_1, nb_val_1 =nb_val_1  ,size_2 = size_2, nb_val_2 = nb_val_2, nb_repeat = 10)
                print('-'* 10)


# On observe que `join_merge` est beaucoup plus rapide lorsque `size_1` est beaucoup plus grand que `size_2` et d'autant plus que `nb_val_1` est grand (et donc la longueur maximale d'une liste stockée dans l'index/table de hash).

# Comparer l'exécution dans Python à celle native dans SQLite
# -------------------------------------------------------------
# 
# Maintenant, on va comparer la performance de ces implantations Python face aux algorithmes jointures de SQLite (qui est écrit en C). Pour cela on va comparer les deux approches suivantes :
# 
# * **Approche A : jointure en SQLite**, on exécute la requête `SELECT * FROM table1 JOIN table2 ON table1.val == table2.val` puis (depuis Python) on récupère l'intégralité du résultat, c'est la fonction `join_python()`
# * **Approche B : jointure en Python**, on exécute la requête `SELECT * FROM table1` et on stocke son résultat dans un tableau, de même pour `SELECT * FROM table2` puis on utilise un des algorithmes précedents pour faire le calcul de jointure et enfin on renvoie le résultat, c'est la fonction `join_sqlite()`
# 
# 
# **EXERCICE** : créer une nouvelle base de données nommée `join_algorithms_versus_sqlite3.db` et exécuter le script SQL `join_algorithms_schema.sql` pour créer le schéma *et* peupler la base avec un jeu de données similaire à celui du benchmark de l'exercice précédent.
# 
# **EXERCICE** : en vous inspirant du code fourni, compléter les fonctions `join_python()` et `join_sqlite()` du programme [`join_algorithms_versus_sqlite3.py`](join_algorithms_versus_sqlite3.py) et observer les temps d'exécution.
# 
#  **EXERCICE** : ensuite, exécuter la requête de jointure directement dans `SQLite3` en activant activant le chronométrage avec `.timer on` depuis l'interpréteur ligne de commande ou depuis _DB Browser for SQLite_ (le temps est affiché en bas de la fenêtre d'exécution). Vous devriez avoir une différence _de plusieurs ordre de magnitude entre les deux_ : comment l'expliquer ?
# 
#  **EXERCICE** : reprendre la comparaison mais cette fois avec la requête `SELECT COUNT(*) FROM table1 JOIN table2 ON table1.val == table2.val`. Ici, `join_python()` renverra _la longueur du tableau_, comme par exemple `len(join_hash(table1, 1, table2, 0))` pour l'algorithme de jointure par hash. Comparer les temps d'exécution, une différence _de plusieurs ordre de magnitude doit les séparer_  : comment l'expliquer ?
# 
# 

# In[57]:


get_ipython().magic('reload_ext sql')
get_ipython().magic('config SqlMagic.displaycon = False')
get_ipython().magic('config SqlMagic.autolimit = 100')


# In[58]:


get_ipython().magic('sql sqlite:///join_algorithms_versus_sqlite3.db')


# In[59]:


get_ipython().run_cell_magic('sql', '', '\nPRAGMA foreign_keys=1;')


# In[60]:


get_ipython().run_cell_magic('sql', '', "\n-- POUR CHARGER DANS SQLite3 : \n-- sqlite3 join_algorithms_versus_sqlite3.db\n-- .timer on\n-- .read join_algorithms_schema.sql\n\ndrop table if exists Table1;\ndrop table if exists Table2;\n\n-- Un schéma très simple, qui reprend le benchmark des 3 algos en Python qu'on rappelle ici :\n--\n-- def benchmark(size_1=1000, nb_val_1=100,\n--               size_2=1000, nb_val_2=100,\n--               nb_repeat=100,\n--               bench_loop=True, bench_hash=True, bench_merge=True):\n--\n--    sample_1 = [(i, randrange(nb_val_1)) for i in range(size_1)]\n--    sample_2 = [(randrange(nb_val_2), 'A'+str(j)) for j in range(size_2)]\n\n-- Activation des clefs étrangères\nPRAGMA foreign_keys=1; \n\ncreate table Table1(\n    idA INTEGER PRIMARY KEY,    -- un ID entier\n    val INTEGER     -- l'attribut de jointure\n);\n\ncreate table Table2(\n    val INTEGER,  -- pas  REFERENCES Table1(val), mais ca ne changerait rien\n    idB INTEGER\n);\n\n\n -- On va remplir les tables avec 10.000 lignes pour A et autant pour B\n\n--pour générer récursivement tous les entiers entre 1 et 10000\n--voir https://sqlpro.developpez.com/cours/sqlserver/cte-recursives/\nWITH RECURSIVE data_1(val) AS (\n  SELECT 1\n  UNION ALL\n  SELECT val+1\n  FROM data_1\n  WHERE val+1 <= 10000\n) \nINSERT INTO Table1 \n  SELECT  val,\n          ABS(RANDOM() % 1000)   --entiers aléatoires entre 0 et 1000\n  FROM data_1;\n\nWITH RECURSIVE data_2(val) AS (\n  SELECT 1\n  UNION ALL\n  SELECT val+1\n  FROM data_2\n  WHERE val+1 <= 10000\n) \nINSERT INTO Table2\n  SELECT  ABS(RANDOM() % 1000),\n          'A' || val\n  FROM data_2;")


# In[61]:


""" Un module pour comparer la performance des jointures 'à la main'
    en Python face à ceux en C bien choisis de SQLite3"""

import sqlite3
import logging
#voir https://docs.python.org/3/howto/logging.html
from timeit import timeit
#from join_algorithms import join_nested_loop, join_hash, join_merge

logging.basicConfig(level=logging.INFO)

DB_FILE = 'join_algorithms_versus_sqlite3.db'

def join_algorithms_versus_sqlite3():
    """Fonction de comparaison"""
    try:
        connection = sqlite3.connect(DB_FILE)

        # Pour avoir des ditcionnaires et non des tuples dans le résultat
        # see https://docs.python.org/3.6/library/sqlite3.html#sqlite3.Row
        # connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        logging.debug("You are connected to - %s", DB_FILE)
        cursor.execute("SELECT sqlite_version() as version;")
        record = cursor.fetchone()
        logging.debug(tuple(record))

        def join_python(jointure):
            cursor.execute("SELECT * FROM table1;")
            table1 = cursor.fetchall()
            #print(table1[:10])
            cursor.execute("SELECT * FROM table2;")
            table2 = cursor.fetchall()
            jointure(table1, 1,table2, 0)
            
        def join_sqlite():
            cursor.execute("SELECT * FROM table1 JOIN table2 ON table1.val == table2.val;")
            record = cursor.fetchone()
            
        for jointure in [join_hash, join_merge]:
            time_join_python = timeit(lambda : join_python(jointure), number=100)
            logging.info(f'Temps pour une jointure {jointure.__name__} côté Python : %f', time_join_python)

        time_join_sqlite = timeit(join_sqlite, number=100)
        logging.info('Temps pour une jointure côté Sqlite3 : %f', time_join_sqlite)

    except (sqlite3.Error) as error:
        logging.error("Error while connecting to sqlite3: %s", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            logging.debug("Sqlite3 connection is closed")


# In[62]:


join_algorithms_versus_sqlite3()


#  **EXERCICE** : ensuite, exécuter la requête de jointure directement dans `SQLite3` en activant activant le chronométrage avec `.timer on` depuis l'interpréteur ligne de commande ou depuis _DB Browser for SQLite_ (le temps est affiché en bas de la fenêtre d'exécution). Vous devriez avoir une différence _de plusieurs ordre de magnitude entre les deux_ : comment l'expliquer ?
#  
# * sqlite3 CLI :
# 
# ![sqlite3-CLI](time_sqlite3.png)
# 
# * sqlite DBBrowser :
# 
# ![sqlite DBBrowser](time_dbbrowser.png)

# **EXERCICE** : reprendre la comparaison mais cette fois avec la requête `SELECT COUNT(*) FROM table1 JOIN table2 ON table1.val == table2.val`. Ici, `join_python()` renverra _la longueur du tableau_, comme par exemple `len(join_hash(table1, 1, table2, 0))` pour l'algorithme de jointure par hash. Comparer les temps d'exécution, une différence _de plusieurs ordre de magnitude doit les séparer_  : comment l'expliquer ?
# 
# 

# In[70]:


def join_algorithms_versus_sqlite3_V2():
    """Fonction de comparaison"""
    try:
        connection = sqlite3.connect(DB_FILE)

        # Pour avoir des ditcionnaires et non des tuples dans le résultat
        # see https://docs.python.org/3.6/library/sqlite3.html#sqlite3.Row
        # connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        logging.debug("You are connected to - %s", DB_FILE)
        cursor.execute("SELECT sqlite_version() as version;")
        record = cursor.fetchone()
        logging.debug(tuple(record))

        def join_python(jointure):
            cursor.execute("SELECT * FROM table1;")
            table1 = cursor.fetchall()
            #print(table1[:10])
            cursor.execute("SELECT * FROM table2;")
            table2 = cursor.fetchall()           
            return len( jointure(table1, 1,table2, 0))
            
        def join_sqlite():
            cursor.execute("SELECT COUNT(*) FROM table1 JOIN table2 ON table1.val == table2.val;")
            record = cursor.fetchone()
            return record
        
                
        for jointure in [join_hash, join_merge]:
            time_join_python = timeit(lambda : join_python(jointure), number=100)
            logging.info(f'Temps pour une jointure {jointure.__name__} côté Python : %f', time_join_python)
            
        time_join_sqlite = timeit(join_sqlite, number=100)
        logging.info('Temps pour une jointure côté Sqlite3 : %f', time_join_sqlite)

        

    except (sqlite3.Error) as error:
        logging.error("Error while connecting to sqlite3: %s", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            logging.debug("Sqlite3 connection is closed")


# In[71]:


join_algorithms_versus_sqlite3_V2()


# Dans ce cas, on a un facteur 100 entre l'exécution en ligne de commandes et l'exécution à travers un programme Python. La requête `SELECT COUNT(*) FROM table1 JOIN table2 ON table1.val == table2.val;` est plus lente que  `SELECT * FROM table1 JOIN table2 ON table1.val == table2.val;` depuis un programme Python si on l'exécute dans `sqlite3` d'abord et similaire si on fait la jointure après avec nos fonctions maisons. On observe au contraire que la  requête  `SELECT COUNT(*) FROM table1 JOIN table2 ON table1.val == table2.val;`  s'exécute plus rapidement en ligne de commande.
# 
# 
# * sqlite3 CLI :
# 
# ![sqlite3-CLI](timer2_sqlite3.png)
# 
# * sqlite DBBrowser :
# 
# ![sqlite DBBrowser](timer2_sqliteDBBrowser.png)

# __EXERCICE (FACULTATIF ET OUVERT) :__
# 
# Conclure en formulant quelques bonnes pratiques de l'accès à une base de données via un programme (Python).
# 
# 
# * Bonne pratique 1 : Faire les opérations SQL (jointures) dans SQLite et non dans Python
# * Bonne pratique 2 : se méfier des tests en ligne de commandes qui peuvent donner de mauvaises indications de performances (voir exercice précédent avec les requêtes `SELECT * FROM table1 JOIN table2 ON table1.val == table2.val;` et `SELECT COUNT(*) FROM table1 JOIN table2 ON table1.val == table2.val;`
