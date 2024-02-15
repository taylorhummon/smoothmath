from pytest import approx, raises
from smoothmath import DomainError, Point, GlobalDifferential, LocalDifferential, GlobalPartial
from smoothmath.expression import (
    Variable, Constant, Add, Multiply, Reciprocal, NthPower, Exponential, Logarithm
)


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
    assert z.evaluate(point) == approx(1.25)
    assert z.partial_at(x, point) == approx(-0.25)
    assert GlobalPartial(z, x).at(point) == approx(-0.25)
    assert LocalDifferential(z, point).component(x) == approx(-0.25)
    assert GlobalDifferential(z).component_at(x, point) == approx(-0.25)


def test_taking_partials_using_string_variable_name():
    x = Variable("x")
    z = x ** 2
    # at x = 3
    point = Point(x = 3)
    assert z.partial_at("x", point) == approx(6)
    assert GlobalPartial(z, "x").at(point) == approx(6)
    assert LocalDifferential(z, point).component("x") == approx(6)
    assert GlobalDifferential(z).component_at("x", point) == approx(6)
    # at x = -1
    point = Point(x = -1)
    assert z.partial_at("x", point) == approx(-2)
    assert GlobalPartial(z, "x").at(point) == approx(-2)
    assert LocalDifferential(z, point).component("x") == approx(-2)
    assert GlobalDifferential(z).component_at("x", point) == approx(-2)


def test_unrelated_variable():
    x = Variable("x")
    y = Variable("y")
    z = x ** 2
    point = Point(x = 2)
    assert z.evaluate(point) == approx(4)
    assert z.partial_at(y, point) == approx(0)
    assert GlobalPartial(z, y).at(point) == approx(0)
    assert LocalDifferential(z, point).component(y) == approx(0)
    assert GlobalDifferential(z).component_at(y, point) == approx(0)


def test_polynomial_of_one_variable():
    x = Variable("x")
    z = x * x - Constant(6) * x + Constant(4)
    point = Point(x = 2)
    assert z.evaluate(point) == approx(-4)
    assert z.partial_at(x, point) == approx(-2)
    assert GlobalPartial(z, x).at(point) == approx(-2)
    assert LocalDifferential(z, point).component(x) == approx(-2)
    assert GlobalDifferential(z).component_at(x, point) == approx(-2)


def test_polynomial_of_two_variables():
    x = Variable("x")
    y = Variable("y")
    z = x * (x + y) - Constant(5) * y ** 2
    point = Point(x = 2, y = 3)
    assert z.evaluate(point) == approx(-35)
    assert z.partial_at(x, point) == approx(7)
    assert z.partial_at(y, point) == approx(-28)
    assert GlobalPartial(z, x).at(point) == approx(7)
    assert GlobalPartial(z, y).at(point) == approx(-28)
    local_differential = LocalDifferential(z, point)
    assert local_differential.component(x) == approx(7)
    assert local_differential.component(y) == approx(-28)
    global_differential = GlobalDifferential(z)
    assert global_differential.component_at(x, point) == approx(7)
    assert global_differential.component_at(y, point) == approx(-28)


def test_polynomial_of_three_variables():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = w * w + Constant(5) * w * x ** 2 - w * x * y
    point = Point(w = 2, x = 3, y = 4)
    assert z.evaluate(point) == approx(70)
    assert z.partial_at(w, point) == approx(37)
    assert z.partial_at(x, point) == approx(52)
    assert z.partial_at(y, point) == approx(-6)
    assert GlobalPartial(z, w).at(point) == approx(37)
    assert GlobalPartial(z, x).at(point) == approx(52)
    assert GlobalPartial(z, y).at(point) == approx(-6)
    local_differential = LocalDifferential(z, point)
    assert local_differential.component(w) == approx(37)
    assert local_differential.component(x) == approx(52)
    assert local_differential.component(y) == approx(-6)
    global_differential = GlobalDifferential(z)
    assert global_differential.component_at(w, point) == approx(37)
    assert global_differential.component_at(x, point) == approx(52)
    assert global_differential.component_at(y, point) == approx(-6)


def test_composite_function():
    x = Variable("x")
    z = Exponential(x ** 2)
    point = Point(x = 2)
    assert z.evaluate(point) == approx(54.598150033)
    assert z.partial_at(x, point) == approx(218.392600132)
    assert GlobalPartial(z, x).at(point) == approx(218.392600132)
    assert LocalDifferential(z, point).component(x) == approx(218.392600132)
    assert GlobalDifferential(z).component_at(x, point) == approx(218.392600132)


def test_indeterminate_form():
    t = Variable("t")
    z = (Constant(2) * t) / t
    point = Point(t = 0)
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(t, point)
    global_t_partial = GlobalPartial(z, t)
    with raises(DomainError):
        global_t_partial.at(point)
    with raises(DomainError):
        LocalDifferential(z, point)
    global_differential = GlobalDifferential(z)
    with raises(DomainError):
        global_differential.component_at(t, point)


def test_consolidate_expression_lacking_variables():
    z = Multiply(NthPower(Add(Constant(2), Constant(1)), n = 2), Constant(2))
    assert z._consolidate_expression_lacking_variables() == Constant(18)
    z = Logarithm(Constant(-1))
    assert z._consolidate_expression_lacking_variables() == None
