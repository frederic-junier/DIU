
# coding: utf-8

# Une implémentation "pythoniste" des listes doublement chaînées
# ================================================================
# 
# Dans ce TP, on va reprendre l'implémentation des listes doublement chainées dans une version plus "pythoniste" qui reprend les conventions et le fonctionnement des collections et objets Python de la bibliothèque standard.
# 
# 
# 
# **Exercice** : compléter le fichier [`linked_list.py`](linked_list.py) et tester l'implémentation avec les tests  `pytest` fournis dans [`linked_list_test.py`](linked_list_test.py).
# 
# Le reste du document est une explication du fonctionnement de la classe. Les tests comportent des exemples qui faciliteront la compréhension
# 
# 
# **Remarque additionnelle** 
# 
# > En effet ce type d'implémentation est très homogène avec les collections standard. Je compléterai en vous incitant à réfléchir sur ce que vous feriez en classe, en fonction des compétences que vous voulez cibler. Pour ce type d'implémentation "pythoneuse", il ne faut pas oublier qu'une certaine maîtrise ou recul des élèves sera nécessaire sur : les classes et l'héritage, les interfaces et classes abstraites, le principe de surcharge, les itérateurs, le type Collection (et Reversible) etc. Beaucoup de ces choses ne sont pas au programme de NSI (même Term). La classe Liste du TP de base n'a pas besoin de tout ça (juste du principe de classe) et est donc d'un autre degré d’accessibilité pour un élève. Dépendamment de ce que vous voulez leur faire faire et le placement dans l'année par rapport au reste du programme, vous pouvez inclure plus ou moins de notions "pythonesques" dans vos propres classes.
# 
# Opérations supportées
# ---------------------
# 
# Plus concrètement, on veut faire en sorte que cette implémentation des listes chainées supporte les opérations suivantes, chacune correspondant à une méthode 'magique' qui est utilisée par l'interpréteur Python.
# 
# ### Constructeur
# 
# Le constructeur peut prendre un objet itérable en paramètre pour initialiser la liste avec les éléments du paramètre, voir la la méthode `__init__` :
# 
# ```python
# a_list = DoublyLinkedList([0, 1, 2])
# a_list = DoublyLinkedList((0, 1, 2))
# ```
# 
# ### Longueur
# 
# On peut utiliser la fonction `len` (et convertir la liste en booléen), voir la méthode `__len__`, l'implémentation par défaut de `__bool__` étant de tester si `__len__` retourne 0 :
# 
# ```python
# len(a_list) # renvoie la longueur de la liste
# if a_list:  # teste si la liste est vide
#     ....
# ```
# 
# ### Appartenance
# 
# On peut utiliser le test `in` pour savoir si un élément est dans la liste, Voir la méthode `__contains__`.
# 
# ```python
# 0 in DoublyLinkedList([0, 1, 2]) # renvoie True
# 3 in DoublyLinkedList([0, 1, 2]) # renvoie False
# 3 not in DoublyLinkedList([0, 1, 2]) # renvoie True
# ```
# 
# ### Protocole d'itération
# 
# C'est le plus important, la classe doit fournir **un itérateur**  sur ses éléments. Ce _design pattern_ est utilisé en Python par toutes   les collections standards et simplifie l'écriture des programme, voir la méthode `__iter__` :
# 
# ```python
# a_list = DoublyLinkedList([0, 1, 2])
# 
# a_table = list(a_list)
# for item in a_list:
#   print(item) # affiche 0, puis 1, puis 2
# 
# a_new_list = [x*x for x in a_list] # l'équivalent de `map` pour votre structure
# ```
# 
# ### Itération à l'envers
# 
# Comme la liste est doublement chainée, on fournira aussi un itérateur qui parcoure la liste à l'envers, voir la méthode `__reversed__`
# 
# ```python
# for item in reversed(a_list):
#   print(itm) # affiche 0, puis 1, puis 2
# ```
#   
# ### Représentation en chaîne de caractères
# 
# La liste pourra être convertie en chaîne de caractères, voir la méthode `__repr__`
# 
# ```python
#   a_list = DoublyLinkedList([0, 1, 2])
#   str(a_list)
#   print(a_list)
# ```
# 
# 
# ### Egalité
# 
# Le test d'égalité entre deux listes vérifiera que les listes ont les mêmes éléments dans le même ordre, voir la méthode `__eq__` :
# 
# ```python
#   DoublyLinkedList([0, 1, 2]) == DoublyLinkedList([0, 1, 2]) # True
# ```
# 
# 
# Interface standard Python
# -------------------------
# 
# Les _Abstract Collection Class_ (ABC) de Python proposent une hiérarchie de type abstraits avec les méthodes (magiques) attendues correspondant aux opération supportées par les types.
# En un sens, le but du TP est de **faire une implémentation de la structure de liste chainée qui s'y conforme**, ici on implémentera les interfaces `Collection` et `Reversible` voir la documentation, <https://docs.python.org/3/library/collections.abc.html>
# 
# Le plus "standard" dans les librairies Python pour les types de données de collection est de fournir un itérateur : on objet qui va permettre de parcourir les éléments de la collection sans la modifier. Un itérateur est un objet avec l'interface minimale suivante :
# 
# * une méthode `__init__`
# * une méthode `__iter__` qui renvoie lui même
# * une méthode `__next__` qui renvoie un élément de la collection et passe au suivant pour le prochain appel. Si on a atteint le dernier élément, alors `__next__` lève une exception particulière avec par exemple `raise StopIteration()`
# 
# Une alternative à l'utilisation d'une classe pour les itérateurs est d'utiliser l'instruction `yield`.
# 

# In[96]:


"""A module for doubly linked lists."""
from collections.abc import Collection, Reversible, Iterable

class Node(object):
    """A node type for doubly linked lists"""

    def __init__(self, a_value, prev_node=None, next_node=None):
        self.value = a_value
        self.prev = prev_node
        self.next = next_node

class DoublyLinkedList(Collection, Reversible):
    """A collection type for doubly linked lists"""

    def __init__(self, iterable=()):
        if not isinstance(iterable, Iterable):
            raise TypeError("Parameter 'iterable' is not Iterable")
        self.start = None
        self.end = None
        self.length = 0
        for value in iterable:
            self.push(value)
            self.length += 1


    def __len__(self):
        return self.length

    def push(self, a_value):
        """Push (append) an element to the right end of the list"""
        new = Node(a_value, prev_node=self.end, next_node=None)
        if self.end is not None:
            self.end.next = new
            self.end = new
        else:  #cas particulier d'une liste vide
            self.start = self.end = new
        self.length += 1
        return self

    def pop(self):
        """Remove the element from the right end of the list, if any"""
        if self.end is  None:
            raise IndexError("List is already empty")
        out = self.end
        if self.length == 1:
            self.start = self.end =  None
        else:
            self.end.prev.next = None        
            self.end = self.end.prev
        self.length -= 1
        return out.value 
    
    def clear(self):
        """Empty the list"""
        while self.start is not None:
            out = self.start
            self.start = self.start.next
            del out
        self.end = None
        self.length = 0
            

    def __iter__(self):
        return DoublyLinkedListIterator(self.start)

    def __reversed__(self):
        # Ici, faire votre propre classe d'itérateur pour parcourir à l'envers
        return DoublyLinkedListReverseIterator(self.end)

    def __contains__(self, a_value):
        pointeur = self.start
        while pointeur is not None and pointeur.value != a_value:
            pointeur = pointeur.next
        return pointeur is not None

    def __repr__(self):
        # S'appuie sur le protocole d'itération pour afficher les éléments
        class_name = type(self).__name__
        return f'{class_name}{tuple(self)}'
    
    #def __str__(self):
        # S'appuie sur le protocole d'itération pour afficher les éléments
      #return '[' + ','.join(str(e) for e in self) + ']'

    def __eq__(self, other):
        # S'appuie sur le protocole d'itération et l'égalité sur le type list de Python
        if not isinstance(other, type(self)):
            return NotImplemented
        return list(self) == list(other)


class DoublyLinkedListIterator(object):
    """An iterator for doubly linked lists"""
    def __init__(self, the_start):
        self.curseur = the_start

    def __next__(self):
        if self.curseur is not None:
            value = self.curseur.value
            self.curseur = self.curseur.next
            return value
        raise StopIteration

    def __iter__(self):
        return self
    
class DoublyLinkedListReverseIterator(object):
    """An iterator for doubly linked lists"""
    def __init__(self, the_end):
        self.curseur = the_end

    def __next__(self):
        if self.curseur is not None:
            value = self.curseur.value
            self.curseur = self.curseur.prev
            return value
        raise StopIteration

    def __iter__(self):
        return self


# In[78]:


a_list = DoublyLinkedList([0, 1, 2])


# In[79]:


1 in a_list


# In[80]:


3 in a_list


# In[81]:


len(a_list)


# In[82]:


for e in a_list:
    print(e)


# In[83]:


a_list


# In[84]:


print(a_list)


# In[85]:


for e in reversed(a_list):
    print(e)


# In[86]:


repr(a_list)


# In[87]:


str(a_list)


# In[88]:


a_list.clear()


# In[89]:


a_list


# In[90]:


isinstance(a_list, Collection)


# In[91]:


isinstance(a_list, Reversible)


# In[92]:


a_list.push(0)


# In[93]:


a_list


# In[94]:


a_list.push(1).push(2)


# In[95]:


a_list.pop()


# ```
# fjunier@fjunier:~/Git/DIU-Junier/bloc4/2_structures_de_donnees/sandbox/TP_listes_pythoneuse$ pytest-3
# =========================================================================================== test session starts ============================================================================================
# platform linux -- Python 3.6.9, pytest-3.3.2, py-1.5.2, pluggy-0.6.0
# rootdir: /home/fjunier/Git/DIU-Junier/bloc4/2_structures_de_donnees/sandbox/TP_listes_pythoneuse, inifile:
# plugins: Faker-4.1.0
# collected 21 items                                                                                                                                                                                         
# 
# linked_list_test.py .....................                                                                                                                                                            [100%]
# 
# ======================================================================================== 21 passed in 0.10 seconds =========================================================================================
# ```
