from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.point import Point
    from smoothmath.expression import Expression
    from smoothmath.expressions import Variable

import smoothmath.utilities as utilities
import smoothmath.expressions as ex
from smoothmath.global_partial import GlobalPartial
from smoothmath.local_differential import LocalDifferential, LocalDifferentialBuilder


class GlobalDifferential:
    def __init__(
        self: GlobalDifferential,
        original_expression: Expression,
        synthetic_partials: dict[str, Expression]
    ) -> None:
        self.original_expression: Expression
        self.original_expression = original_expression
        self._synthetic_partials: dict[str, Expression]
        self._synthetic_partials = synthetic_partials.copy()

    def component_at(
        self: GlobalDifferential,
        point: Point,
        variable: Variable | str
    ) -> real_number:
        return self.component(variable).at(point)

    def component(
        self: GlobalDifferential,
        variable: Variable | str
    ) -> GlobalPartial:
        variable_name = utilities.get_variable_name(variable)
        synthetic_partial_or_none = self._synthetic_partials.get(variable_name, None)
        synthetic_partial = ex.Constant(0) if synthetic_partial_or_none is None else synthetic_partial_or_none
        return GlobalPartial(self.original_expression, synthetic_partial)

    def at(
        self: GlobalDifferential,
        point: Point
    ) -> LocalDifferential:
        self.original_expression.evaluate(point)
        builder = LocalDifferentialBuilder(self.original_expression)
        for variable_name, synthetic_partial in self._synthetic_partials.items():
            local_partial = synthetic_partial.evaluate(point)
            builder.add_to(variable_name, local_partial)
        return builder.build()

    def __eq__(
        self: GlobalDifferential,
        other: GlobalDifferential
    ) -> bool:
        # We'll assume correctness of the synthetic partials, so it suffices to compare
        # the original expressions.
        return self.original_expression == other.original_expression

    def __str__(
        self: GlobalDifferential
    ) -> str:
        return " + ".join([
            "(" + str(synthetic_partial) + ") d" + variable_name
            for variable_name, synthetic_partial in self._synthetic_partials.items()
        ])


class GlobalDifferentialBuilder:
    def __init__(
        self: GlobalDifferentialBuilder,
        original_expression: Expression
    ) -> None:
        self._original_expression: Expression
        self._original_expression = original_expression
        self._synthetic_partials: dict[str, Expression]
        self._synthetic_partials = {}

    def add_to(
        self: GlobalDifferentialBuilder,
        variable: Variable | str,
        contribution: Expression
    ) -> None:
        variable_name = utilities.get_variable_name(variable)
        existing = self._synthetic_partials.get(variable_name, None)
        next = contribution if existing is None else existing + contribution
        self._synthetic_partials[variable_name] = next

    def build(
        self: GlobalDifferentialBuilder
    ) -> GlobalDifferential:
        return GlobalDifferential(self._original_expression, self._synthetic_partials)
