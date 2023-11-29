from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.expression import Expression
    from smoothmath.expressions import Variable

import smoothmath.utilities as utilities


class LocalDifferential:
    def __init__(
        self: LocalDifferential,
        original_expression: Expression,
        local_partials: dict[str, real_number]
    ) -> None:
        self.original_expression: Expression
        self.original_expression = original_expression
        self._local_partials: dict[str, real_number]
        self._local_partials = local_partials.copy()

    def component(
        self: LocalDifferential,
        variable: Variable | str
    ) -> real_number:
        variable_name = utilities.get_variable_name(variable)
        return self._local_partials.get(variable_name, 0)

    def __eq__(
        self: LocalDifferential,
        other: LocalDifferential
    ) -> bool:
        # We'll assume correctness of the local partials, so it suffices to compare
        # the original expressions.
        return self.original_expression == other.original_expression

    def __str__(
        self: LocalDifferential
    ) -> str:
        return " + ".join([
            "(" + str(local_partial) + ") d" + variable_name
            for variable_name, local_partial in self._local_partials.items()
        ])


class LocalDifferentialBuilder:
    def __init__(
        self: LocalDifferentialBuilder,
        original_expression: Expression
    ) -> None:
        self._original_expression: Expression
        self._original_expression = original_expression
        self._local_partials: dict[str, real_number]
        self._local_partials = {}

    def add_to(
        self: LocalDifferentialBuilder,
        variable: Variable | str,
        contribution: real_number
    ) -> None:
        variable_name = utilities.get_variable_name(variable)
        existing = self._local_partials.get(variable_name, 0)
        self._local_partials[variable_name] = existing + contribution

    def build(
        self: LocalDifferentialBuilder
    ) -> LocalDifferential:
        return LocalDifferential(self._original_expression, self._local_partials)
