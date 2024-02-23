from pytest import approx, raises
from smoothmath import DomainError, Point, Derivative
from smoothmath.expression import Variable, Constant, NthPower, Logarithm


def test_Derivative():
    x = Variable("x")
    z = Constant(5) * x + x ** 3
    point = Point(x = 3)
    late_derivative = Derivative(z, compute_early = False)
    assert late_derivative.at(3) == approx(32)
    assert late_derivative.at(point) == approx(32)
    late_derivative_expression = late_derivative.as_expression()
    assert late_derivative_expression.at(point) == approx(32)
    assert late_derivative_expression == Constant(5) + Constant(3) * NthPower(Variable("x"), 2)
    early_derivative = Derivative(z, compute_early = True)
    assert early_derivative.at(3) == approx(32)
    assert early_derivative.at(point) == approx(32)
    early_derivative_expression = early_derivative.as_expression()
    assert early_derivative_expression.at(point) == approx(32)
    assert early_derivative_expression == Constant(5) + Constant(3) * NthPower(Variable("x"), 2)


def test_Derivative_raises():
    x = Variable("x")
    y = Variable("y")
    z = x ** 2 + y ** 2
    with raises(Exception):
        Derivative(z, compute_early = False)
    with raises(Exception):
        Derivative(z, compute_early = True)


def test_Derivative_at_raises():
    x = Variable("x")
    z = Logarithm(x)
    late_derivative = Derivative(z, compute_early = False)
    with raises(DomainError):
        late_derivative.at(Point(x = -1))
    early_derivative = Derivative(z, compute_early = True)
    with raises(DomainError):
        early_derivative.at(Point(x = -1))


def test_Derivative_equality():
    x = Variable("x")
    assert Derivative(x ** 2) == Derivative(x ** 2)
    assert Derivative(x ** 2) == Derivative(x ** 2, compute_early = True)
    y = Variable("y")
    assert Derivative(x ** 2) != Derivative(y ** 2)


def test_Derivative_hashing():
    x = Variable("x")
    z = x ** 2
    assert hash(Derivative(z)) == hash(Derivative(z))
    assert hash(Derivative(z)) == hash(Derivative(z, compute_early = True))
