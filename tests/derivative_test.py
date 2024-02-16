from pytest import approx, raises
from smoothmath import DomainError, Point, Derivative
from smoothmath.expression import Variable, Constant, NthPower, Logarithm


def test_Derivative():
    x = Variable("x")
    z = Constant(5) * x + x ** 3
    point = Point(x = 3)
    derivative = Derivative(z)
    assert derivative.at(3) == approx(32)
    assert derivative.at(point) == approx(32)
    assert derivative.as_expression() == Constant(5) + Constant(3) * NthPower(Variable("x"), 2)
    eager_derivative = Derivative(z, compute_eagerly = True)
    assert eager_derivative.at(3) == approx(32)
    assert eager_derivative.at(point) == approx(32)
    assert eager_derivative.as_expression() == Constant(5) + Constant(3) * NthPower(Variable("x"), 2)


def test_Derivative_raises():
    x = Variable("x")
    y = Variable("y")
    z = x ** 2 + y ** 2
    with raises(Exception):
        Derivative(z)
    with raises(Exception):
        Derivative(z, compute_eagerly = True)


def test_Derivative_at_raises():
    x = Variable("x")
    z = Logarithm(x)
    derivative = Derivative(z)
    with raises(DomainError):
        derivative.at(Point(x = -1))


def test_Derivative_equality():
    x = Variable("x")
    assert Derivative(x ** 2) == Derivative(x ** 2)
    y = Variable("y")
    assert Derivative(x ** 2) != Derivative(y ** 2)


def test_Derivative_hashing():
    x = Variable("x")
    z = x ** 2
    assert hash(Derivative(z)) == hash(Derivative(z))
