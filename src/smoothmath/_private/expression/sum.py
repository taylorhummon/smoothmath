from __future__ import annotations
from typing import TYPE_CHECKING, Callable
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


class Sum(base.NAryExpression):
    def _verify_domain_constraints(
        self: Sum,
        inner_expressions: list[sm.Expression]
    ) -> None:
        pass

    def _value_formula(
        self: Sum,
        inner_values: list[sm.real_number]
    ) -> sm.real_number:
        return sum(inner_values)

    def _local_partial(
        self: Sum,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        return sum(
            inner._local_partial(point, with_respect_to)
            for inner in self._inner_expressions
        )

    def _synthetic_partial(
        self: Sum,
        with_respect_to: str
    ) -> sm.Expression:
        return ex.Sum([
            inner._synthetic_partial(with_respect_to)
            for inner in self._inner_expressions
        ])

    def _compute_local_differential(
        self: Sum,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        for inner in self._inner_expressions:
            inner._compute_local_differential(builder, accumulated)

    def _compute_global_differential(
        self: Sum,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        for inner in self._inner_expressions:
            inner._compute_global_differential(builder, accumulated)

    @property
    def _reducers(
        self: Sum
    ) -> list[Callable[[], sm.Expression | None]]:
        return []
