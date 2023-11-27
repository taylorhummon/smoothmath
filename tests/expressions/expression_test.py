from pytest import approx, raises
from smoothmath.errors import DomainError
from smoothmath.point import Point
from smoothmath.expressions import Constant, Variable, Exponential


def test_equality():
    c = Constant(7)
    assert c == c
    assert c == Constant(7)
    assert c == Constant(7.0)
    assert c != Constant(8)
    x = Variable("x")
    assert x == x
    assert x != Variable("y")
    assert x == Variable("x")
    assert x != c
    z = x ** c
    assert z == z
    assert z == x ** c
    assert z != c
    assert z != x
    assert z != x ** c + Constant(1)


def test_expression_reuse():
    x = Variable("x")
    w = x ** Constant(2)
    z = (w + Constant(1)) / w
    point = Point({x: 2})
    assert z.evaluate(point) == approx(1.25)
    assert z.partial_at(point, x) == approx(-0.25)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(-0.25)
    assert z.compute_global_partials().partial_at(point, x) == approx(-0.25)


def test_taking_partials_using_string_variable_name():
    x = Variable("x")
    z = x ** Constant(2)
    point = Point({"x": 3})
    assert z.partial_at(point, "x") == approx(6)
    assert z.compute_global_partials().partial_at(point, x) == approx(6)


def test_unrelated_variable():
    x = Variable("x")
    y = Variable("y")
    z = x ** Constant(2)
    point = Point({x: 2})
    assert z.evaluate(point) == approx(4)
    assert z.partial_at(point, y) == approx(0)
    assert z.compute_local_partials(point).partial_with_respect_to(y) == approx(0)
    assert z.compute_global_partials().partial_at(point, y) == approx(0)


def test_polynomial_of_one_variable():
    x = Variable("x")
    z = x * x - Constant(6) * x + Constant(4)
    point = Point({x: 2})
    assert z.evaluate(point) == approx(-4)
    assert z.partial_at(point, x) == approx(-2)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(-2)
    assert z.compute_global_partials().partial_at(point, x) == approx(-2)


def test_polynomial_of_two_variables():
    x = Variable("x")
    y = Variable("y")
    z = x * (x + y) - Constant(5) * y * y
    point = Point({x: 2, y: 3})
    assert z.evaluate(point) == approx(-35)
    assert z.partial_at(point, x) == approx(7)
    assert z.partial_at(point, y) == approx(-28)
    local_differential = z.compute_local_partials(point)
    assert local_differential.partial_with_respect_to(x) == approx(7)
    assert local_differential.partial_with_respect_to(y) == approx(-28)
    global_differential = z.compute_global_partials()
    assert global_differential.partial_at(point, x) == approx(7)
    assert global_differential.partial_at(point, y) == approx(-28)


def test_polynomial_of_three_variables():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = w * w + Constant(5) * w * x * x - w * x * y
    point = Point({w: 2, x: 3, y: 4})
    assert z.evaluate(point) == approx(70)
    assert z.partial_at(point, w) == approx(37)
    assert z.partial_at(point, x) == approx(52)
    assert z.partial_at(point, y) == approx(-6)
    local_differential = z.compute_local_partials(point)
    assert local_differential.partial_with_respect_to(w) == approx(37)
    assert local_differential.partial_with_respect_to(x) == approx(52)
    assert local_differential.partial_with_respect_to(y) == approx(-6)
    global_differential = z.compute_global_partials()
    assert global_differential.partial_at(point, w) == approx(37)
    assert global_differential.partial_at(point, x) == approx(52)
    assert global_differential.partial_at(point, y) == approx(-6)


def test_composite_function():
    x = Variable("x")
    z = Exponential(x ** Constant(2))
    point = Point({x: 2})
    assert z.evaluate(point) == approx(54.598150033)
    assert z.partial_at(point, x) == approx(218.392600132)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(218.392600132)
    assert z.compute_global_partials().partial_at(point, x) == approx(218.392600132)


def test_indeterminate_form():
    t = Variable("t")
    z = (Constant(2) * t) / t
    point = Point({t: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, t)
    with raises(DomainError):
        z.compute_local_partials(point)
    global_differential = z.compute_global_partials()
    with raises(DomainError):
        global_differential.partial_at(point, t)
