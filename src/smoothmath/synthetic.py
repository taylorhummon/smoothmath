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
        # we evaluate the original expression to ensure it is defined for variable_values
        self.original_expression.evaluate(variable_values)
        variable_name = utilities.get_variable_name(variable)
        synthetic_partial = self._lookup(variable_name)
        return synthetic_partial.evaluate(variable_values)

    def _add_to(
        self: Synthetic,
        variable: Variable,
        summand: Expression
    ) -> None:
        expression = self._lookup(variable.name)
        self._partial_by_variable_name[variable.name] = ex.Plus(expression, summand)

    def _lookup(
        self: Synthetic,
        variable_name: str
    ) -> Expression:
        existing_or_none = self._partial_by_variable_name.get(variable_name, None)
        if existing_or_none is None:
            return ex.Constant(0)
        else:
            return existing_or_none

    # !!! this is a temporary hack
    def _register_partial(
        self: Synthetic,
        variable_name: str,
        partial: Expression
    ) -> None:
        self._partial_by_variable_name[variable_name] = partial
