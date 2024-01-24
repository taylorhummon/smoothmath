from pytest import approx, raises
from smoothmath import DomainError, Point
from smoothmath.expression import (
    Constant, Variable, Negation, Reciprocal, NthPower, NthRoot, Exponential, Multiply
)
from smoothmath._private.expression.nth_power import nth_power


def test_nth_power():
    # n = 0
    with raises(DomainError):
        nth_power(0, 0)
    with raises(DomainError):
        nth_power(3, 0)
    with raises(DomainError):
        nth_power(-3, 0)
    with raises(DomainError):
        nth_power(0.5, 0)
    # n = 1
    assert nth_power(0, 1) == 0
    assert nth_power(3, 1) == 3
    assert nth_power(-3, 1) == -3
    assert nth_power(0.5, 1) == 0.5
    # n = 2
    assert nth_power(0, 2) == 0
    assert nth_power(3, 2) == 9
    assert nth_power(-3, 2) == 9
    assert nth_power(0.5, 2) == 0.25
    # n = 3
    assert nth_power(0, 3) == 0
    assert nth_power(3, 3) == 27
    assert nth_power(-3, 3) == -27
    assert nth_power(0.5, 3) == 0.125


def test_NthPower_with_n_equal_one():
    x = Variable("x")
    z = NthPower(x, n = 1)
    global_x_partial = z.global_partial(x)
    global_differential = z.global_differential()
    # at x = 3
    point = Point({x: 3})
    assert z.evaluate(point) == approx(3)
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
    # at x = -5
    point = Point({x: -5})
    assert z.evaluate(point) == approx(-5)
    assert z.local_partial(point, x) == approx(1)
    assert global_x_partial.at(point) == approx(1)
    assert z.local_differential(point).component(x) == approx(1)
    assert global_differential.component_at(point, x) == approx(1)


def test_NthPower_with_n_equal_one_composition():
    x = Variable("x")
    z = NthPower(Constant(3) * x - Constant(1), n = 1)
    point = Point({x: 1})
    assert z.evaluate(point) == approx(2)
    assert z.local_partial(point, x) == approx(3)
    assert z.global_partial(x).at(point) == approx(3)
    assert z.local_differential(point).component(x) == approx(3)
    assert z.global_differential().component_at(point, x) == approx(3)


def test_NthPower_with_n_equal_two():
    x = Variable("x")
    z = NthPower(x, n = 2)
    global_x_partial = z.global_partial(x)
    global_differential = z.global_differential()
    # at x = 3
    point = Point({x: 3})
    assert z.evaluate(point) == approx(9)
    assert z.local_partial(point, x) == approx(6)
    assert global_x_partial.at(point) == approx(6)
    assert z.local_differential(point).component(x) == approx(6)
    assert global_differential.component_at(point, x) == approx(6)
    # at x = 0
    point = Point({x: 0})
    assert z.evaluate(point) == approx(0)
    assert z.local_partial(point, x) == approx(0)
    assert global_x_partial.at(point) == approx(0)
    assert z.local_differential(point).component(x) == approx(0)
    assert global_differential.component_at(point, x) == approx(0)
    # at x = -5
    point = Point({x: -5})
    assert z.evaluate(point) == approx(25)
    assert z.local_partial(point, x) == approx(-10)
    assert global_x_partial.at(point) == approx(-10)
    assert z.local_differential(point).component(x) == approx(-10)
    assert global_differential.component_at(point, x) == approx(-10)


def test_NthPower_with_n_equal_two_composition():
    x = Variable("x")
    z = NthPower(Constant(3) * x - Constant(1), n = 2)
    point = Point({x: 1})
    assert z.evaluate(point) == approx(4)
    assert z.local_partial(point, x) == approx(12)
    assert z.global_partial(x).at(point) == approx(12)
    assert z.local_differential(point).component(x) == approx(12)
    assert z.global_differential().component_at(point, x) == approx(12)


def test_reduce_nth_power_where_n_is_one():
    u = Variable("u")
    z = NthPower(u, n = 1)
    assert z._reduce_nth_power_where_n_is_one() == u


def test_reduce_nth_root_where_n_is_one():
    u = Variable("u")
    z = NthRoot(u, n = 1)
    assert z._reduce_nth_root_where_n_is_one() == u


def test_reduce_nth_power_of_mth_root_of_u():
    u = Variable("u")
    z = NthPower(NthRoot(u, n = 2), n = 2)
    assert z._reduce_nth_power_of_mth_root_of_u() == u
    z = NthPower(NthRoot(u, n = 6), n = 2)
    assert z._reduce_nth_power_of_mth_root_of_u() == NthPower(NthRoot(u, n = 3), n = 1)
    z = NthPower(NthRoot(u, n = 2), n = 6)
    assert z._reduce_nth_power_of_mth_root_of_u() == NthPower(NthRoot(u, n = 1), n = 3)
    z = NthPower(NthRoot(u, n = 6), n = 4)
    assert z._reduce_nth_power_of_mth_root_of_u() == NthPower(NthRoot(u, n = 3), n = 2)
    z = NthPower(NthRoot(u, n = 4), n = 6)
    assert z._reduce_nth_power_of_mth_root_of_u() == NthPower(NthRoot(u, n = 2), n = 3)


def test_reduce_nth_power_of_mth_power_of_u():
    u = Variable("u")
    z = NthPower(NthPower(u, n = 3), n = 2)
    assert z._reduce_nth_power_of_mth_power_of_u() == NthPower(u, n = 6)


def test_reduce_nth_power_of_negation_of_u():
    u = Variable("u")
    z = NthPower(Negation(u), n = 2)
    assert z._reduce_nth_power_of_negation_of_u() == NthPower(u, n = 2)
    z = NthPower(Negation(u), n = 3)
    assert z._reduce_nth_power_of_negation_of_u() == Negation(NthPower(u, n = 3))


def test_reduce_nth_power_of_reciprocal_of_u():
    u = Variable("u")
    z = NthPower(Reciprocal(u), n = 2)
    assert z._reduce_nth_power_of_reciprocal_of_u() == Reciprocal(NthPower(u, n = 2))


def test_reduce_nth_power_of_exponential_of_u():
    u = Variable("u")
    z = NthPower(Exponential(u), n = 2)
    assert z._reduce_nth_power_of_exponential_of_u() == Exponential(Multiply(Constant(2), u))
    z = NthPower(Exponential(u, base = 2), n = 3)
    assert z._reduce_nth_power_of_exponential_of_u() == Exponential(Multiply(Constant(3), u), base = 2)
