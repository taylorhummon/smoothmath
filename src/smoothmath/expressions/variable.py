from __future__ import annotations
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.typing import real_number
    from smoothmath.variable_values import VariableValues
    from smoothmath.all_partials import AllPartials
from smoothmath.expressions.nullary_expression import NullaryExpression

class Variable(NullaryExpression):
    def __init__(
        self: Variable,
        name: str
    ) -> None:
        super().__init__(lacks_variables = False)
        if not name:
            raise Exception("Variables must be given a non-blank name")
        self.name : str
        self.name = name
        self._cached_hash : int | None
        self._cached_hash = None

    def _evaluate(
        self: Variable,
        variable_values: VariableValues
    ) -> real_number:
        return variable_values.value_for(self.name)

    def _partial_at(
        self: Variable,
        variable_values: VariableValues,
        with_respect_to: str
    ) -> real_number:
        if self.name == with_respect_to:
            return 1
        else:
            return 0

    def _compute_all_partials_at(
        self: Variable,
        all_partials: AllPartials,
        variable_values: VariableValues,
        seed: real_number
    ) -> None:
        all_partials._add_seed(self, seed)

    def __eq__(
        self: Variable,
        other: Any
    ) -> bool:
        return isinstance(other, Variable) and (other.name == self.name)

    def __hash__(
        self: Variable
    ) -> int:
        if self._cached_hash is None:
            self._cached_hash = hash(self.name)
        return self._cached_hash

    def __str__(
        self: Variable
    ) -> str:
        return self.name
