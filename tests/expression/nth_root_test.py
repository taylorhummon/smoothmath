from pytest import approx, raises
from smoothmath import DomainError, Point
from smoothmath.expression import Constant, Variable, Negation, Reciprocal, NthPower, NthRoot


def test_NthRoot_with_n_equal_two():
    x = Variable("x")
    z = NthRoot(x, n = 2)
    global_x_partial = z.global_partial(x)
    global_differential = z.global_differential()
    # at x = 4
    point = Point({x: 4})
    assert z.evaluate(point) == approx(2)
    assert z.local_partial(point, x) == approx(1 / 4)
    assert global_x_partial.at(point) == approx(1 / 4)
    assert z.local_differential(point).component(x) == approx(1 / 4)
    assert global_differential.component_at(point, x) == approx(1 / 4)
    # at x = 0
    point = Point({x: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, x)
    with raises(DomainError):
        global_x_partial.at(point)
    with raises(DomainError):
        z.local_differential(point).component(x)
    with raises(DomainError):
        global_differential.component_at(point, x)
    # at x = -1
    point = Point({x: -1})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, x)
    with raises(DomainError):
        global_x_partial.at(point)
    with raises(DomainError):
        z.local_differential(point).component(x)
    with raises(DomainError):
        global_differential.component_at(point, x)


def test_NthRoot_with_n_equal_two_composition():
    x = Variable("x")
    z = NthRoot(Constant(2) * x + Constant(7), n = 2)
    point = Point({x: 1})
    assert z.evaluate(point) == approx(3)
    assert z.local_partial(point, x) == approx(1 / 3)
    assert z.global_partial(x).at(point) == approx(1 / 3)
    assert z.local_differential(point).component(x) == approx(1 / 3)
    assert z.global_differential().component_at(point, x) == approx(1 / 3)


def test_NthRoot_with_n_equal_three():
    x = Variable("x")
    z = NthRoot(x, n = 3)
    global_x_partial = z.global_partial(x)
    global_differential = z.global_differential()
    # at x = 4
    point = Point({x: 8})
    assert z.evaluate(point) == approx(2)
    assert z.local_partial(point, x) == approx(1 / 12)
    assert global_x_partial.at(point) == approx(1 / 12)
    assert z.local_differential(point).component(x) == approx(1 / 12)
    assert global_differential.component_at(point, x) == approx(1 / 12)
    # at x = 0
    point = Point({x: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, x)
    with raises(DomainError):
        global_x_partial.at(point)
    with raises(DomainError):
        z.local_differential(point).component(x)
    with raises(DomainError):
        global_differential.component_at(point, x)
    # at x = -1
    point = Point({x: -1})
    assert z.evaluate(point) == approx(-1)
    assert z.local_partial(point, x) == approx(1 / 3)
    assert global_x_partial.at(point) == approx(1 / 3)
    assert z.local_differential(point).component(x) == approx(1 / 3)
    assert global_differential.component_at(point, x) == approx(1 / 3)


def test_NthRoot_with_n_equal_three_composition():
    x = Variable("x")
    z = NthRoot(Constant(2) * x + Constant(25), n = 3)
    point = Point({x: 1})
    assert z.evaluate(point) == approx(3)
    assert z.local_partial(point, x) == approx(2 / 27)
    assert z.global_partial(x).at(point) == approx(2 / 27)
    assert z.local_differential(point).component(x) == approx(2 / 27)
    assert z.global_differential().component_at(point, x) == approx(2 / 27)


def test_NthRoot_with_n_equal_one():
    x = Variable("x")
    z = NthRoot(x, n = 1)
    global_x_partial = z.global_partial(x)
    global_differential = z.global_differential()
    # at x = 4
    point = Point({x: 4})
    assert z.evaluate(point) == approx(4)
    assert z.local_partial(point, x) == approx(1)
    assert global_x_partial.at(point) == approx(1)
    assert z.local_differential(point).component(x) == approx(1)
    assert global_differential.component_at(point, x) == approx(1)
    # at x = 0
    point = Point({x: 0})
    assert z.evaluate(point) == approx(0)
    assert z.local_partial(point, x) == approx(1)
    assert global_x_partial.at(point) == approx(1)
    assert z.local_differential(point).component(x) == approx(1)
    assert global_differential.component_at(point, x) == approx(1)
    # at x = -1
    point = Point({x: -1})
    assert z.evaluate(point) == approx(-1)
    assert z.local_partial(point, x) == approx(1)
    assert global_x_partial.at(point) == approx(1)
    assert z.local_differential(point).component(x) == approx(1)
    assert global_differential.component_at(point, x) == approx(1)


def test_NthRoot_with_n_equal_one_composition():
    x = Variable("x")
    z = NthRoot(Constant(2) * x + Constant(3), n = 1)
    point = Point({x: 1})
    assert z.evaluate(point) == approx(5)
    assert z.local_partial(point, x) == approx(2)
    assert z.global_partial(x).at(point) == approx(2)
    assert z.local_differential(point).component(x) == approx(2)
    assert z.global_differential().component_at(point, x) == approx(2)


def test_NthRoot_with_n_equal_zero():
    x = Variable("x")
    with raises(Exception):
        NthRoot(x, n = 0)


def test_NthRoot_where_exponent_is_an_integer_represented_as_a_float():
    x = Variable("x")
    z = NthRoot(x, n = 2.0) # type: ignore
    point = Point({x: 9})
    assert z.evaluate(point) == approx(3)
    assert z.local_partial(point, x) == approx(1 / 6)
    assert z.global_partial(x).at(point) == approx(1 / 6)
    assert z.local_differential(point).component(x) == approx(1 / 6)
    assert z.global_differential().component_at(point, x) == approx(1 / 6)


def test_NthRoot_normalization():
    x = Variable("x")
    z = NthRoot(x, n = 1)
    assert z._normalize() == x
    z = NthRoot(x, n = 2)
    assert z._normalize() == NthRoot(x, n = 2)
    z = NthRoot(NthRoot(x, n = 3), n = 2)
    assert z._normalize() == NthRoot(x, n = 6)
    z = NthRoot(NthPower(x, n = 2), n = 2)
    assert z._normalize() == x
    z = NthRoot(NthPower(x, n = 2), n = 6)
    assert z._normalize() == NthRoot(x, n = 3)
    z = NthRoot(NthPower(x, n = 6), n = 2)
    assert z._normalize() == NthPower(x, n = 3)
    z = NthRoot(NthPower(x, n = 6), n = 4)
    assert z._normalize() == NthPower(NthRoot(x, n = 2), n = 3)
    z = NthRoot(NthPower(x, n = 4), n = 6)
    assert z._normalize() == NthPower(NthRoot(x, n = 3), n = 2)
    z = NthRoot(Negation(x), n = 2)
    assert z._normalize() == NthRoot(Negation(x), n = 2)
    z = NthRoot(Negation(x), n = 3)
    assert z._normalize() == Negation(NthRoot(x, n = 3))
    z = NthRoot(Reciprocal(x), n = 2)
    assert z._normalize() == Reciprocal(NthRoot(x, n = 2))
    z = NthRoot(Reciprocal(x), n = 3)
    assert z._normalize() == Reciprocal(NthRoot(x, n = 3))
