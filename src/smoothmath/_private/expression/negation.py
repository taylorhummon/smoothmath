from __future__ import annotations
from typing import TYPE_CHECKING
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


# differential rule: d(-a) = -da

class Negation(base.UnaryExpression):
    def __init__(
        self: Negation,
        a: sm.Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Negation,
        point: sm.Point
    ) -> sm.real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(point)
        self._value = - a_value
        return self._value

    def _local_partial(
        self: Negation,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        a_partial = self._a._local_partial(point, with_respect_to)
        return - a_partial

    def _synthetic_partial(
        self: Negation,
        with_respect_to: str
    ) -> sm.Expression:
        a_partial = self._a._synthetic_partial(with_respect_to)
        return ex.Negation(a_partial)

    def _compute_local_differential(
        self: Negation,
        builder: LocalDifferentialBuilder,
        point: sm.Point,
        accumulated: sm.real_number
    ) -> None:
        self._a._compute_local_differential(builder, point, - accumulated)

    def _compute_global_differential(
        self: Negation,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        self._a._compute_global_differential(builder, ex.Negation(accumulated))
