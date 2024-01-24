from pytest import approx
from smoothmath import Point
from smoothmath.expression import (
    Constant, Variable, Negation, Reciprocal, NthPower, NthRoot, Exponential, Plus, Multiply
)


def test_Multiply():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(x, y)
    point = Point({x: 2, y: 3})
    assert z.evaluate(point) == approx(6)
    assert z.local_partial(point, x) == approx(3)
    assert z.local_partial(point, y) == approx(2)
    assert z.global_partial(x).at(point) == approx(3)
    assert z.global_partial(y).at(point) == approx(2)
    local_differential = z.local_differential(point)
    assert local_differential.component(x) == approx(3)
    assert local_differential.component(y) == approx(2)
    global_differential = z.global_differential()
    assert global_differential.component_at(point, x) == approx(3)
    assert global_differential.component_at(point, y) == approx(2)


def test_Multiply_composition():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(Constant(5) * x, y - Constant(1))
    point = Point({x: 2, y: 4})
    assert z.evaluate(point) == approx(30)
    assert z.local_partial(point, x) == approx(15)
    assert z.local_partial(point, y) == approx(10)
    assert z.global_partial(x).at(point) == approx(15)
    assert z.global_partial(y).at(point) == approx(10)
    local_differential = z.local_differential(point)
    assert local_differential.component(x) == approx(15)
    assert local_differential.component(y) == approx(10)
    global_differential = z.global_differential()
    assert global_differential.component_at(point, x) == approx(15)
    assert global_differential.component_at(point, y) == approx(10)


def test_Multiply_by_zero():
    x = Variable("x")
    z = Multiply(Constant(0), x)
    point = Point({x: 2})
    assert z.evaluate(point) == approx(0)
    assert z.local_partial(point, x) == approx(0)
    assert z.global_partial(x).at(point) == approx(0)
    assert z.local_differential(point).component(x) == approx(0)
    assert z.global_differential().component_at(point, x) == approx(0)


def test_Multiply_by_one():
    x = Variable("x")
    z = Multiply(Constant(1), x)
    point = Point({x: 2})
    assert z.evaluate(point) == approx(2)
    assert z.local_partial(point, x) == approx(1)
    assert z.global_partial(x).at(point) == approx(1)
    assert z.local_differential(point).component(x) == approx(1)
    assert z.global_differential().component_at(point, x) == approx(1)


def test_reduce_by_associating_multiply_left():
    u = Variable("u")
    v = Variable("v")
    w = Variable("w")
    z = Multiply(u, Multiply(v, w))
    assert z._reduce_by_associating_multiply_left() == Multiply(Multiply(u, v), w)


def test_reduce_one_times_u():
    u = Variable("u")
    z = Multiply(Constant(1), u)
    assert z._reduce_one_times_u() == u


def test_reduce_zero_times_u():
    u = Variable("u")
    z = Multiply(Constant(0), u)
    assert z._reduce_zero_times_u() == Constant(0)


def test_reduce_negative_one_times_u():
    u = Variable("u")
    z = Multiply(Constant(-1), u)
    assert z._reduce_negative_one_times_u() == Negation(u)


def test_reduce_by_commuting_constant_left_across_multiply():
    u = Variable("u")
    z = Multiply(u, Constant(12))
    assert z._reduce_by_commuting_constant_left_across_multiply() == Multiply(Constant(12), u)


def test_reduce_negation_of_u__times_v():
    u = Variable("u")
    v = Variable("v")
    z = Multiply(Negation(u), v)
    assert z._reduce_negation_of_u__times_v() == Negation(Multiply(u, v))


def test_reduce_u_times_negation_of_v():
    u = Variable("u")
    v = Variable("v")
    z = Multiply(u, Negation(v))
    assert z._reduce_u_times_negation_of_v() == Negation(Multiply(u, v))


def test_reduce_by_commuting_reciprocal_left_across_multiply():
    u = Variable("u")
    v = Variable("v")
    z = Multiply(u, Reciprocal(v))
    assert z._reduce_by_commuting_reciprocal_left_across_multiply() == Multiply(Reciprocal(v), u)


def test_reduce_product_of_reciprocals():
    u = Variable("u")
    v = Variable("v")
    z = Multiply(Reciprocal(u), Reciprocal(v))
    assert z._reduce_product_of_reciprocals() == Reciprocal(Multiply(u, v))


def test_reduce_product_of_nth_powers():
    u = Variable("u")
    v = Variable("v")
    z = Multiply(NthPower(u, n = 2), NthPower(v, n = 2))
    assert z._reduce_product_of_nth_powers() == NthPower(Multiply(u, v), n = 2)


def test_reduce_product_of_nth_roots():
    u = Variable("u")
    v = Variable("v")
    z = Multiply(NthRoot(u, n = 2), NthRoot(v, n = 2))
    assert z._reduce_product_of_nth_roots() == NthRoot(Multiply(u, v), n = 2)


def test_reduce_product_of_exponentials():
    u = Variable("u")
    v = Variable("v")
    z = Multiply(Exponential(u), Exponential(v))
    assert z._reduce_product_of_exponentials() == Exponential(Plus(u, v))
    z = Multiply(Exponential(u, base = 2), Exponential(v, base = 2))
    assert z._reduce_product_of_exponentials() == Exponential(Plus(u, v), base = 2)
