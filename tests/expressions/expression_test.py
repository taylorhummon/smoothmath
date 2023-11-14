from pytest import approx, raises
from smoothmath.errors import DomainError
from smoothmath.variable_values import VariableValues
from smoothmath.expressions import Constant, Variable, Exponential

def test_polynomial_of_one_variable():
    x = Variable("x")
    z = x * x - Constant(6) * x + Constant(4)
    variable_values = VariableValues({ x: 2 })
    value = z.evaluate(variable_values)
    assert value == -4
    partial = z.partial_at(variable_values, x)
    assert partial == -2
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == -2

def test_polynomial_of_two_variables():
    x = Variable("x")
    y = Variable("y")
    z = x * (x + y) - Constant(5) * y * y
    variable_values = VariableValues({ x: 2, y: 3 })
    value = z.evaluate(variable_values)
    assert value == -35
    partial_with_respect_to_x = z.partial_at(variable_values, x)
    assert partial_with_respect_to_x == 7
    partial_with_respect_to_y = z.partial_at(variable_values, y)
    assert partial_with_respect_to_y == -28
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == 7
    assert all_partials.partial_with_respect_to(y) == -28

def test_polynomial_of_three_variables():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = w * w + Constant(5) * w * x * x - w * x * y
    variable_values = VariableValues({ w: 2, x: 3, y: 4 })
    value = z.evaluate(variable_values)
    assert value == 70
    partial_with_respect_toW = z.partial_at(variable_values, w)
    assert partial_with_respect_toW == 37
    partial_with_respect_to_x = z.partial_at(variable_values, x)
    assert partial_with_respect_to_x == 52
    partial_with_respect_to_y = z.partial_at(variable_values, y)
    assert partial_with_respect_to_y == -6
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(w) == 37
    assert all_partials.partial_with_respect_to(x) == 52
    assert all_partials.partial_with_respect_to(y) == -6

def test_unrelated_variable():
    x = Variable("x")
    y = Variable("y")
    z = x ** Constant(2)
    variable_values = VariableValues({ x: 2 })
    value = z.evaluate(variable_values)
    assert value == 4
    partial = z.partial_at(variable_values, y)
    assert partial == 0
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(y) == 0

def test_composite_function():
    x = Variable("x")
    z = Exponential(x ** Constant(2))
    variable_values = VariableValues({ x: 2 })
    value = z.evaluate(variable_values)
    assert value == approx(54.598150033)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(218.392600132)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(218.392600132)

def test_indeterminate_form():
    t = Variable("t")
    z = (Constant(2) * t) / t
    variable_values = VariableValues({ t: 0 })
    with raises(DomainError):
        z.evaluate(variable_values)
    with raises(DomainError):
        z.partial_at(variable_values, t)
    with raises(DomainError):
        z.all_partials_at(variable_values)

def test_expression_reuse():
    x = Variable("x")
    w = x ** Constant(2)
    z = (w + Constant(1)) / w
    variable_values = VariableValues({ x: 2 })
    value = z.evaluate(variable_values)
    assert value == approx(1.25)
    partial = z.partial_at(variable_values, x)
    assert partial == approx(-0.25)
    all_partials = z.all_partials_at(variable_values)
    assert all_partials.partial_with_respect_to(x) == approx(-0.25)

def test_partial_at_using_variable_name():
    x = Variable("x")
    z = x ** Constant(2)
    partial = z.partial_at(VariableValues({ "x": 3 }), "x")
    assert partial == approx(6)

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
