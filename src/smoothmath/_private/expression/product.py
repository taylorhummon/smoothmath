from __future__ import annotations
from typing import TYPE_CHECKING, Callable
from functools import reduce
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
from smoothmath._private.utilities import list_without_entry_at
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


def product(
    values: list[sm.real_number]
) -> sm.real_number:
    return reduce(lambda a, b: a * b, values, 1)


class Product(base.NAryExpression):
    def _verify_domain_constraints(
        self: Product,
        inner_expressions: list[sm.Expression]
    ) -> None:
        pass

    def _value_formula(
        self: Product,
        inner_values: list[sm.real_number]
    ) -> sm.real_number:
        return product(inner_values)

    def _local_partial(
        self: Product,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        inner_values = [inner._evaluate(point) for inner in self._inner_expressions]
        return sum(
            inner._local_partial(point, with_respect_to) *
            product(list_without_entry_at(inner_values, i))
            for (i, inner) in enumerate(self._inner_expressions)
        )

    def _synthetic_partial(
        self: Product,
        with_respect_to: str
    ) -> sm.Expression:
        return ex.Sum([
            ex.Product(
                [inner._synthetic_partial(with_respect_to)] +
                list_without_entry_at(self._inner_expressions, i)
            )
            for (i, inner) in enumerate(self._inner_expressions)
        ])

    def _compute_local_differential(
        self: Product,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        for inner in self._inner_expressions:
            inner._compute_local_differential(builder, accumulated)

    def _compute_global_differential(
        self: Product,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        for inner in self._inner_expressions:
            inner._compute_global_differential(builder, accumulated)

    @property
    def _reducers(
        self: Product
    ) -> list[Callable[[], sm.Expression | None]]:
        return []
