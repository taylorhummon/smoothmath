from pytest import approx, raises
from smoothmath import DomainError, Point, GlobalPartial
from smoothmath.expression import Variable, Constant, Multiply, Logarithm


def test_GlobalPartial():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = Constant(4) * w + x * y ** 3
    global_y_partial = GlobalPartial(z, y)
    point = Point(w = 7, x = 4, y = 5)
    assert global_y_partial.at(point) == approx(300)
    assert global_y_partial.at(point) == approx(300)
    synthetic_y_partial = global_y_partial.as_expression()
    assert synthetic_y_partial == Multiply(Constant(3), y ** 2, x)


def test_GlobalPartial_raises():
    x = Variable("x")
    z = Logarithm(x)
    global_x_partial = GlobalPartial(z, x)
    with raises(DomainError):
        global_x_partial.at(Point(x = -1))


def test_GlobalPartial_equality():
    x = Variable("x")
    y = Variable("y")
    z = x ** 2 + y ** 2
    assert GlobalPartial(z, x) == GlobalPartial(z, x)
    assert GlobalPartial(z, x) != GlobalPartial(z, y)


def test_GlobalPartial_hashing():
    x = Variable("x")
    y = Variable("y")
    z = x ** 2 + y ** 2
    assert hash(GlobalPartial(z, x)) == hash(GlobalPartial(z, x))
