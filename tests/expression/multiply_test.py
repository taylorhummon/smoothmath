from pytest import approx
from smoothmath import Point
from smoothmath.expression import (
    Variable, Constant, Negation, Multiply, Divide, Reciprocal, NthPower, NthRoot, Exponential
)


def test_2_ary_Multiply():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(x, y)
    point = Point(x = 2, y = 3)
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


def test_2_ary_Multiply_composition():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(Constant(5) * x, y - Constant(1))
    point = Point(x = 2, y = 4)
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


def test_3_ary_Multiply():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = Multiply(w, x, y)
    point = Point(w = 1, x = 2, y = 3)
    assert z.evaluate(point) == approx(6)
    assert z.local_partial(point, w) == approx(6)
    assert z.local_partial(point, x) == approx(3)
    assert z.local_partial(point, y) == approx(2)
    assert z.global_partial(w).at(point) == approx(6)
    assert z.global_partial(x).at(point) == approx(3)
    assert z.global_partial(y).at(point) == approx(2)
    local_differential = z.local_differential(point)
    assert local_differential.component(w) == approx(6)
    assert local_differential.component(x) == approx(3)
    assert local_differential.component(y) == approx(2)
    global_differential = z.global_differential()
    assert global_differential.component_at(point, w) == approx(6)
    assert global_differential.component_at(point, x) == approx(3)
    assert global_differential.component_at(point, y) == approx(2)


def test_3_ary_Multiply_composition():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = Multiply(w, x, y)
    z = Multiply(Constant(4) * w - Constant(1), Constant(5) * x, y + Constant(1))
    point = Point(w = 1, x = 2, y = 3)
    assert z.evaluate(point) == approx(120)
    assert z.local_partial(point, w) == approx(160)
    assert z.local_partial(point, x) == approx(60)
    assert z.local_partial(point, y) == approx(30)
    assert z.global_partial(w).at(point) == approx(160)
    assert z.global_partial(x).at(point) == approx(60)
    assert z.global_partial(y).at(point) == approx(30)
    local_differential = z.local_differential(point)
    assert local_differential.component(w) == approx(160)
    assert local_differential.component(x) == approx(60)
    assert local_differential.component(y) == approx(30)
    global_differential = z.global_differential()
    assert global_differential.component_at(point, w) == approx(160)
    assert global_differential.component_at(point, x) == approx(60)
    assert global_differential.component_at(point, y) == approx(30)


def test_1_ary_Multiply():
    x = Variable("x")
    z = Multiply(x)
    point = Point(x = 2)
    assert z.evaluate(point) == approx(2)
    assert z.local_partial(point, x) == approx(1)
    assert z.global_partial(x).at(point) == approx(1)
    local_differential = z.local_differential(point)
    assert local_differential.component(x) == approx(1)
    global_differential = z.global_differential()
    assert global_differential.component_at(point, x) == approx(1)


def test_1_ary_Multiply_composition():
    x = Variable("x")
    z = Multiply(Constant(5) * x - Constant(1))
    point = Point(x = 2)
    assert z.evaluate(point) == approx(9)
    assert z.local_partial(point, x) == approx(5)
    assert z.global_partial(x).at(point) == approx(5)
    local_differential = z.local_differential(point)
    assert local_differential.component(x) == approx(5)
    global_differential = z.global_differential()
    assert global_differential.component_at(point, x) == approx(5)


def test_0_ary_Multiply():
    z = Multiply()
    point = Point()
    assert z.evaluate(point) == approx(1)


def test_Multiply_by_zero():
    x = Variable("x")
    z = Multiply(Constant(0), x)
    point = Point(x = 2)
    assert z.evaluate(point) == approx(0)
    assert z.local_partial(point, x) == approx(0)
    assert z.global_partial(x).at(point) == approx(0)
    assert z.local_differential(point).component(x) == approx(0)
    assert z.global_differential().component_at(point, x) == approx(0)


def test_Multiply_by_one():
    x = Variable("x")
    z = Multiply(Constant(1), x)
    point = Point(x = 2)
    assert z.evaluate(point) == approx(2)
    assert z.local_partial(point, x) == approx(1)
    assert z.global_partial(x).at(point) == approx(1)
    assert z.local_differential(point).component(x) == approx(1)
    assert z.global_differential().component_at(point, x) == approx(1)


def test_Multiply_normalization():
    v = Variable("v")
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    # flattening
    z = Multiply(Multiply(v), Multiply(Multiply(w, x), y), Multiply())
    assert z._normalize() == Multiply(v, w, x, y)
    # with Constant
    z = Multiply(Constant(0), x)
    assert z._normalize() == Constant(0)
    z = Multiply(x, Constant(1))
    assert z._normalize() == x
    z = Multiply(Constant(1), x)
    assert z._normalize() == x
    z = Multiply(Constant(2), x, Constant(3))
    assert z._normalize() == Multiply(x, Constant(6))
    z = Multiply(Constant(0.5), x, Constant(2))
    assert z._normalize() == x
    # with Reciprocal
    z = Multiply(x, y)
    assert z._normalize() == Multiply(x, y)
    z = Multiply(x, Reciprocal(y))
    assert z._normalize() == Divide(x, y)
    z = Multiply(Reciprocal(x), y)
    assert z._normalize() == Divide(y, x)
    z = Multiply(Reciprocal(x), Reciprocal(y))
    assert z._normalize() == Reciprocal(Multiply(x, y))
    z = Multiply(Reciprocal(w), x, Reciprocal(y))
    assert z._normalize() == Divide(x, Multiply(w, y))
    z = Multiply(w, Reciprocal(x), y)
    assert z._normalize() == Divide(Multiply(w, y), x)
    z = Multiply(Reciprocal(v), w, Reciprocal(x), y)
    assert z._normalize() == Divide(Multiply(w, y), Multiply(v, x))
    # with Negation
    z = Multiply(x, Negation(y))
    assert z._normalize() == Multiply(x, y, Constant(-1))
    z = Multiply(Negation(x), Negation(y))
    assert z._normalize() == Multiply(x, y)
    # with NthPowers
    z = Multiply(NthPower(x, 2), NthPower(y, 2))
    assert z._normalize() == NthPower(Multiply(x, y), 2)
    z = Multiply(NthPower(x, 2), NthPower(y, 3))
    assert z._normalize() == Multiply(NthPower(x, 2), NthPower(y, 3))
    z = Multiply(NthPower(v, 2), NthPower(w, 3), NthPower(x, 2), y)
    assert z._normalize() == Multiply(y, NthPower(Multiply(v, x), 2), NthPower(w, 3))
    # with NthRoots
    z = Multiply(NthRoot(x, 2), NthRoot(y, 2))
    assert z._normalize() == NthRoot(Multiply(x, y), 2)
    z = Multiply(NthRoot(x, 2), NthRoot(y, 3))
    assert z._normalize() == Multiply(NthRoot(x, 2), NthRoot(y, 3))
    z = Multiply(NthRoot(v, 2), NthRoot(w, 3), NthRoot(x, 2), y)
    assert z._normalize() == Multiply(y, NthRoot(Multiply(v, x), 2), NthRoot(w, 3))
    # with Exponentials
    z = Multiply(Exponential(x, base = 2), Exponential(y, base = 2))
    assert z._normalize() == Exponential(x + y, 2)
    z = Multiply(Exponential(x, base = 2), Exponential(y, base = 3))
    assert z._normalize() == Multiply(Exponential(x, 2), Exponential(y, 3))
    z = Multiply(Exponential(v, 2), Exponential(w, 3), Exponential(x, 2), y)
    assert z._normalize() == Multiply(y, Exponential(v + x, base = 2), Exponential(w, base = 3))
