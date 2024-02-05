from __future__ import annotations
from typing import TYPE_CHECKING, Callable
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.base_expression as base
from smoothmath._private.math_functions import cosine, sine, multiply
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


class Sine(base.UnaryExpression):

    ## Evaluation ##

    def _verify_domain_constraints(
        self: Sine,
        inner_value: sm.real_number
    ) -> None:
        pass

    def _value_formula(
        self: Sine,
        inner_value: sm.real_number
    ) -> sm.real_number:
        return sine(inner_value)

    ## Partials and Differentials ##

    def _local_partial(
        self: Sine,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        inner_partial = self._inner._local_partial(point, with_respect_to)
        return self._local_partial_formula(point, inner_partial)

    def _synthetic_partial(
        self: Sine,
        with_respect_to: str
    ) -> sm.Expression:
        inner_partial = self._inner._synthetic_partial(with_respect_to)
        return self._synthetic_partial_formula(inner_partial)

    def _compute_local_differential(
        self: Sine,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        next_accumulated = self._local_partial_formula(builder.point, accumulated)
        self._inner._compute_local_differential(builder, next_accumulated)

    def _compute_global_differential(
        self: Sine,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        next_accumulated = self._synthetic_partial_formula(accumulated)
        self._inner._compute_global_differential(builder, next_accumulated)

    def _local_partial_formula(
        self: Sine,
        point: sm.Point,
        multiplier: sm.real_number
    ) -> sm.real_number:
        inner_value = self._inner._evaluate(point)
        return multiply(cosine(inner_value), multiplier)

    def _synthetic_partial_formula(
        self: Sine,
        multiplier: sm.Expression
    ) -> sm.Expression:
        return ex.Multiply(ex.Cosine(self._inner), multiplier)

    ## Normalization and Reduction ##

    @property
    def _reducers(
        self: Sine
    ) -> list[Callable[[], sm.Expression | None]]:
        return [self._reduce_sine_of_negation_of_u]

    # Sine(Negation(u)) => Negation(Sine(u))
    def _reduce_sine_of_negation_of_u(
        self: Sine
    ) -> sm.Expression | None:
        if isinstance(self._inner, ex.Negation):
            return ex.Negation(ex.Sine(self._inner._inner))
        else:
            return None
