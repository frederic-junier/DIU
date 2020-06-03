DIU bloc 4 : "Bases de données : création de schémas et normalisation" : TP sur les algorithmes de jointure
====================================================

Dans ce TP, on va s'intéresser **aux algorithmes de jointures**, c'est-à-dire aux algorithmes exécutés par les moteurs des SGBDs quand ils traduisent des requêtes comme la suivante :

```sql
SELECT *
FROM table1 JOIN table2 ON table1.attr1 == table2.attr2
```

Il existe plusieurs algorithmes de jointure et l'optimiseur de requêtes du SGBD va tâcher de choisir le _meilleur_, vis-à-vis de statistiques sur les données et surtout des **index** disponibles sur les tables.
Le but du TP est ainsi de comprendre ces algorithmes fondamentaux et de les comparer entre eux puis de les comparer face à deux de SQLite 3.

**Remarque** la comparaison de performance (_benchmark_) est un exercice complexe car de nombreux paramètres très différents contribuent à la performance finale (matériel, OS, I/O disques ou d'affichage, efficacité de la compilation/interprétation du langage de programmation, caches, temps d'initialisation etc.).

Implanter les algorithmes classiques de jointure en Python
-----------------------------------------------------------

Le fichier [`join_algorithms.py`](join_algorithms.py) contient le squelette à remplir pour les trois algorithmes, à savoir _nested loop_, _hash join_ et _merge join_. Ces algorithmes font la même chose et ont la même signature `def algo(table1, attr1, table2, attr2):` :

* `table1` et `table2` sont des listes (Python) de tuples (Python). Il n'y a pas de garanties d'ordre sur ces listes;
* `attr1` (resp. `attr2`) est _l'indice_ (entier) de l'attribut de `table1` (resp. de `tablee`) sur lequel on fait la jointure;
* ces algorithmes retournent tous une liste de tuples, comme l'aurait fait la requête SQL.


Le fichier [`join_algorithms_test.py`](join_algorithms_test.py) donne un exemple d'entrées et de résultats attendus.

**EXERCICE** : compléter la fonction `join_nested_loop` et tester votre implantation avec `pytest-3` et les tests fournis.

**EXERCICE** : compléter la fonction `join_hash` et tester votre implantation avec `pytest-3` et les tests fournis.

**EXERCICE (POUR ALLER PLUS LOIN)** : compléter la fonction `join_merge` et tester votre implantations avec `pytest-3` et les tests fournis. Vous n'êtes pas obligé de faire cet exercice pour passer à la suite.


Comparer algorithmes implantés en Python
----------------------------------------

On peut maintenant comparer la performance des algorithmes avec la fonction fournie `benchmark`.Pour la fonction `join_merge` on compte séparément le temps pris pour le tris des tables.
En effet, cette étape peut-être _amortie_ car elle est utile pour d'autre opérations que la jointure, comme les clauses `ORDER BY` ou `GROUP BY`.

**EXERCICE** : comprendre ce que fait la fonction `benchmark` (vous pouvez ajouter des commentaires par exempl)e avant de l'exécuter. 

Avec les paramètres par défaut de `benchmark`, on obtient les résultats suivants sur une machine portable (Dual Core Intel i7-5600U CPU @ 2.60GHz, 8GB RAM).

```
Temps pour une exécution de join_nested_loop : 47.21451419973164 ms
Temps pour une exécution de join_hash        : 0.8530486993549857 ms
Temps pour une exécution des tris            : 0.3733556004590355 ms
Temps pour une exécution de join_merge       : 0.49316930017084815 ms
```

**EXERCICE (POUR ALLER PLUS LOIN)** : jouer avec les paramètres pour trouver un cas qui soit défavorable à `join_hash` mais favorable à `join_merge`. Sans tenir compte du temps de tri, on peut trouver des cas avec un facteur 10x en faveur de `join_merge`. _Indice_ : remarquez que les rôles de `table1` et `table2` sont asymétriques faire en sorte de passer du temps dans l'étape de construction d'index de `join_hash`.

**EXERCICE (POUR ALLER PLUS LOIN)** : même question que précédement, mais cette fois si il faut trouver un cas qui est favorable à `join_nested_loop` et dévaforable aux deux autres. _Indice_ faites en sorte que la jointure soit aussi grosse que le produit cartésien.

Comparer l'exécution dans Python à celle native dans SQLite
-------------------------------------------------------------

Maintenant, on va comparer la performance de ces implantations Python face aux algorithmes jointures de SQLite (qui est écrit en C). Pour cela on va comparer les deux approches suivantes :

* **Approche A : jointure en SQLite**, on exécute la requête `SELECT * FROM table1 JOIN table2 ON table1.val == table2.val` puis (depuis Python) on récupère l'intégralité du résultat, c'est la fonction `join_sqlite()`
* **Approche B : jointure en Python**, on exécute la requête `SELECT * FROM table1` et on stocke son résultat dans un tableau, de même pour `SELECT * FROM table2` puis on utilise un des algorithmes précedents pour faire le calcul de jointure et enfin on renvoie le résultat, c'est la fonction `join_python()`


**EXERCICE** : créer une nouvelle base de données nommée `join_algorithms_versus_sqlite3.db` et exécuter le script SQL `join_algorithms_schema.sql` pour créer le schéma *et* peupler la base avec un jeu de données similaire à celui du benchmark de l'exercice précédent.

**EXERCICE** :  avec la fonction `join_algorithms_versus_sqlite3()` du programme [`join_algorithms_versus_sqlite3.py`](join_algorithms_versus_sqlite3.py) comparer les temps d'exécution des deux méthodes.

Sur ma machine, j'obtiens cet ordre de grandeur :

```
INFO:root:Temps de transfert et de jointure côté Python  : 36.440872ms
INFO:root:Temps de transfert et de jointure côté Sqlite3 : 108.951388ms
```

 **EXERCICE** : reprendre la comparaison mais cette fois avec la requête `SELECT COUNT(*) FROM table1 JOIN table2 ON table1.val == table2.val`. Ici, `join_python()` renverra _la longueur du tableau_ avec  `len(join_hash(table1, 1, table2, 0))` pour l'algorithme de jointure par hash. Une différence _importante doit les séparer_  : comment l'expliquer ?

Sur ma machine, j'obtiens cet ordre de grandeur :

```
INFO:root:Temps de transfert et de jointure côté Python : 36.784499ms
INFO:root:Temps de transfert et de jointure côté Sqlite3 : 6.756878ms
```

 **EXERCICE (FACULTATIF ET OUVERT)** : conclure en formulant quelques bonnes pratiques de l'accès à une base de données via un programme (Python).
