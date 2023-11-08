from __future__ import annotations
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real, VariableValues
    from src.smooth_expression.multi_result import InternalMultiResult
    from src.smooth_expression.variable import Variable
from src.smooth_expression.nullary_expression import NullaryExpression

class Constant(NullaryExpression):
    def __init__(
        self: Constant,
        value: Real
    ) -> None:
        super().__init__(lacksVariables = True)
        self._value : Real
        self._value = value

    def _evaluate(
        self: Constant,
        variableValues: VariableValues
    ) -> Real:
        return self._value

    def _deriveSingle(
        self: Constant,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> tuple[bool, Real]:
        return (True, 0)

    def _deriveMulti(
        self: Constant,
        multiResult: InternalMultiResult,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        pass

    def __eq__(
        self: Constant,
        other: Any
    ) -> bool:
        return isinstance(other, Constant) and (other._value == self._value)

    def __str__(
        self: Constant
    ) -> str:
        return str(self._value)
