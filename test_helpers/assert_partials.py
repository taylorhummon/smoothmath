from pytest import approx, raises
from smoothmath import DomainError, RealNumber, Point, Expression
from smoothmath.expression import Variable
import smoothmath._private.expression.variable as va


def assert_1_ary_partials(
    expression: Expression,
    point: Point,
    variable: Variable,
    expected: RealNumber
) -> None:
    variable_name = va.get_variable_name(variable)
    assert expression._numeric_partial(variable_name, point) == approx(expected)
    assert expression._synthetic_partial(variable_name).at(point) == approx(expected)
    assert expression._numeric_partials(point)[variable_name] == approx(expected)
    assert expression._synthetic_partials()[variable_name].at(point) == approx(expected)


def assert_1_ary_partials_raise(
    expression: Expression,
    point: Point,
    variable: Variable
) -> None:
    variable_name = va.get_variable_name(variable)
    with raises(DomainError):
        expression._numeric_partial(variable_name, point)
    with raises(DomainError):
        expression._numeric_partials(point)


def assert_2_ary_partials(
    expression: Expression,
    point: Point,
    variable_a: Variable,
    expected_a: RealNumber,
    variable_b: Variable,
    expected_b: RealNumber
) -> None:
    variable_name_a = va.get_variable_name(variable_a)
    variable_name_b = va.get_variable_name(variable_b)
    assert expression._numeric_partial(variable_name_a, point) == approx(expected_a)
    assert expression._numeric_partial(variable_name_b, point) == approx(expected_b)
    assert expression._synthetic_partial(variable_name_a).at(point) == approx(expected_a)
    assert expression._synthetic_partial(variable_name_b).at(point) == approx(expected_b)
    numeric_partials = expression._numeric_partials(point)
    assert numeric_partials[variable_name_a] == approx(expected_a)
    assert numeric_partials[variable_name_b] == approx(expected_b)
    synthetic_partials = expression._synthetic_partials()
    assert synthetic_partials[variable_name_a].at(point) == approx(expected_a)
    assert synthetic_partials[variable_name_b].at(point) == approx(expected_b)


def assert_2_ary_partials_raise(
    expression: Expression,
    point: Point,
    variable_a: Variable,
    variable_b: Variable
) -> None:
    variable_name_a = va.get_variable_name(variable_a)
    variable_name_b = va.get_variable_name(variable_b)
    with raises(DomainError):
        expression._numeric_partial(variable_name_a, point)
    with raises(DomainError):
        expression._numeric_partial(variable_name_b, point)
    with raises(DomainError):
        expression._numeric_partials(point)


def assert_3_ary_partials(
    expression: Expression,
    point: Point,
    variable_a: Variable,
    expected_a: RealNumber,
    variable_b: Variable,
    expected_b: RealNumber,
    variable_c: Variable,
    expected_c: RealNumber
) -> None:
    variable_name_a = va.get_variable_name(variable_a)
    variable_name_b = va.get_variable_name(variable_b)
    variable_name_c = va.get_variable_name(variable_c)
    assert expression._numeric_partial(variable_name_a, point) == approx(expected_a)
    assert expression._numeric_partial(variable_name_b, point) == approx(expected_b)
    assert expression._numeric_partial(variable_name_c, point) == approx(expected_c)
    assert expression._synthetic_partial(variable_name_a).at(point) == approx(expected_a)
    assert expression._synthetic_partial(variable_name_b).at(point) == approx(expected_b)
    assert expression._synthetic_partial(variable_name_c).at(point) == approx(expected_c)
    numeric_partials = expression._numeric_partials(point)
    assert numeric_partials[variable_name_a] == approx(expected_a)
    assert numeric_partials[variable_name_b] == approx(expected_b)
    assert numeric_partials[variable_name_c] == approx(expected_c)
    synthetic_partials = expression._synthetic_partials()
    assert synthetic_partials[variable_name_a].at(point) == approx(expected_a)
    assert synthetic_partials[variable_name_b].at(point) == approx(expected_b)
    assert synthetic_partials[variable_name_c].at(point) == approx(expected_c)
