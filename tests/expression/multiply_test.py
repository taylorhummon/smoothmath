from pytest import approx
from smoothmath import Point
from smoothmath.expression import (
    Variable, Constant, Negation, Multiply, Divide, Reciprocal, NthPower, NthRoot, Exponential
)
from assert_derivatives import ( # type: ignore
    assert_1_ary_derivatives,
    assert_2_ary_derivatives,
    assert_3_ary_derivatives
)


def test_2_ary_Multiply():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(x, y)
    point = Point(x = 2, y = 3)
    assert z.evaluate(point) == approx(6)
    assert_2_ary_derivatives(z, point, x, 3, y, 2)


def test_2_ary_Multiply_composition():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(Constant(5) * x, y - Constant(1))
    point = Point(x = 2, y = 4)
    assert z.evaluate(point) == approx(30)
    assert_2_ary_derivatives(z, point, x, 15, y, 10)


def test_3_ary_Multiply():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = Multiply(w, x, y)
    point = Point(w = 1, x = 2, y = 3)
    assert z.evaluate(point) == approx(6)
    assert_3_ary_derivatives(z, point, w, 6, x, 3, y, 2)


def test_3_ary_Multiply_composition():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = Multiply(w, x, y)
    z = Multiply(Constant(4) * w - Constant(1), Constant(5) * x, y + Constant(1))
    point = Point(w = 1, x = 2, y = 3)
    assert z.evaluate(point) == approx(120)
    assert_3_ary_derivatives(z, point, w, 160, x, 60, y, 30)


def test_1_ary_Multiply():
    x = Variable("x")
    z = Multiply(x)
    point = Point(x = 2)
    assert z.evaluate(point) == approx(2)
    assert_1_ary_derivatives(z, point, x, 1)


def test_1_ary_Multiply_composition():
    x = Variable("x")
    z = Multiply(Constant(5) * x - Constant(1))
    point = Point(x = 2)
    assert z.evaluate(point) == approx(9)
    assert_1_ary_derivatives(z, point, x, 5)


def test_0_ary_Multiply():
    z = Multiply()
    point = Point()
    assert z.evaluate(point) == approx(1)


def test_Multiply_by_zero():
    x = Variable("x")
    z = Multiply(Constant(0), x)
    point = Point(x = 2)
    assert z.evaluate(point) == approx(0)
    assert_1_ary_derivatives(z, point, x, 0)


def test_Multiply_by_one():
    x = Variable("x")
    z = Multiply(Constant(1), x)
    point = Point(x = 2)
    assert z.evaluate(point) == approx(2)
    assert_1_ary_derivatives(z, point, x, 1)


def test_Multiply_normalization_with_flattening():
    v = Variable("v")
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = Multiply(Multiply(v), Multiply(Multiply(w, x), y), Multiply())
    assert z._normalize() == Multiply(v, w, x, y)


def test_Multiply_normalization_with_Constant():
    x = Variable("x")
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


def test_Multiply_normalization_with_Reciprocal():
    v = Variable("v")
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
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


def test_Multiply_normalization_with_Negation():
    x = Variable("x")
    y = Variable("y")
    z = Multiply(x, Negation(y))
    assert z._normalize() == Multiply(x, y, Constant(-1))
    z = Multiply(Negation(x), Negation(y))
    assert z._normalize() == Multiply(x, y)


def test_Multiply_normalization_with_NthPower():
    v = Variable("v")
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = Multiply(NthPower(x, 2), NthPower(y, 2))
    assert z._normalize() == NthPower(Multiply(x, y), 2)
    z = Multiply(NthPower(x, 2), NthPower(y, 3))
    assert z._normalize() == Multiply(NthPower(x, 2), NthPower(y, 3))
    z = Multiply(NthPower(v, 2), NthPower(w, 3), NthPower(x, 2), y)
    assert z._normalize() == Multiply(y, NthPower(Multiply(v, x), 2), NthPower(w, 3))


def test_Multiply_normalization_with_NthRoot():
    v = Variable("v")
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = Multiply(NthRoot(x, 2), NthRoot(y, 2))
    assert z._normalize() == NthRoot(Multiply(x, y), 2)
    z = Multiply(NthRoot(x, 2), NthRoot(y, 3))
    assert z._normalize() == Multiply(NthRoot(x, 2), NthRoot(y, 3))
    z = Multiply(NthRoot(v, 2), NthRoot(w, 3), NthRoot(x, 2), y)
    assert z._normalize() == Multiply(y, NthRoot(Multiply(v, x), 2), NthRoot(w, 3))


def test_Multiply_normalization_with_Exponential():
    v = Variable("v")
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = Multiply(Exponential(x, base = 2), Exponential(y, base = 2))
    assert z._normalize() == Exponential(x + y, 2)
    z = Multiply(Exponential(x, base = 2), Exponential(y, base = 3))
    assert z._normalize() == Multiply(Exponential(x, 2), Exponential(y, 3))
    z = Multiply(Exponential(v, 2), Exponential(w, 3), Exponential(x, 2), y)
    assert z._normalize() == Multiply(y, Exponential(v + x, base = 2), Exponential(w, base = 3))
