"""Test unitaires des algorithmes de jointure en Python"""

from join_algorithms import join_nested_loop, join_hash, join_merge

# pylint: disable=invalid-name

sample_table_1 = [
    (27, "Jonah"),
    (28, "Alan"),
    (18, "Alan"),
    (10, "Peppa"),
    (28, "Glory"),
    (18, "Popeye"),
    (19, "Popeye"),
]

sample_table_2 = [
    ("Jonah", "Whales"),
    ("Alan", "Ghosts"),
    ("Jonah", "Spiders"),
    ("Alan", "Zombies"),
    ("Glory", "Buffy"),
    ("John", "Bats"),
    ("Popeye", "Spinach"),
]

# Alan est 2x dans t1 et 2x dans t2, il apparait 4 fois dans la jointure
# Glory est 1x dans t1 et 1x dans t2, elle apparait 1 fois dans la jointure
# Jonah est 1x dans t1 et 2x dans t2, il apparait 2 fois dans la jointure
# Popeye est 2x dans t1 et 1x dans t2, il apparait 2 fois dans la jointure
# Peppa est 1x dans t1 et 0x dans t2, elle apparait 0 fois dans la jointure
# John est 0x dans t1 et 1x dans t2, il apparait 0 fois dans la jointure

reference_result = [
    (18, 'Alan', 'Alan', 'Ghosts'),
    (18, 'Alan', 'Alan', 'Zombies'),
    (28, 'Alan', 'Alan', 'Ghosts'),
    (28, 'Alan', 'Alan', 'Zombies'),
    (28, 'Glory', 'Glory', 'Buffy'),
    (27, 'Jonah', 'Jonah', 'Spiders'),
    (27, 'Jonah', 'Jonah', 'Whales'),
    (18, 'Popeye', 'Popeye', 'Spinach'),
    (19, 'Popeye', 'Popeye', 'Spinach')]

def test_join_nested_loop():
    """Tests for naive join with nested loops"""
    results = join_nested_loop(sample_table_1, 1, sample_table_2, 0)
    results.sort(key=lambda x: (x[1], x[0], x[3]))
    assert results == reference_result

def test_join_hash():
    """Tests for hash join"""
    results = join_hash(sample_table_1, 1, sample_table_2, 0)
    results.sort(key=lambda x: (x[1], x[0], x[3]))
    assert results == reference_result

def test_join_merge():
    """Tests for merge join"""
    sample_table_1.sort(key=lambda x: x[1])
    sample_table_2.sort(key=lambda x: x[0])
    results = join_merge(sample_table_1, 1, sample_table_2, 0)
    results.sort(key=lambda x: (x[1], x[0], x[3]))
    assert results == reference_result
