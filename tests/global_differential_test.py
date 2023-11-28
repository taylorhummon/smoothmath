from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.expression import Expression

from pytest import approx, raises
from smoothmath.errors import DomainError
from smoothmath.point import Point
from smoothmath.expressions import Variable, Constant, Logarithm, Reciprocal
from smoothmath.global_partial import GlobalPartial
from smoothmath.local_differential import LocalDifferential
from smoothmath.global_differential import GlobalDifferential


def desired_local_differential(
    original_expression: Expression
) -> LocalDifferential:
    local_differential = LocalDifferential(original_expression)
    local_differential._add_to("w", 4)
    local_differential._add_to("x", 125)
    local_differential._add_to("y", 300)
    local_differential._freeze()
    return local_differential


def test_GlobalDifferential():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    original_expression = Constant(4) * w + x * y ** Constant(3)
    synthetic_w_partial = Constant(4)
    synthetic_x_partial = y ** Constant(3)
    synthetic_y_partial = Constant(3) * x * y ** Constant(2)
    global_differential = GlobalDifferential(original_expression)
    global_differential._add_to(w, synthetic_w_partial)
    global_differential._add_to(x, synthetic_x_partial)
    global_differential._add_to(y, synthetic_y_partial)
    global_differential._freeze()
    point = Point({w: 7, x: 4, y: 5})
    # component_at() method
    assert global_differential.component_at(point, w) == approx(4)
    assert global_differential.component_at(point, x) == approx(125)
    assert global_differential.component_at(point, y) == approx(300)
    # component() method
    global_w_partial = global_differential.component(w)
    global_x_partial = global_differential.component(x)
    global_y_partial = global_differential.component(y)
    assert global_differential.component(w).at(point) == approx(4)
    assert global_differential.component(x).at(point) == approx(125)
    assert global_differential.component(y).at(point) == approx(300)
    assert global_w_partial.original_expression == original_expression
    assert global_x_partial.original_expression == original_expression
    assert global_y_partial.original_expression == original_expression
    assert global_w_partial == GlobalPartial(original_expression, synthetic_w_partial)
    assert global_x_partial == GlobalPartial(original_expression, synthetic_x_partial)
    assert global_y_partial == GlobalPartial(original_expression, synthetic_y_partial)
    # at() method
    local_differential = global_differential.at(point)
    assert local_differential.component(w) == approx(4)
    assert local_differential.component(x) == approx(125)
    assert local_differential.component(y) == approx(300)
    assert local_differential.original_expression == original_expression
    assert local_differential == desired_local_differential(original_expression)


def test_GlobalDifferential_raises():
    x = Variable("x")
    original_expression = Logarithm(x)
    synthetic_x_partial = Reciprocal(x)
    global_differential = GlobalDifferential(original_expression)
    global_differential._add_to(x, synthetic_x_partial)
    global_differential._freeze()
    point = Point({x: -1})
    with raises(DomainError):
        global_differential.component_at(point, x)
    global_x_partial = global_differential.component(x)
    with raises(DomainError):
        global_x_partial.at(point)
    with raises(DomainError):
        global_differential.at(point)
