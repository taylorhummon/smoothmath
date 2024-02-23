from pytest import raises, fail
from smoothmath import CoordinateMissing, Point
from smoothmath.expression import Variable
from smoothmath._private.point import point_on_number_line


def test_Point():
    x = Variable("x")
    y = Variable("y")
    point = Point(x = 3, y = 4)
    assert point.coordinate(x) == 3
    assert point.coordinate(y) == 4
    assert point.coordinate("x") == 3
    assert point.coordinate("y") == 4
    point = Point(x = 5, y = 6)
    assert point.coordinate(x) == 5
    assert point.coordinate(y) == 6
    assert point.coordinate("x") == 5
    assert point.coordinate("y") == 6


def test_Point_when_missing_a_variable():
    point = Point(x = 3)
    with raises(CoordinateMissing):
        point.coordinate(Variable("y"))


def test_Point_when_no_variables_are_provided():
    try:
        Point()
    except Exception:
        fail("Creating a point with zero variables failed")


def test_Point_equality():
    assert Point(x = 3, y = 4) == Point(x = 3, y = 4)
    assert Point(x = 3, y = 4) == Point(y = 4, x = 3)
    assert Point(x = 3, y = 4) != Point(x = 4, y = 3)
    assert Point(x = 3, y = 4) != Point(x = 3)


def test_Point_hashing():
    assert hash(Point(x = 3, y = 4)) == hash(Point(x = 3, y = 4))
    assert hash(Point(x = 3, y = 4)) == hash(Point(y = 4, x = 3))


def test_point_on_number_line():
    assert point_on_number_line("x", 3) == Point(x = 3)
