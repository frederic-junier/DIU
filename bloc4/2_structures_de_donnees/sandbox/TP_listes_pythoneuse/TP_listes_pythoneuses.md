Une implémentation "pythoniste" des listes doublement chaînées
================================================================

Dans ce TP, on va reprendre l'implémentation des listes doublement chainées dans une version plus "pythoniste" qui reprend les conventions et le fonctionnement des collections et objets Python de la bibliothèque standard.



**Exercice** : compléter le fichier [`linked_list.py`](linked_list.py) et tester l'implémentation avec les tests  `pytest` fournis dans [`linked_list_test.py`](linked_list_test.py).

Le reste du document est une explication du fonctionnement de la classe. Les tests comportent des exemples qui faciliteront la compréhension


**Remarque additionnelle** 

> En effet ce type d'implémentation est très homogène avec les collections standard. Je compléterai en vous incitant à réfléchir sur ce que vous feriez en classe, en fonction des compétences que vous voulez cibler. Pour ce type d'implémentation "pythoneuse", il ne faut pas oublier qu'une certaine maîtrise ou recul des élèves sera nécessaire sur : les classes et l'héritage, les interfaces et classes abstraites, le principe de surcharge, les itérateurs, le type Collection (et Reversible) etc. Beaucoup de ces choses ne sont pas au programme de NSI (même Term). La classe Liste du TP de base n'a pas besoin de tout ça (juste du principe de classe) et est donc d'un autre degré d’accessibilité pour un élève. Dépendamment de ce que vous voulez leur faire faire et le placement dans l'année par rapport au reste du programme, vous pouvez inclure plus ou moins de notions "pythonesques" dans vos propres classes.

Opérations supportées
---------------------

Plus concrètement, on veut faire en sorte que cette implémentation des listes chainées supporte les opérations suivantes, chacune correspondant à une méthode 'magique' qui est utilisée par l'interpréteur Python.

### Constructeur

Le constructeur peut prendre un objet itérable en paramètre pour initialiser la liste avec les éléments du paramètre, voir la la méthode `__init__` :

```python
a_list = DoublyLinkedList([0, 1, 2])
a_list = DoublyLinkedList((0, 1, 2))
```

### Longueur

On peut utiliser la fonction `len` (et convertir la liste en booléen), voir la méthode `__len__`, l'implémentation par défaut de `__bool__` étant de tester si `__len__` retourne 0 :

```python
len(a_list) # renvoie la longueur de la liste
if a_list:  # teste si la liste est vide
    ....
```

### Appartenance

On peut utiliser le test `in` pour savoir si un élément est dans la liste, Voir la méthode `__contains__`.

```python
0 in DoublyLinkedList([0, 1, 2]) # renvoie True
3 in DoublyLinkedList([0, 1, 2]) # renvoie False
3 not in DoublyLinkedList([0, 1, 2]) # renvoie True
```

### Protocole d'itération

C'est le plus important, la classe doit fournir **un itérateur**  sur ses éléments. Ce _design pattern_ est utilisé en Python par toutes   les collections standards et simplifie l'écriture des programme, voir la méthode `__iter__` :

```python
a_list = DoublyLinkedList([0, 1, 2])

a_table = list(a_list)
for item in a_list:
  print(item) # affiche 0, puis 1, puis 2

a_new_list = [x*x for x in a_list] # l'équivalent de `map` pour votre structure
```

### Itération à l'envers

Comme la liste est doublement chainée, on fournira aussi un itérateur qui parcoure la liste à l'envers, voir la méthode `__reversed__`

```python
for item in reversed(a_list):
  print(itm) # affiche 0, puis 1, puis 2
```
  
### Représentation en chaîne de caractères

La liste pourra être convertie en chaîne de caractères, voir la méthode `__repr__`

```python
  a_list = DoublyLinkedList([0, 1, 2])
  str(a_list)
  print(a_list)
```


### Egalité

Le test d'égalité entre deux listes vérifiera que les listes ont les mêmes éléments dans le même ordre, voir la méthode `__eq__` :

```python
  DoublyLinkedList([0, 1, 2]) == DoublyLinkedList([0, 1, 2]) # True
```


Interface standard Python
-------------------------

Les _Abstract Collection Class_ (ABC) de Python proposent une hiérarchie de type abstraits avec les méthodes (magiques) attendues correspondant aux opération supportées par les types.
En un sens, le but du TP est de **faire une implémentation de la structure de liste chainée qui s'y conforme**, ici on implémentera les interfaces `Collection` et `Reversible` voir la documentation, <https://docs.python.org/3/library/collections.abc.html>

Le plus "standard" dans les librairies Python pour les types de données de collection est de fournir un itérateur : on objet qui va permettre de parcourir les éléments de la collection sans la modifier. Un itérateur est un objet avec l'interface minimale suivante :

* une méthode `__init__`
* une méthode `__iter__` qui renvoie lui même
* une méthode `__next__` qui renvoie un élément de la collection et passe au suivant pour le prochain appel. Si on a atteint le dernier élément, alors `__next__` lève une exception particulière avec par exemple `raise StopIteration()`

Une alternative à l'utilisation d'une classe pour les itérateurs est d'utiliser l'instruction `yield`.
