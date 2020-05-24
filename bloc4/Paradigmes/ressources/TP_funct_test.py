# pour exécuter les tests automatiquement, exécuter `pytest-3` dans le dossier

import pytest
from functools import wraps
import TP_funct as m


def counter(fn):
    """Un décorateur pour compter le nombre d'appels à une fonction"""
    @wraps(fn)
    def wrapped(*args, **kwargs):
        wrapped.invocations += 1
        return fn(*args, **kwargs)
    wrapped.invocations = 0
    return wrapped


class TestIntro:
    def test_fibo_iter(self):
        assert m.fibo_iter(0) == 0
        assert m.fibo_iter(1) == 1
        assert m.fibo_iter(2) == 1
        assert m.fibo_iter(3) == 2
        assert m.fibo_iter(4) == 3
        assert m.fibo_iter(9) == 34

    def test_fact_rec(self):
        assert m.fact_rec(0) == 1
        assert m.fact_rec(1) == 1
        assert m.fact_rec(2) == 2
        assert m.fact_rec(3) == 6
        assert m.fact_rec(4) == 24
        assert m.fact_rec(9) == 362880





class TestForall:
    ex_nil = []
    ex_ok = [4, 0, 8]
    ex_ko = [4, 4, 2, 0, 1]

    def test_forall(self):
        @counter
        def pair(x):
            return x % 2 == 0

        def pair_test(forall):
            pair.invocations = 0
            assert forall(pair, TestForall.ex_nil) == True
            assert pair.invocations == 0
            assert forall(pair, TestForall.ex_ok) == True
            assert pair.invocations == 3
            assert forall(pair, TestForall.ex_ko) == False
            assert pair.invocations == 8

        forall = [m.forall_for, m.forall_funct, m.forall_map_all, m.forall_filter, m.forall_reduce]
        [pair_test(f) for f in forall]

class TestDecorator:
    def test_maybe(self):
        # /!\ le décorateur maybe tel que demandé doit être curryfié pour être utilisable avec la syntaxe @ de python /!\
        maybe = lambda v : lambda f : m.maybe(f, v)

        @maybe(0)
        def fn(n):
            if n < 0:
                return None
            return n

        assert fn(0) == 0
        assert fn(42) == 42
        assert fn(-1) == 0


    def test_maybe_lambda(self):
        maybe = lambda v : lambda f : m.maybe_lambda(f, v)

        @counter
        def fn_c(n):
            if n < 0:
                return None
            return n

        @maybe(0)
        def fn(n):
            return fn_c(n)
        
        assert fn(0) == 0
        assert fn(42) == 42
        assert fn(-1) == 0
        assert fn_c.invocations >= 3

    def test_maybe_lambda_better(self):
        maybe = lambda v : lambda f : m.maybe_lambda_better(f, v)

        @counter
        def fn_c(n):
            if n < 0:
                return None
            return n

        @maybe(0)
        def fn(n):
            return fn_c(n)
        
        assert fn(0) == 0
        assert fn(42) == 42
        assert fn(-1) == 0
        assert fn_c.invocations == 3

    def test_memoize(self):

        @counter
        def id(x):
            return x
        
        @m.memoize
        def fn(n):
            return id(n)

        fn(0)
        fn(0)
        fn(0)
        assert id.invocations == 1
        fn(1)
        fn(1)
        assert id.invocations == 2
        fn(0)
        assert id.invocations == 2

    def test_memoize_nary(self):

        @counter
        def sumargs(*args):
            r = 0
            for x in args:
                r += x
            return r
        
        @m.memoize_nary
        def fn(*args):
            return sumargs(*args)

        fn(0, 0)
        fn(0, 0)
        fn(0, 0)
        assert sumargs.invocations == 1
        fn(0, 1)
        fn(0, 1)
        assert sumargs.invocations == 2
        fn(0, 0)
        assert sumargs.invocations == 2