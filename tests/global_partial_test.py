from pytest import approx, raises
from smoothmath import DomainError, Point, GlobalPartial
from smoothmath.expression import Variable, Constant, Reciprocal, NthPower, Logarithm


def test_GlobalPartial():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    original_expression = Constant(4) * w + x * y ** 3
    synthetic_y_partial = Constant(3) * x * y ** 2
    global_y_partial = GlobalPartial(original_expression, synthetic_y_partial)
    point = Point({w: 7, x: 4, y: 5})
    assert global_y_partial.at(point) == approx(300)


def test_GlobalPartial_raises():
    x = Variable("x")
    original_expression = Logarithm(x)
    synthetic_x_partial = Reciprocal(x)
    global_x_partial = GlobalPartial(original_expression, synthetic_x_partial)
    with raises(DomainError):
        global_x_partial.at(Point({x: -1}))


def test_GlobalPartial_equality():
    x = Variable("x")
    y = Variable("y")
    global_partial = GlobalPartial(NthPower(x, n = 2), Constant(2) * x)
    assert global_partial == GlobalPartial(NthPower(x, n = 2), Constant(2) * x)
    assert global_partial != GlobalPartial(NthPower(y, n = 2), Constant(2) * y)


def test_GlobalPartial_hashing():
    x = Variable("x")
    global_partial_a = GlobalPartial(NthPower(x, n = 2), Constant(2) * x)
    global_partial_b = GlobalPartial(NthPower(x, n = 2), Constant(2) * x)
    assert global_partial_a == global_partial_b
    assert hash(global_partial_a) == hash(global_partial_b)
