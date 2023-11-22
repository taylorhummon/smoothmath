from pytest import approx, raises
from smoothmath.errors import DomainError
from smoothmath.variable_values import VariableValues
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
    variable_values = VariableValues({x: 2})
    assert z.evaluate(variable_values) == approx(1.25)
    assert z.partial_at(variable_values, x) == approx(-0.25)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(-0.25)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(-0.25)


def test_taking_partials_using_string_variable_name():
    x = Variable("x")
    z = x ** Constant(2)
    variable_values = VariableValues({"x": 3})
    assert z.partial_at(variable_values, "x") == approx(6)
    assert z.synthetic_partial("x").evaluate(variable_values) == approx(6)


def test_unrelated_variable():
    x = Variable("x")
    y = Variable("y")
    z = x ** Constant(2)
    variable_values = VariableValues({x: 2})
    assert z.evaluate(variable_values) == approx(4)
    assert z.partial_at(variable_values, y) == approx(0)
    assert z.all_partials_at(variable_values).partial_with_respect_to(y) == approx(0)
    assert z.synthetic_partial(y).evaluate(variable_values) == approx(0)


def test_polynomial_of_one_variable():
    x = Variable("x")
    z = x * x - Constant(6) * x + Constant(4)
    variable_values = VariableValues({x: 2})
    assert z.evaluate(variable_values) == approx(-4)
    assert z.partial_at(variable_values, x) == approx(-2)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(-2)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(-2)


def test_polynomial_of_two_variables():
    x = Variable("x")
    y = Variable("y")
    z = x * (x + y) - Constant(5) * y * y
    variable_values = VariableValues({x: 2, y: 3})
    assert z.evaluate(variable_values) == approx(-35)
    assert z.partial_at(variable_values, x) == approx(7)
    assert z.partial_at(variable_values, y) == approx(-28)
    both_partials = z.all_partials_at(variable_values)
    assert both_partials.partial_with_respect_to(x) == approx(7)
    assert both_partials.partial_with_respect_to(y) == approx(-28)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(7)
    assert z.synthetic_partial(y).evaluate(variable_values) == approx(-28)


def test_polynomial_of_three_variables():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = w * w + Constant(5) * w * x * x - w * x * y
    variable_values = VariableValues({w: 2, x: 3, y: 4})
    assert z.evaluate(variable_values) == approx(70)
    assert z.partial_at(variable_values, w) == approx(37)
    assert z.partial_at(variable_values, x) == approx(52)
    assert z.partial_at(variable_values, y) == approx(-6)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(w) == approx(37)
    assert all_partials.partial_with_respect_to(x) == approx(52)
    assert all_partials.partial_with_respect_to(y) == approx(-6)
    assert z.synthetic_partial(w).evaluate(variable_values) == approx(37)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(52)
    assert z.synthetic_partial(y).evaluate(variable_values) == approx(-6)


def test_composite_function():
    x = Variable("x")
    z = Exponential(x ** Constant(2))
    variable_values = VariableValues({x: 2})
    assert z.evaluate(variable_values) == approx(54.598150033)
    assert z.partial_at(variable_values, x) == approx(218.392600132)
    assert z.all_partials_at(variable_values).partial_with_respect_to(x) == approx(218.392600132)
    assert z.synthetic_partial(x).evaluate(variable_values) == approx(218.392600132)


def test_indeterminate_form():
    t = Variable("t")
    z = (Constant(2) * t) / t
    variable_values = VariableValues({t: 0})
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, t)
    with raises(DomainError):
        z.all_partials_at(variable_values)
    with raises(DomainError):
        z.synthetic_partial(t).evaluate(variable_values)
