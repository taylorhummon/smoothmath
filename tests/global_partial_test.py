from pytest import approx, raises
from smoothmath import Point, DomainError, GlobalPartial
from smoothmath.expression import Variable, Constant, Logarithm, Reciprocal


def test_GlobalPartial():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    original_expression = Constant(4) * w + x * y ** Constant(3)
    synthetic_y_partial = Constant(3) * x * y ** Constant(2)
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
