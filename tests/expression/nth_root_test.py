from pytest import approx, raises
from smoothmath import DomainError, Point
from smoothmath.expression import Constant, Variable, NthRoot
from smoothmath._private.expression.nth_root import nth_root


def test_nth_root():
    # n = -2
    with raises(DomainError):
        nth_root(-2, 12)
    # n = -1
    with raises(DomainError):
        nth_root(-1, 12)
    # n = 0
    with raises(DomainError):
        nth_root(0, 12)
    # n = 1
    assert nth_root(1, 0.5) == approx(0.5)
    assert nth_root(1, 1) == 1
    assert nth_root(1, 2) == 2
    assert nth_root(1, 0) == 0
    assert nth_root(1, -0.5) == approx(-0.5)
    assert nth_root(1, -1) == -1
    assert nth_root(1, -2) == -2
    # n = 2 (a.k.a square root)
    assert nth_root(2, 0.25) == approx(0.5)
    assert nth_root(2, 1) == 1
    assert nth_root(2, 2) == approx(1.4142135623730)
    assert nth_root(2, 9) == 3
    assert nth_root(2, 50 ** 2) == 50
    with raises(DomainError):
        nth_root(2, 0)
    with raises(DomainError):
        nth_root(2, -1)
    # n = 3 (a.k.a cube root)
    assert nth_root(3, 0.125) == approx(0.5)
    assert nth_root(3, 1) == 1
    assert nth_root(3, 2) == approx(1.2599210498948)
    assert nth_root(3, 8) == 2
    assert nth_root(3, 50 ** 3) == 50
    with raises(DomainError):
        nth_root(3, 0)
    assert nth_root(3, -0.125) == approx(-0.5)
    assert nth_root(3, -1) == -1
    assert nth_root(3, -2) == approx(-1.2599210498948)
    assert nth_root(3, -8) == -2
    # n = 4
    assert nth_root(4, 0.5 ** 4) == approx(0.5)
    assert nth_root(4, 1) == 1
    assert nth_root(4, 4) == approx(1.4142135623730)
    assert nth_root(4, 81) == 3
    assert nth_root(4, 50 ** 4) == 50
    with raises(DomainError):
        nth_root(4, 0)
    with raises(DomainError):
        nth_root(4, -1)


def test_NthRoot_with_n_equal_two():
    x = Variable("x")
    z = NthRoot(2, x)
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
    z = NthRoot(2, Constant(2) * x + Constant(7))
    point = Point({x: 1})
    assert z.evaluate(point) == approx(3)
    assert z.local_partial(point, x) == approx(1 / 3)
    assert z.global_partial(x).at(point) == approx(1 / 3)
    assert z.local_differential(point).component(x) == approx(1 / 3)
    assert z.global_differential().component_at(point, x) == approx(1 / 3)


def test_NthRoot_with_n_equal_three():
    x = Variable("x")
    z = NthRoot(3, x)
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
    z = NthRoot(3, Constant(2) * x + Constant(25))
    point = Point({x: 1})
    assert z.evaluate(point) == approx(3)
    assert z.local_partial(point, x) == approx(2 / 27)
    assert z.global_partial(x).at(point) == approx(2 / 27)
    assert z.local_differential(point).component(x) == approx(2 / 27)
    assert z.global_differential().component_at(point, x) == approx(2 / 27)


def test_NthRoot_with_n_equal_one():
    x = Variable("x")
    z = NthRoot(1, x)
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
    z = NthRoot(1, Constant(2) * x + Constant(3))
    point = Point({x: 1})
    assert z.evaluate(point) == approx(5)
    assert z.local_partial(point, x) == approx(2)
    assert z.global_partial(x).at(point) == approx(2)
    assert z.local_differential(point).component(x) == approx(2)
    assert z.global_differential().component_at(point, x) == approx(2)


def test_NthRoot_with_n_equal_zero():
    x = Variable("x")
    with raises(Exception):
        NthRoot(0, x)


def test_NthRoot_where_exponent_is_an_integer_represented_as_a_float():
    x = Variable("x")
    z = NthRoot(2.0, x) # type: ignore
    point = Point({x: 9})
    assert z.evaluate(point) == approx(3)
    assert z.local_partial(point, x) == approx(1 / 6)
    assert z.global_partial(x).at(point) == approx(1 / 6)
    assert z.local_differential(point).component(x) == approx(1 / 6)
    assert z.global_differential().component_at(point, x) == approx(1 / 6)
