from __future__ import annotations
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from src.forward_accumulation.variable import Variable
from src.forward_accumulation.custom_types import VariableValues, Real
from src.forward_accumulation.result import InternalResult
from src.forward_accumulation.expression import NullaryExpression

class Constant(NullaryExpression):
    def __init__(
        self: Constant,
        value: Real
    ) -> None:
        self.value = value

    def _derive(
        self: Constant,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
        return InternalResult(
            lacksVariables = True,
            value = self.value,
            partial = 0
        )

    def __eq__(
        self: Constant,
        other: Any
    ) -> bool:
        return isinstance(other, Constant) and (other.value == self.value)

    def __str__(
        self: Constant
    ) -> str:
        return str(self.value)
