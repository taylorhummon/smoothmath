from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.variable_values import VariableValues
    from smoothmath.expression import Expression
    from smoothmath.expressions import Variable

import smoothmath.utilities as utilities
import smoothmath.expressions as ex


class Synthetic:
    def __init__(
        self: Synthetic,
        original_expression: Expression
    ) -> None:
        self.original_expression: Expression
        self.original_expression = original_expression
        self._partial_by_variable_name: dict[str, Expression]
        self._partial_by_variable_name = {}

    def partial_at(
        self: Synthetic,
        variable_values: VariableValues,
        variable: Variable | str
    ) -> real_number:
        # We evaluate the original expression to check for DomainErrors.
        # e.g. (ln(x))' = 1 / x
        # Naively, the RHS is defined for negative x, but ln(x) isn't defined there!
        self.original_expression.evaluate(variable_values)
        synthetic_partial = self._lookup(utilities.get_variable_name(variable))
        return synthetic_partial.evaluate(variable_values)

    def _add_to(
        self: Synthetic,
        variable: Variable,
        expression: Expression
    ) -> None:
        existing = self._lookup(variable.name)
        self._partial_by_variable_name[variable.name] = ex.Plus(existing, expression)

    def _lookup(
        self: Synthetic,
        variable_name: str
    ) -> Expression:
        existing_or_none = self._partial_by_variable_name.get(variable_name, None)
        if existing_or_none is None:
            return ex.Constant(0)
        else:
            return existing_or_none
