from __future__ import annotations
from typing import TYPE_CHECKING
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


class Negation(base.UnaryExpression):
    def __init__(
        self: Negation,
        inner: sm.Expression
    ) -> None:
        super().__init__(inner)

    def _verify_domain_constraints(
        self: Negation,
        inner_value: sm.real_number
    ) -> None:
        pass

    def _value_formula(
        self: Negation,
        inner_value: sm.real_number
    ) -> sm.real_number:
        return - inner_value

    def _local_partial(
        self: Negation,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        inner_partial = self._inner._local_partial(point, with_respect_to)
        return - inner_partial

    def _synthetic_partial(
        self: Negation,
        with_respect_to: str
    ) -> sm.Expression:
        inner_partial = self._inner._synthetic_partial(with_respect_to)
        return ex.Negation(inner_partial)

    def _compute_local_differential(
        self: Negation,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        self._inner._compute_local_differential(builder, - accumulated)

    def _compute_global_differential(
        self: Negation,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        self._inner._compute_global_differential(builder, ex.Negation(accumulated))
