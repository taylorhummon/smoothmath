from pytest import approx, raises
from smoothmath import (
    DomainError, RealNumber, Point, Expression, Partial, Differential, LocatedDifferential
)
from smoothmath.expression import Variable


def assert_1_ary_derivatives(
    expression: Expression,
    point: Point,
    variable: Variable,
    expected: RealNumber
) -> None:
    assert Partial(expression, variable).at(point) == approx(expected)
    assert Partial(expression, variable, compute_eagerly = True).at(point) == approx(expected)
    assert Differential(expression).component_at(variable, point) == approx(expected)
    assert LocatedDifferential(expression, point).component(variable) == approx(expected)


def assert_1_ary_derivatives_raise(
    expression: Expression,
    point: Point,
    variable: Variable
) -> None:
    partial = Partial(expression, variable)
    with raises(DomainError):
        partial.at(point)
    partial = Partial(expression, variable, compute_eagerly=True)
    with raises(DomainError):
        partial.at(point)
    differential = Differential(expression)
    with raises(DomainError):
        differential.component_at(variable, point)
    with raises(DomainError):
        LocatedDifferential(expression, point)


def assert_2_ary_derivatives(
    expression: Expression,
    point: Point,
    variable_a: Variable,
    expected_a: RealNumber,
    variable_b: Variable,
    expected_b: RealNumber
) -> None:
    assert Partial(expression, variable_a).at(point) == approx(expected_a)
    assert Partial(expression, variable_b).at(point) == approx(expected_b)
    assert Partial(expression, variable_a, compute_eagerly = True).at(point) == approx(expected_a)
    assert Partial(expression, variable_b, compute_eagerly = True).at(point) == approx(expected_b)
    differential = Differential(expression)
    assert differential.component_at(variable_a, point) == approx(expected_a)
    assert differential.component_at(variable_b, point) == approx(expected_b)
    located_differential = LocatedDifferential(expression, point)
    assert located_differential.component(variable_a) == approx(expected_a)
    assert located_differential.component(variable_b) == approx(expected_b)


def assert_2_ary_derivatives_raise(
    expression: Expression,
    point: Point,
    variable_a: Variable,
    variable_b: Variable
) -> None:
    partial_a = Partial(expression, variable_a)
    with raises(DomainError):
        partial_a.at(point)
    partial_b = Partial(expression, variable_b)
    with raises(DomainError):
        partial_b.at(point)
    partial_a = Partial(expression, variable_a, compute_eagerly = True)
    with raises(DomainError):
        partial_a.at(point)
    partial_b = Partial(expression, variable_b, compute_eagerly = True)
    with raises(DomainError):
        partial_b.at(point)
    differential = Differential(expression)
    with raises(DomainError):
        differential.component_at(variable_a, point)
    with raises(DomainError):
        differential.component_at(variable_b, point)
    with raises(DomainError):
        LocatedDifferential(expression, point)


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
    assert Partial(expression, variable_a).at(point) == approx(expected_a)
    assert Partial(expression, variable_b).at(point) == approx(expected_b)
    assert Partial(expression, variable_c).at(point) == approx(expected_c)
    assert Partial(expression, variable_a, compute_eagerly = True).at(point) == approx(expected_a)
    assert Partial(expression, variable_b, compute_eagerly = True).at(point) == approx(expected_b)
    assert Partial(expression, variable_c, compute_eagerly = True).at(point) == approx(expected_c)
    differential = Differential(expression)
    assert differential.component_at(variable_a, point) == approx(expected_a)
    assert differential.component_at(variable_b, point) == approx(expected_b)
    assert differential.component_at(variable_c, point) == approx(expected_c)
    located_differential = LocatedDifferential(expression, point)
    assert located_differential.component(variable_a) == approx(expected_a)
    assert located_differential.component(variable_b) == approx(expected_b)
    assert located_differential.component(variable_c) == approx(expected_c)
