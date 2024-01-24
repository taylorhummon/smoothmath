from pytest import approx, raises
from smoothmath import DomainError, Point
from smoothmath.expression import Constant, Variable, Negation, Reciprocal, NthPower, NthRoot
from smoothmath._private.expression.nth_root import nth_root


def test_nth_root():
    # n = -2
    with raises(DomainError):
        nth_root(12, -2)
    # n = -1
    with raises(DomainError):
        nth_root(12, -1)
    # n = 0
    with raises(DomainError):
        nth_root(0, 12)
    # n = 1
    assert nth_root(0.5, 1) == approx(0.5)
    assert nth_root(1, 1) == approx(1)
    assert nth_root(2, 1) == approx(2)
    assert nth_root(0, 1) == approx(0)
    assert nth_root(-0.5, 1) == approx(-0.5)
    assert nth_root(-1, 1) == approx(-1)
    assert nth_root(-2, 1) == approx(-2)
    # n = 2 (a.k.a square root)
    assert nth_root(0.25, 2) == approx(0.5)
    assert nth_root(1, 2) == approx(1)
    assert nth_root(2, 2) == approx(1.4142135623730)
    assert nth_root(9, 2) == approx(3)
    assert nth_root(50 ** 2, 2) == approx(50)
    with raises(DomainError):
        nth_root(0, 2)
    with raises(DomainError):
        nth_root(-1, 2)
    # n = 3 (a.k.a cube root)
    assert nth_root(0.125, 3) == approx(0.5)
    assert nth_root(1, 3) == approx(1)
    assert nth_root(2, 3) == approx(1.2599210498948)
    assert nth_root(8, 3) == approx(2)
    assert nth_root(50 ** 3, 3) == approx(50)
    with raises(DomainError):
        nth_root(0, 3)
    assert nth_root(-0.125, 3) == approx(-0.5)
    assert nth_root(-1, 3) == approx(-1)
    assert nth_root(-2, 3) == approx(-1.2599210498948)
    assert nth_root(-8, 3) == approx(-2)
    # n = 4
    assert nth_root(0.5 ** 4, 4) == approx(0.5)
    assert nth_root(1, 4) == approx(1)
    assert nth_root(4, 4) == approx(1.4142135623730)
    assert nth_root(81, 4) == approx(3)
    assert nth_root(50 ** 4, 4) == approx(50)
    with raises(DomainError):
        nth_root(0, 4)
    with raises(DomainError):
        nth_root(-1, 4)
    # n = 5
    assert nth_root(0.5 ** 5, 5) == approx(0.5)
    assert nth_root(1, 5) == approx(1)
    assert nth_root(4, 5) == approx(1.3195079107728942)
    assert nth_root(243, 5) == approx(3)
    assert nth_root(50 ** 5, 5) == approx(50)
    with raises(DomainError):
        nth_root(0, 5)
    assert nth_root(-1, 5) == approx(-1)
    assert nth_root(-243, 5) == approx(-3)


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


def test_reduce_nth_root_of_mth_power_of_u():
    u = Variable("u")
    z = NthRoot(NthPower(u, n = 2), n = 3)
    assert z._reduce_nth_root_of_mth_power_of_u() == NthPower(NthRoot(u, n = 3), n = 2)


def test_reduce_nth_root_of_mth_root_of_u():
    u = Variable("u")
    z = NthRoot(NthRoot(u, n = 3), n = 2)
    assert z._reduce_nth_root_of_mth_root_of_u() == NthRoot(u, n = 6)


def test_reduce_odd_nth_root_of_negation_of_u():
    u = Variable("u")
    z = NthRoot(Negation(u), n = 3)
    assert z._reduce_odd_nth_root_of_negation_of_u() == Negation(NthRoot(u, n = 3))


def test_reduce_nth_root_of_reciprocal_of_u():
    u = Variable("u")
    z = NthRoot(Reciprocal(u), n = 2)
    assert z._reduce_nth_root_of_reciprocal_of_u() == Reciprocal(NthRoot(u, n = 2))
