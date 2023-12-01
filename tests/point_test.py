from pytest import raises
from smoothmath import Point
from smoothmath.expression import Variable


def test_Point():
    x = Variable("x")
    y = Variable("y")
    point = Point({x: 3, y: 4})
    assert point.value_for(x) == 3
    assert point.value_for(y) == 4
    assert point.value_for("x") == 3
    assert point.value_for("y") == 4
    point = Point({"x": 5, "y": 6})
    assert point.value_for(x) == 5
    assert point.value_for(y) == 6
    assert point.value_for("x") == 5
    assert point.value_for("y") == 6


def test_Point_when_missing_a_variable():
    x = Variable("x")
    y = Variable("y")
    point = Point({x: 3})
    with raises(Exception):
        point.value_for(y)


def test_Point_when_providing_the_same_variable_twice():
    x = Variable("x")
    y = Variable("y")
    with raises(Exception):
        Point({x: 3, y: 4, "x": 5})
