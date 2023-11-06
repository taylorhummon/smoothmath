from __future__ import annotations
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from src.forward_accumulation.variable import Variable
from src.forward_accumulation.custom_types import VariableValues
from src.forward_accumulation.result import InternalResult
from src.forward_accumulation.expression import NullaryExpression

class Variable(NullaryExpression):
    def __init__(
        self: Variable,
        name: str
    ) -> None:
        if not name:
            raise Exception("Variables must be given a non-blank name")
        self.name: str
        self.name = name
        self._cachedHash: int | None
        self._cachedHash = None

    def _derive(
        self: Variable,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
        value = variableValues.get(self, None)
        if value is None:
            raise Exception("variableValues is missing a value for a variable")
        return InternalResult(
            lacksVariables = False,
            value = value,
            partial = 1 if self == withRespectTo else 0
        )

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
