from __future__ import annotations
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real
    from src.smooth_expression.variable_values import VariableValues
    from src.smooth_expression.all_partials import AllPartials
from src.smooth_expression.nullary_expression import NullaryExpression

class Variable(NullaryExpression):
    def __init__(
        self: Variable,
        name: str
    ) -> None:
        super().__init__(lacksVariables = False)
        if not name:
            raise Exception("Variables must be given a non-blank name")
        self.name : str
        self.name = name
        self._cachedHash : int | None
        self._cachedHash = None

    def _evaluate(
        self: Variable,
        variableValues: VariableValues
    ) -> Real:
        return variableValues.valueFor(self.name)

    def _partialAt(
        self: Variable,
        variableValues: VariableValues,
        withRespectTo: str
    ) -> tuple[bool, Real]:
        if self.name == withRespectTo:
            return (False, 1)
        else:
            return (False, 0)

    def _allPartialsAt(
        self: Variable,
        allPartials: AllPartials,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        allPartials._addSeed(self, seed)

    def __eq__(
        self: Variable,
        other: Any
    ) -> bool:
        return isinstance(other, Variable) and (other.name == self.name)

    def __hash__(self):
        if not self._cachedHash:
            self._cachedHash = hash(self.name)
        return self._cachedHash

    def __str__(
        self: Variable
    ) -> str:
        return self.name
