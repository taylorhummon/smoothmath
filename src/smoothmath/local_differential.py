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
        original_expression: Expression
    ) -> None:
        self.original_expression: Expression
        self.original_expression = original_expression
        self._local_partials: dict[str, real_number]
        self._local_partials = {}
        self._is_frozen = False

    def component(
        self: LocalDifferential,
        variable: Variable | str
    ) -> real_number:
        if not self._is_frozen:
            raise Exception("Cannot take the component() of a LocalDifferential until frozen")
        variable_name = utilities.get_variable_name(variable)
        return self._local_partials.get(variable_name, 0)

    def _add_to(
        self: LocalDifferential,
        variable: Variable | str,
        contribution: real_number
    ) -> None:
        if self._is_frozen:
            raise Exception("Cannot add to a frozen LocalDifferential")
        variable_name = utilities.get_variable_name(variable)
        existing = self._local_partials.get(variable_name, 0)
        self._local_partials[variable_name] = existing + contribution

    def _freeze(
        self: LocalDifferential
    ) -> None:
        self._is_frozen = True

    def __eq__(
        self: LocalDifferential,
        other: LocalDifferential
    ) -> bool:
        # We'll assume correctness of the local partials, so it suffices to compare
        # the original expressions once the local differentials have been frozen.
        return (
            self._is_frozen and
            other._is_frozen and
            (self.original_expression == other.original_expression)
        )

    def __str__(
        self: LocalDifferential
    ) -> str:
        return " + ".join([
            "(" + str(local_partial) + ") d" + variable_name
            for variable_name, local_partial in self._local_partials.items()
        ])
