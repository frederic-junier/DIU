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

        pass

    def __len__(self):
        raise NotImplementedError()

    def push(self, a_value):
        """Push (append) an element to the right end of the list"""
        raise NotImplementedError()

    def pop(self):
        """Remove the element from the right end of the list, if any"""
        if not self.end:
            raise IndexError("List is already empty")

        raise NotImplementedError()

    def clear(self):
        """Empty the list"""
        raise NotImplementedError()

    def __iter__(self):
        return DoublyLinkedListIterator(self.start)

    def __reversed__(self):
        # Ici, faire votre propre classe d'itérateur pour parcourir à l'envers
        raise NotImplementedError()

    def __contains__(self, a_value):
        raise NotImplementedError()

    def __repr__(self):
        # S'appuie sur le protocole d'itération pour afficher les éléments
        class_name = type(self).__name__
        return f'{class_name}{tuple(self)}'

    def __eq__(self, other):
        # S'appuie sur le protocole d'itération et l'égalité sur le type list de Python
        if not isinstance(other, type(self)):
            return NotImplemented
        return list(self) == list(other)


class DoublyLinkedListIterator(object):
    """An iterator for doubly linked lists"""
    def __init__(self, the_start):
        pass

    def __next__(self):
        raise NotImplementedError()

    def __iter__(self):
        return self


