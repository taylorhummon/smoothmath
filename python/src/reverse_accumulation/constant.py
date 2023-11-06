from __future__ import annotations
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from src.reverse_accumulation.result import InternalResult
    from src.reverse_accumulation.custom_types import Real, VariableValues
from src.reverse_accumulation.expression import NullaryExpression

class Constant(NullaryExpression):
    def __init__(
        self: Constant,
        value: Real
    ) -> None:
        super().__init__(lacksVariables = True)
        self._valueFromInit = value

    def _evaluate(
        self: Constant,
        variableValues: VariableValues
    ) -> Real:
        return self._valueFromInit

    def _derive(
        self: Constant,
        result: InternalResult,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        pass

    def __eq__(
        self: Constant,
        other: Any
    ) -> bool:
        return isinstance(other, Constant) and (other._valueFromInit == self._valueFromInit)

    def __str__(
        self: Constant
    ) -> str:
        return str(self._valueFromInit)
