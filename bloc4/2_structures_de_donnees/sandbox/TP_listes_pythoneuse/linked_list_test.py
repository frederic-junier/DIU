"""Unitary tests for the DoublyLinkedList collection class"""

# using pycov, checks coverage with
# pytest --cov=linked_list --cov-report term-missing

from collections.abc import Iterable, Iterator
import pytest
from linked_list import DoublyLinkedList


def test_creation_empty():
    """An empty list should have its attributes set"""
    a_list = DoublyLinkedList()
    assert not a_list
    assert hasattr(a_list, "start")
    assert hasattr(a_list, "end")
    assert hasattr(a_list, "length")

def test_push_chained():
    """Calls to push should be chained"""
    a_list = DoublyLinkedList()
    after_append = a_list.push(0)
    assert id(a_list) == id(after_append)

def test_push_one():
    """One element should be added to an empty list"""
    a_list = DoublyLinkedList()
    a_list.push(0)
    assert len(a_list) == 1
    assert a_list.start == a_list.end

def test_push_two():
    """Two elements should be added to an empty list"""
    a_list = DoublyLinkedList()
    a_list.push(0)
    a_list.push(1)
    assert len(a_list) == 2
    assert a_list.start.next == a_list.end
    assert a_list.end.prev == a_list.start

def test_pop_one_from_zero():
    """Popping an empty lists should raise an exception"""
    a_list = DoublyLinkedList()
    with pytest.raises(IndexError) as excinfo:
        a_list.pop()
    assert str(excinfo.value) == "List is already empty"

def test_pop_one_from_one():
    """One element should be removed from a list of size one after pop"""
    a_list = DoublyLinkedList()
    a_list.push(0)
    value = a_list.pop()
    assert value == 0
    assert not a_list

def test_pop_two_from_two():
    """Two elements should be removed from a list of size one after two pops"""
    a_list = DoublyLinkedList()
    a_list.push(0).push(1)
    a_value = a_list.pop()
    assert a_value == 1
    another_value = a_list.pop()
    assert another_value == 0
    assert not a_list

def test_pop_one_from_three():
    """One element should be removed from a list of size three after pop"""
    a_list = DoublyLinkedList()
    a_list.push(0).push(1).push(2)
    a_value = a_list.pop()
    assert a_value == 2
    assert a_list.end.value == 1
    assert a_list.start.value == 0
    assert len(a_list) == 2

def test_iterable():
    """DoublyLinkedList should be Iterable"""
    a_list = DoublyLinkedList()
    assert isinstance(a_list, Iterable)
    an_iter = iter(a_list)
    assert isinstance(an_iter, Iterable)
    assert isinstance(an_iter, Iterator)

def test_iterable_idempotent():
    """Getting an iterator should be idempotent"""
    a_list = DoublyLinkedList()
    an_iter = iter(a_list)
    assert id(an_iter) == id(iter(an_iter))

def test_iteration():
    """Should convert a DoublyLinkedList into a built-in list using iteration protocol"""
    a_list = DoublyLinkedList()
    a_list.push(0).push(1).push(2)
    an_array = list(a_list)
    assert an_array == [0, 1, 2]

def test_reverse_iteration():
    """Should convert a DoublyLinkedList into a built-in list using reverse iteration protocol"""
    a_list = DoublyLinkedList()
    a_list.push(0).push(1).push(2)
    an_array = list(reversed(a_list))
    assert an_array == [2, 1, 0]

def test_equality():
    """DoublyLinkedList with same elements in order should be equal"""
    a_list = DoublyLinkedList()
    a_list.push(0).push(1).push(2)
    another_list = DoublyLinkedList()
    another_list.push(0).push(1).push(2)
    assert id(another_list) != id(a_list)
    assert another_list == a_list

def test_equality_unorder():
    """DoublyLinkedList with same elements in different order should NOT be equal"""
    a_list = DoublyLinkedList()
    a_list.push(0).push(1).push(2)
    another_list = DoublyLinkedList()
    another_list.push(1).push(2).push(0)
    assert id(another_list) != id(a_list)
    assert another_list != a_list

def test_equality_repeat():
    """DoublyLinkedList with different number of occurences should NOT be equal"""
    a_list = DoublyLinkedList()
    a_list.push(0).push(1).push(2)
    another_list = DoublyLinkedList()
    another_list.push(0).push(0).push(1).push(2)
    assert id(another_list) != id(a_list)
    assert another_list != a_list

def test_equality_other_class():
    """DoublyLinkedList equality with another class should return NotImplemented"""
    a_list = DoublyLinkedList()
    assert a_list.__eq__(0) == NotImplemented
    assert a_list.__eq__(True) == NotImplemented
    assert a_list.__eq__(()) == NotImplemented
    assert a_list.__eq__("test") == NotImplemented
    assert a_list.__eq__([]) == NotImplemented


def test_repr():
    """Should convert a list to string"""
    a_list = DoublyLinkedList()
    a_list.push(0).push(1).push(2)
    assert repr(a_list) == "DoublyLinkedList(0, 1, 2)"

def test_creation_from_iterable():
    """Should create a DoublyLinkedList from an iterable"""
    a_list = DoublyLinkedList([0, 1, 2])
    assert list(a_list) == [0, 1, 2]

def test_creation_from_not_iterable():
    """DoublyLinkedList from a non iterable type should raise TypeError"""
    with pytest.raises(TypeError):
        DoublyLinkedList(2)

def test_clear():
    """DoublyLinkedList should be emtpy after clear()"""
    a_list = DoublyLinkedList([0, 1, 2])
    a_list.clear()
    assert not a_list

def test_contains():
    """__contains__ method should be used by 'in' statements"""
    a_list = DoublyLinkedList([0, 1, 2])
    assert 0 in a_list
    assert 1 in a_list
    assert 2 in a_list
    assert 42 not in a_list
