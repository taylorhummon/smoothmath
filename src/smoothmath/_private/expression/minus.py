from __future__ import annotations
from typing import TYPE_CHECKING, Callable
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


class Minus(base.BinaryExpression):
    def _verify_domain_constraints(
        self: Minus,
        left_value: sm.real_number,
        right_value: sm.real_number
    ) -> None:
        pass

    def _value_formula(
        self: Minus,
        left_value: sm.real_number,
        right_value: sm.real_number
    ) -> sm.real_number:
        return left_value - right_value

    def _local_partial(
        self: Minus,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        left_partial = self._left._local_partial(point, with_respect_to)
        right_partial = self._right._local_partial(point, with_respect_to)
        return left_partial - right_partial

    def _synthetic_partial(
        self: Minus,
        with_respect_to: str
    ) -> sm.Expression:
        left_partial = self._left._synthetic_partial(with_respect_to)
        right_partial = self._right._synthetic_partial(with_respect_to)
        return ex.Minus(left_partial, right_partial)

    def _compute_local_differential(
        self: Minus,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        self._left._compute_local_differential(builder, accumulated)
        self._right._compute_local_differential(builder, - accumulated)

    def _compute_global_differential(
        self: Minus,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        self._left._compute_global_differential(builder, accumulated)
        self._right._compute_global_differential(builder, ex.Negation(accumulated))

    @property
    def _reducers(
        self: Minus
    ) -> list[Callable[[], sm.Expression | None]]:
        return []
