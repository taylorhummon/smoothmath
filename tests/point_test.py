from pytest import raises
from smoothmath import Point
from smoothmath.expression import Variable


def test_Point():
    x = Variable("x")
    y = Variable("y")
    point = Point({x: 3, y: 4})
    assert point.coordinate(x) == 3
    assert point.coordinate(y) == 4
    assert point.coordinate("x") == 3
    assert point.coordinate("y") == 4
    point = Point({"x": 5, "y": 6})
    assert point.coordinate(x) == 5
    assert point.coordinate(y) == 6
    assert point.coordinate("x") == 5
    assert point.coordinate("y") == 6


def test_Point_when_missing_a_variable():
    x = Variable("x")
    y = Variable("y")
    point = Point({x: 3})
    with raises(Exception):
        point.coordinate(y)


def test_Point_when_providing_the_same_variable_twice():
    x = Variable("x")
    y = Variable("y")
    with raises(Exception):
        Point({x: 3, y: 4, "x": 5})


def test_Point_equality():
    x = Variable("x")
    y = Variable("y")
    assert Point({x: 3, y: 4}) == Point({x: 3, y: 4})
    assert Point({x: 3, y: 4}) == Point({y: 4, x: 3})
    assert Point({x: 3, y: 4}) != Point({x: 4, y: 3})
    assert Point({x: 3, y: 4}) != Point({x: 3})


def test_Point_hashing():
    x = Variable("x")
    y = Variable("y")
    assert hash(Point({x: 3, y: 4})) == hash(Point({x: 3, y: 4}))
    assert hash(Point({x: 3, y: 4})) == hash(Point({y: 4, x: 3}))
