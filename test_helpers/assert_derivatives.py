from pytest import approx, raises
from smoothmath import DomainError, RealNumber, Point, Expression
from smoothmath.expression import Variable


def assert_1_ary_derivatives(
    expression: Expression,
    point: Point,
    variable: Variable,
    expected: RealNumber
) -> None:
    assert expression.global_differential().component_at(variable, point) == approx(expected)
    assert expression.local_differential(point).component(variable) == approx(expected)
    assert expression.global_partial(variable).at(point) == approx(expected)
    assert expression.local_partial(variable, point) == approx(expected)


def assert_1_ary_derivatives_raise(
    expression: Expression,
    point: Point,
    variable: Variable
) -> None:
    global_differential = expression.global_differential()
    with raises(DomainError):
        global_differential.component_at(variable, point)
    with raises(DomainError):
        expression.local_differential(point)
    global_partial = expression.global_partial(variable)
    with raises(DomainError):
        global_partial.at(point)
    with raises(DomainError):
        expression.local_partial(variable, point)


def assert_2_ary_derivatives(
    expression: Expression,
    point: Point,
    variable_a: Variable,
    expected_a: RealNumber,
    variable_b: Variable,
    expected_b: RealNumber
) -> None:
    global_differential = expression.global_differential()
    assert global_differential.component_at(variable_a, point) == approx(expected_a)
    assert global_differential.component_at(variable_b, point) == approx(expected_b)
    local_differential = expression.local_differential(point)
    assert local_differential.component(variable_a) == approx(expected_a)
    assert local_differential.component(variable_b) == approx(expected_b)
    assert expression.global_partial(variable_a).at(point) == approx(expected_a)
    assert expression.global_partial(variable_b).at(point) == approx(expected_b)
    assert expression.local_partial(variable_a, point) == approx(expected_a)
    assert expression.local_partial(variable_b, point) == approx(expected_b)


def assert_2_ary_derivatives_raise(
    expression: Expression,
    point: Point,
    variable_a: Variable,
    variable_b: Variable
) -> None:
    global_differential = expression.global_differential()
    with raises(DomainError):
        global_differential.component_at(variable_a, point)
    with raises(DomainError):
        global_differential.component_at(variable_b, point)
    with raises(DomainError):
        expression.local_differential(point)
    global_partial_a = expression.global_partial(variable_a)
    with raises(DomainError):
        global_partial_a.at(point)
    global_partial_b = expression.global_partial(variable_b)
    with raises(DomainError):
        global_partial_b.at(point)
    with raises(DomainError):
        expression.local_partial(variable_a, point)
    with raises(DomainError):
        expression.local_partial(variable_b, point)


def assert_3_ary_derivatives(
    expression: Expression,
    point: Point,
    variable_a: Variable,
    expected_a: RealNumber,
    variable_b: Variable,
    expected_b: RealNumber,
    variable_c: Variable,
    expected_c: RealNumber
) -> None:
    global_differential = expression.global_differential()
    assert global_differential.component_at(variable_a, point) == approx(expected_a)
    assert global_differential.component_at(variable_b, point) == approx(expected_b)
    assert global_differential.component_at(variable_c, point) == approx(expected_c)
    local_differential = expression.local_differential(point)
    assert local_differential.component(variable_a) == approx(expected_a)
    assert local_differential.component(variable_b) == approx(expected_b)
    assert local_differential.component(variable_c) == approx(expected_c)
    assert expression.global_partial(variable_a).at(point) == approx(expected_a)
    assert expression.global_partial(variable_b).at(point) == approx(expected_b)
    assert expression.global_partial(variable_c).at(point) == approx(expected_c)
    assert expression.local_partial(variable_a, point) == approx(expected_a)
    assert expression.local_partial(variable_b, point) == approx(expected_b)
    assert expression.local_partial(variable_c, point) == approx(expected_c)
