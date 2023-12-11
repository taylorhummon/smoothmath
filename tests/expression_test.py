from pytest import approx, raises
import math
from smoothmath import DomainError, Point
from smoothmath.expression import Constant, Variable, Reciprocal, Exponential, Multiply


def test_unary_expression_equality():
    x = Variable("x")
    y = Variable("y")
    assert Reciprocal(x) == Reciprocal(x)
    assert Reciprocal(x) != Reciprocal(y)


def test_binary_expression_equality():
    x = Variable("x")
    y = Variable("y")
    assert Multiply(x, y) == Multiply(x, y)
    assert Multiply(x, y) != Multiply(y, x)


def test_expression_reuse():
    x = Variable("x")
    w = x ** 2
    z = (w + Constant(1)) / w
    point = Point({x: 2})
    assert z.evaluate(point) == approx(1.25)
    assert z.local_partial(point, x) == approx(-0.25)
    assert z.global_partial(x).at(point) == approx(-0.25)
    assert z.local_differential(point).component(x) == approx(-0.25)
    assert z.global_differential().component_at(point, x) == approx(-0.25)


def test_taking_partials_using_string_variable_name():
    x = Variable("x")
    z = x ** 2
    global_x_partial = z.global_partial("x")
    global_differential = z.global_differential()
    # at x = 3
    point = Point({x: 3})
    assert z.local_partial(point, "x") == approx(6)
    assert global_x_partial.at(point) == approx(6)
    assert z.local_differential(point).component("x") == approx(6)
    assert global_differential.component_at(point, "x") == approx(6)
    # at x = -1
    point = Point({"x": -1})
    assert z.local_partial(point, "x") == approx(-2)
    assert global_x_partial.at(point) == approx(-2)
    assert z.local_differential(point).component("x") == approx(-2)
    assert global_differential.component_at(point, "x") == approx(-2)


def test_unrelated_variable():
    x = Variable("x")
    y = Variable("y")
    z = x ** 2
    point = Point({x: 2})
    assert z.evaluate(point) == approx(4)
    assert z.local_partial(point, y) == approx(0)
    assert z.global_partial(y).at(point) == approx(0)
    assert z.local_differential(point).component(y) == approx(0)
    assert z.global_differential().component_at(point, y) == approx(0)


def test_polynomial_of_one_variable():
    x = Variable("x")
    z = x * x - Constant(6) * x + Constant(4)
    point = Point({x: 2})
    assert z.evaluate(point) == approx(-4)
    assert z.local_partial(point, x) == approx(-2)
    assert z.global_partial(x).at(point) == approx(-2)
    assert z.local_differential(point).component(x) == approx(-2)
    assert z.global_differential().component_at(point, x) == approx(-2)


def test_polynomial_of_two_variables():
    x = Variable("x")
    y = Variable("y")
    z = x * (x + y) - Constant(5) * y ** 2
    point = Point({x: 2, y: 3})
    assert z.evaluate(point) == approx(-35)
    assert z.local_partial(point, x) == approx(7)
    assert z.local_partial(point, y) == approx(-28)
    assert z.global_partial(x).at(point) == approx(7)
    assert z.global_partial(y).at(point) == approx(-28)
    local_differential = z.local_differential(point)
    assert local_differential.component(x) == approx(7)
    assert local_differential.component(y) == approx(-28)
    global_differential = z.global_differential()
    assert global_differential.component_at(point, x) == approx(7)
    assert global_differential.component_at(point, y) == approx(-28)


def test_polynomial_of_three_variables():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = w * w + Constant(5) * w * x ** 2 - w * x * y
    point = Point({w: 2, x: 3, y: 4})
    assert z.evaluate(point) == approx(70)
    assert z.local_partial(point, w) == approx(37)
    assert z.local_partial(point, x) == approx(52)
    assert z.local_partial(point, y) == approx(-6)
    assert z.global_partial(w).at(point) == approx(37)
    assert z.global_partial(x).at(point) == approx(52)
    assert z.global_partial(y).at(point) == approx(-6)
    local_differential = z.local_differential(point)
    assert local_differential.component(w) == approx(37)
    assert local_differential.component(x) == approx(52)
    assert local_differential.component(y) == approx(-6)
    global_differential = z.global_differential()
    assert global_differential.component_at(point, w) == approx(37)
    assert global_differential.component_at(point, x) == approx(52)
    assert global_differential.component_at(point, y) == approx(-6)


def test_composite_function():
    x = Variable("x")
    z = Exponential(math.e, x ** 2)
    point = Point({x: 2})
    assert z.evaluate(point) == approx(54.598150033)
    assert z.local_partial(point, x) == approx(218.392600132)
    assert z.global_partial(x).at(point) == approx(218.392600132)
    assert z.local_differential(point).component(x) == approx(218.392600132)
    assert z.global_differential().component_at(point, x) == approx(218.392600132)


def test_indeterminate_form():
    t = Variable("t")
    z = (Constant(2) * t) / t
    point = Point({t: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.local_partial(point, t)
    global_t_partial = z.global_partial(t)
    with raises(DomainError):
        global_t_partial.at(point)
    with raises(DomainError):
        z.local_differential(point)
    global_differential = z.global_differential()
    with raises(DomainError):
        global_differential.component_at(point, t)
