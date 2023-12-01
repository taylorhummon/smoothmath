from pytest import approx, raises
from smoothmath import DomainError, Point
from smoothmath.expression import Constant, Variable, Logarithm, Divide


def test_Divide():
    x = Variable("x")
    y = Variable("y")
    z = Divide(x, y)
    global_x_partial = z.global_partial(x)
    global_y_partial = z.global_partial(y)
    global_differential = z.global_differential()
    # at (x, y) = (5, 2)
    point = Point({x: 5, y: 2})
    assert z.evaluate(point) == approx(2.5)
    assert z.local_partial(point, x) == approx(0.5)
    assert z.local_partial(point, y) == approx(-1.25)
    assert global_x_partial.at(point) == approx(0.5)
    assert global_y_partial.at(point) == approx(-1.25)
    local_differential = z.local_differential(point)
    assert local_differential.component(x) == approx(0.5)
    assert local_differential.component(y) == approx(-1.25)
    assert global_differential.component_at(point, x) == approx(0.5)
    assert global_differential.component_at(point, y) == approx(-1.25)
    # at (x, y) = (3, 0)
    point = Point({x: 3, y: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, x)
    with raises(DomainError):
        z.local_partial(point, y)
    with raises(DomainError):
        global_x_partial.at(point)
    with raises(DomainError):
        global_y_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    with raises(DomainError):
        global_differential.component_at(point, x)
    with raises(DomainError):
        global_differential.component_at(point, y)
    # at (x, y) = (0, 0)
    point = Point({x: 0, y: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, x)
    with raises(DomainError):
        z.local_partial(point, y)
    with raises(DomainError):
        global_x_partial.at(point)
    with raises(DomainError):
        global_y_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    with raises(DomainError):
        global_differential.component_at(point, x)
    with raises(DomainError):
        global_differential.component_at(point, y)


def test_Divide_composition():
    x = Variable("x")
    y = Variable("y")
    z = Divide(Constant(2) * x + Constant(4), Constant(5) * y)
    point = Point({x: 3, y: 1})
    assert z.evaluate(point) == approx(2)
    assert z.local_partial(point, x) == approx(0.4)
    assert z.local_partial(point, y) == approx(-2)
    assert z.global_partial(x).at(point) == approx(0.4)
    assert z.global_partial(y).at(point) == approx(-2)
    local_differential = z.local_differential(point)
    assert local_differential.component(x) == approx(0.4)
    assert local_differential.component(y) == approx(-2)
    global_differential = z.global_differential()
    assert global_differential.component_at(point, x) == approx(0.4)
    assert global_differential.component_at(point, y) == approx(-2)


def test_Divide_with_constant_numerator_zero():
    y = Variable("y")
    z = Divide(Constant(0), y)
    global_y_partial = z.global_partial(y)
    global_differential = z.global_differential()
    # at y = 3
    point = Point({y: 3})
    assert z.evaluate(point) == approx(0)
    assert z.local_partial(point, y) == approx(0)
    assert global_y_partial.at(point) == approx(0)
    assert z.local_differential(point).component(y) == approx(0)
    assert global_differential.component_at(point, y) == approx(0)
    # at y = 0
    point = Point({y: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, y)
    with raises(DomainError):
        global_y_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    with raises(DomainError):
        global_differential.component_at(point, y)


def test_Divide_with_constant_numerator_zero_composition():
    y = Variable("y")
    z = Divide(Constant(0), Constant(2) * y + Constant(4))
    point = Point({y: 3})
    assert z.evaluate(point) == approx(0)
    assert z.local_partial(point, y) == approx(0)
    assert z.global_partial(y).at(point) == approx(0)
    assert z.local_differential(point).component(y) == approx(0)
    assert z.global_differential().component_at(point, y) == approx(0)


def test_Divide_with_constant_numerator_zero_doesnt_short_circuit():
    y = Variable("y")
    z = Divide(Constant(0), Logarithm(y))
    point = Point({y: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, y)
    global_y_partial = z.global_partial(y)
    with raises(DomainError):
        global_y_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    global_differential = z.global_differential()
    with raises(DomainError):
        global_differential.component_at(point, y)


def test_Divide_with_constant_denominator_one():
    x = Variable("x")
    z = Divide(x, Constant(1))
    global_x_partial = z.global_partial(x)
    global_differential = z.global_differential()
    # at x = 3
    point = Point({x: 3})
    assert z.evaluate(point) == approx(3)
    assert z.local_partial(point, x) == approx(1)
    assert global_x_partial.at(point) == approx(1)
    assert z.local_differential(point).component(x) == approx(1)
    assert global_differential.component_at(point, x) == approx(1)
    # at x = 0
    point = Point({x: 0})
    assert z.evaluate(point) == approx(0)
    assert z.local_partial(point, x) == approx(1)
    assert global_x_partial.at(point) == approx(1)
    assert z.local_differential(point).component(x) == approx(1)
    assert global_differential.component_at(point, x) == approx(1)


def test_divide_with_constant_denominator_zero():
    x = Variable("x")
    z = Divide(x, Constant(0))
    global_x_partial = z.global_partial(x)
    global_differential = z.global_differential()
    # at x = 3
    point = Point({x: 3})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, x)
    with raises(DomainError):
        global_x_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    with raises(DomainError):
        global_differential.component_at(point, x)
    # at x = 0
    point = Point({x: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, x)
    with raises(DomainError):
        global_x_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    with raises(DomainError):
        global_differential.component_at(point, x)
