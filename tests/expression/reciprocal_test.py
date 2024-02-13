from pytest import approx, raises
from smoothmath import DomainError, Point
from smoothmath.expression import Variable, Constant, Reciprocal
from assert_derivatives import ( # type: ignore
    assert_1_ary_derivatives,
    assert_1_ary_derivatives_raise
)


def test_Reciprocal():
    x = Variable("x")
    z = Reciprocal(x)
    # at x = 2
    point = Point(x = 2)
    assert z.evaluate(point) == approx(0.5)
    assert_1_ary_derivatives(z, point, x, -0.25)
    # at x = 0
    point = Point(x = 0)
    with raises(DomainError):
        z.evaluate(point)
    assert_1_ary_derivatives_raise(z, point, x)
    # at x = -1
    point = Point(x = -1)
    assert z.evaluate(point) == approx(-1)
    assert_1_ary_derivatives(z, point, x, -1)


def test_Reciprocal_composition():
    x = Variable("x")
    z = Reciprocal(Constant(2) * x - Constant(4))
    point = Point(x = 3)
    assert z.evaluate(point) == approx(0.5)
    assert_1_ary_derivatives(z, point, x, -0.5)


def test_Reciprocal_normalization():
    x = Variable("x")
    y = Variable("y")
    z = Reciprocal(x)
    assert z._normalize() == Reciprocal(x)
    z = Reciprocal(Reciprocal(x))
    assert z._normalize() == x
    z = Reciprocal(Reciprocal(Reciprocal(x)))
    assert z._normalize() == Reciprocal(x)
    z = Reciprocal(- x)
    assert z._normalize() == - Reciprocal(x)
    z = Reciprocal(x * y)
    assert z._normalize() == Reciprocal(x * y)
