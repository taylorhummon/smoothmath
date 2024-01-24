from __future__ import annotations
from typing import TYPE_CHECKING, Callable
import math
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


class Cosine(base.UnaryExpression):
    def _verify_domain_constraints(
        self: Cosine,
        inner_value: sm.real_number
    ) -> None:
        pass

    def _value_formula(
        self: Cosine,
        inner_value: sm.real_number
    ) -> sm.real_number:
        return math.cos(inner_value)

    def _local_partial(
        self: Cosine,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        inner_partial = self._inner._local_partial(point, with_respect_to)
        return self._local_partial_formula(point, inner_partial)

    def _synthetic_partial(
        self: Cosine,
        with_respect_to: str
    ) -> sm.Expression:
        inner_partial = self._inner._synthetic_partial(with_respect_to)
        return self._synthetic_partial_formula(inner_partial)

    def _compute_local_differential(
        self: Cosine,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        next_accumulated = self._local_partial_formula(builder.point, accumulated)
        self._inner._compute_local_differential(builder, next_accumulated)

    def _compute_global_differential(
        self: Cosine,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        next_accumulated = self._synthetic_partial_formula(accumulated)
        self._inner._compute_global_differential(builder, next_accumulated)

    def _local_partial_formula(
        self: Cosine,
        point: sm.Point,
        multiplier: sm.real_number
    ) -> sm.real_number:
        inner_value = self._inner._evaluate(point)
        return - math.sin(inner_value) * multiplier

    def _synthetic_partial_formula(
        self: Cosine,
        multiplier: sm.Expression
    ) -> sm.Expression:
        return ex.Multiply(ex.Negation(ex.Sine(self._inner)), multiplier)

    @property
    def _reducers(
        self: Cosine
    ) -> list[Callable[[], sm.Expression | None]]:
        return [
            self._reduce_cosine_of_negation_of_u
        ]

    # Cosine(Negation(u)) => Cosine(u)
    def _reduce_cosine_of_negation_of_u(
        self: Cosine
    ) -> sm.Expression | None:
        if isinstance(self._inner, ex.Negation):
            return ex.Cosine(self._inner._inner)
        else:
            return None
