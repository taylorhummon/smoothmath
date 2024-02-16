from pytest import approx, raises, fail
from smoothmath import DomainError, Point, Partial, Differential, LocatedDifferential
from smoothmath.expression import (
    Variable, Constant, Add, Multiply, Reciprocal, NthPower, Exponential, Logarithm
)
from smoothmath._private.base_expression.expression import get_the_single_variable_name


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
    point = Point(x = 2)
    assert z.at(point) == approx(1.25)
    assert Partial(z, x).at(point) == approx(-0.25)
    assert Partial(z, x, compute_eagerly = True).at(point) == approx(-0.25)
    assert Differential(z).component_at(x, point) == approx(-0.25)
    assert LocatedDifferential(z, point).component(x) == approx(-0.25)


def test_taking_partials_using_string_variable_name():
    x = Variable("x")
    z = x ** 2
    # at x = 3
    point = Point(x = 3)
    assert Partial(z, "x").at(point) == approx(6)
    assert Partial(z, "x", compute_eagerly = True).at(point) == approx(6)
    assert Differential(z).component_at("x", point) == approx(6)
    assert LocatedDifferential(z, point).component("x") == approx(6)
    # at x = -1
    point = Point(x = -1)
    assert Partial(z, "x").at(point) == approx(-2)
    assert Partial(z, "x", compute_eagerly = True).at(point) == approx(-2)
    assert Differential(z).component_at("x", point) == approx(-2)
    assert LocatedDifferential(z, point).component("x") == approx(-2)


def test_unrelated_variable():
    x = Variable("x")
    y = Variable("y")
    z = x ** 2
    point = Point(x = 2)
    assert z.at(point) == approx(4)
    assert Partial(z, y).at(point) == approx(0)
    assert Partial(z, y, compute_eagerly = True).at(point) == approx(0)
    assert Differential(z).component_at(y, point) == approx(0)
    assert LocatedDifferential(z, point).component(y) == approx(0)


def test_polynomial_of_one_variable():
    x = Variable("x")
    z = x * x - Constant(6) * x + Constant(4)
    point = Point(x = 2)
    assert z.at(point) == approx(-4)
    assert Partial(z, x).at(point) == approx(-2)
    assert Partial(z, x, compute_eagerly = True).at(point) == approx(-2)
    assert Differential(z).component_at(x, point) == approx(-2)
    assert LocatedDifferential(z, point).component(x) == approx(-2)


def test_polynomial_of_two_variables():
    x = Variable("x")
    y = Variable("y")
    z = x * (x + y) - Constant(5) * y ** 2
    point = Point(x = 2, y = 3)
    assert z.at(point) == approx(-35)
    assert Partial(z, x).at(point) == approx(7)
    assert Partial(z, y).at(point) == approx(-28)
    assert Partial(z, x, compute_eagerly = True).at(point) == approx(7)
    assert Partial(z, y, compute_eagerly = True).at(point) == approx(-28)
    differential = Differential(z)
    assert differential.component_at(x, point) == approx(7)
    assert differential.component_at(y, point) == approx(-28)
    located_differential = LocatedDifferential(z, point)
    assert located_differential.component(x) == approx(7)
    assert located_differential.component(y) == approx(-28)


def test_polynomial_of_three_variables():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = w * w + Constant(5) * w * x ** 2 - w * x * y
    point = Point(w = 2, x = 3, y = 4)
    assert z.at(point) == approx(70)
    assert Partial(z, w).at(point) == approx(37)
    assert Partial(z, x).at(point) == approx(52)
    assert Partial(z, y).at(point) == approx(-6)
    assert Partial(z, w, compute_eagerly = True).at(point) == approx(37)
    assert Partial(z, x, compute_eagerly = True).at(point) == approx(52)
    assert Partial(z, y, compute_eagerly = True).at(point) == approx(-6)
    differential = Differential(z)
    assert differential.component_at(w, point) == approx(37)
    assert differential.component_at(x, point) == approx(52)
    assert differential.component_at(y, point) == approx(-6)
    located_differential = LocatedDifferential(z, point)
    assert located_differential.component(w) == approx(37)
    assert located_differential.component(x) == approx(52)
    assert located_differential.component(y) == approx(-6)


def test_composite_function():
    x = Variable("x")
    z = Exponential(x ** 2)
    point = Point(x = 2)
    assert z.at(point) == approx(54.598150033)
    assert Partial(z, x).at(point) == approx(218.392600132)
    assert Partial(z, x, compute_eagerly = True).at(point) == approx(218.392600132)
    assert Differential(z).component_at(x, point) == approx(218.392600132)
    assert LocatedDifferential(z, point).component(x) == approx(218.392600132)


def test_indeterminate_form():
    t = Variable("t")
    z = (Constant(2) * t) / t
    point = Point(t = 0)
    with raises(DomainError):
        z.at(point)
    partial = Partial(z, t)
    with raises(DomainError):
        partial.at(point)
    partial = Partial(z, t, compute_eagerly = True)
    with raises(DomainError):
        partial.at(point)
    differential = Differential(z)
    with raises(DomainError):
        differential.component_at(t, point)
    with raises(DomainError):
        LocatedDifferential(z, point)


def test_consolidate_expression_lacking_variables():
    z = Multiply(NthPower(Add(Constant(2), Constant(1)), n = 2), Constant(2))
    assert z._consolidate_expression_lacking_variables() == Constant(18)
    z = Logarithm(Constant(-1))
    assert z._consolidate_expression_lacking_variables() == None


def test_get_the_single_variable_name():
    x = Variable("x")
    exception_message = "exception message"
    good = x ** 2 + Constant(3)
    assert get_the_single_variable_name(good, exception_message) == "x"
    lacking_variables = Constant(3) ** 2
    try:
        assert get_the_single_variable_name(lacking_variables, exception_message) == "whatever"
    except Exception:
        fail("getting the variable name of an expression lacking variables shouldnt fail")
    y = Variable("y")
    bad = x ** 2 + y ** 2
    with raises(Exception):
        get_the_single_variable_name(bad, exception_message)
