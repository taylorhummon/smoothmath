from pytest import approx
from smoothmath import Point
from smoothmath.expression import Constant, Variable, Negation, Logarithm, Plus, Multiply


def test_Plus():
    x = Variable("x")
    y = Variable("y")
    z = Plus(x, y)
    point = Point({x: 2, y: 3})
    assert z.evaluate(point) == approx(5)
    assert z.local_partial(point, x) == approx(1)
    assert z.local_partial(point, y) == approx(1)
    assert z.global_partial(x).at(point) == approx(1)
    assert z.global_partial(y).at(point) == approx(1)
    local_differential = z.local_differential(point)
    assert local_differential.component(x) == approx(1)
    assert local_differential.component(y) == approx(1)
    global_differential = z.global_differential()
    assert global_differential.component_at(point, x) == approx(1)
    assert global_differential.component_at(point, y) == approx(1)


def test_Plus_composition():
    x = Variable("x")
    y = Variable("y")
    z = Plus(Constant(5) * x, Constant(4) * y)
    point = Point({x: 2, y: 3})
    assert z.evaluate(point) == approx(22)
    assert z.local_partial(point, x) == approx(5)
    assert z.local_partial(point, y) == approx(4)
    assert z.global_partial(x).at(point) == approx(5)
    assert z.global_partial(y).at(point) == approx(4)
    local_differential = z.local_differential(point)
    assert local_differential.component(x) == approx(5)
    assert local_differential.component(y) == approx(4)
    global_differential = z.global_differential()
    assert global_differential.component_at(point, x) == approx(5)
    assert global_differential.component_at(point, y) == approx(4)


def test_reduce_by_associating_plus_right():
    u = Variable("u")
    v = Variable("v")
    w = Variable("w")
    z = Plus(Plus(u, v), w)
    assert z._reduce_by_associating_plus_right() == Plus(u, Plus(v, w))


def test_reduce_u_plus_zero():
    u = Variable("u")
    z = Plus(u, Constant(0))
    assert z._reduce_u_plus_zero() == u


def test_reduce_by_commuting_constant_right_across_plus():
    u = Variable("u")
    z = Plus(Constant(7), u)
    assert z._reduce_by_commuting_constant_right_across_plus() == Plus(u, Constant(7))


def test_reduce_by_commuting_negation_right_across_plus():
    u = Variable("u")
    v = Variable("v")
    z = Plus(Negation(u), v)
    assert z._reduce_by_commuting_negation_right_across_plus() == Plus(v, Negation(u))


def test_reduce_sum_of_negations():
    u = Variable("u")
    v = Variable("v")
    z = Plus(Negation(u), Negation(v))
    assert z._reduce_sum_of_negations() == Negation(Plus(u, v))


def test_reduce_sum_of_logarithms():
    u = Variable("u")
    v = Variable("v")
    z = Plus(Logarithm(u), Logarithm(v))
    assert z._reduce_sum_of_logarithms() == Logarithm(Multiply(u, v))
    z = Plus(Logarithm(u, base = 2), Logarithm(v, base = 2))
    assert z._reduce_sum_of_logarithms() == Logarithm(Multiply(u, v), base = 2)
