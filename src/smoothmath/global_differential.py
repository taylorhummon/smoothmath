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
from smoothmath.local_differential import LocalDifferential


class GlobalDifferential:
    def __init__(
        self: GlobalDifferential,
        original_expression: Expression
    ) -> None:
        self.original_expression: Expression
        self.original_expression = original_expression
        self._synthetic_partials: dict[str, Expression]
        self._synthetic_partials = {}
        self._is_frozen = False

    def component_at(
        self: GlobalDifferential,
        point: Point,
        variable: Variable | str
    ) -> real_number:
        if not self._is_frozen:
            raise Exception("Cannot take the component_at() of a GlobalDifferential until frozen")
        return self.component(variable).at(point)

    def component(
        self: GlobalDifferential,
        variable: Variable | str
    ) -> GlobalPartial:
        if not self._is_frozen:
            raise Exception("Cannot take the component() of a GlobalDifferential until frozen")
        synthetic_partial = self._look_up_synthetic_partial(variable)
        return GlobalPartial(self.original_expression, synthetic_partial)

    def at(
        self: GlobalDifferential,
        point: Point
    ) -> LocalDifferential:
        if not self._is_frozen:
            raise Exception("Cannot take at() of a GlobalDifferential until frozen")
        self.original_expression.evaluate(point)
        local_differential = LocalDifferential(self.original_expression)
        for variable_name, synthetic_partial in self._synthetic_partials.items():
            local_partial = synthetic_partial.evaluate(point)
            local_differential._add_to(variable_name, local_partial)
        local_differential._freeze()
        return local_differential

    def _add_to(
        self: GlobalDifferential,
        variable: Variable | str,
        contribution: Expression
    ) -> None:
        if self._is_frozen:
            raise Exception("Cannot add to a frozen GlobalDifferential until frozen")
        synthetic_partial = self._look_up_synthetic_partial(variable)
        self._save_synthetic_partial(variable, synthetic_partial + contribution)

    def _look_up_synthetic_partial(
        self: GlobalDifferential,
        variable: Variable | str
    ) -> Expression:
        variable_name = utilities.get_variable_name(variable)
        synthetic_partial = self._synthetic_partials.get(variable_name, None)
        if synthetic_partial is None:
            return ex.Constant(0)
        else:
            return synthetic_partial

    def _save_synthetic_partial(
        self: GlobalDifferential,
        variable: Variable | str,
        synthetic_partial: Expression
    ) -> None:
        variable_name = utilities.get_variable_name(variable)
        self._synthetic_partials[variable_name] = synthetic_partial

    def _freeze(
        self: GlobalDifferential
    ) -> None:
        self._is_frozen = True

    def __eq__(
        self: GlobalDifferential,
        other: GlobalDifferential
    ) -> bool:
        # We'll assume correctness of the synthetic partials, so it suffices to compare
        # the original expressions once the global differentials have been frozen.
        return (
            self._is_frozen and
            other._is_frozen and
            (self.original_expression == other.original_expression)
        )

    def __str__(
        self: GlobalDifferential
    ) -> str:
        return " + ".join([
            "(" + str(synthetic_partial) + ") d" + variable_name
            for variable_name, synthetic_partial in self._synthetic_partials.items()
        ])
