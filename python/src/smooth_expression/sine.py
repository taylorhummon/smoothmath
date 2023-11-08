from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real, VariableValues
    from src.smooth_expression.multi_result import InternalMultiResult
    from src.smooth_expression.expression import Expression
    from src.smooth_expression.variable import Variable
import math
from src.smooth_expression.unary_expression import UnaryExpression

class Sine(UnaryExpression):
    def __init__(
        self: Sine,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Sine,
        variableValues: VariableValues
    ) -> Real:
        if self._value is not None:
            return self._value
        aValue = self.a._evaluate(variableValues)
        self._value = math.sin(aValue)
        return self._value

    def _deriveSingle(
        self: Sine,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> tuple[bool, Real]:
        aValue = self.a._evaluate(variableValues)
        aLacksVariables, aPartial = self.a._deriveSingle(variableValues, withRespectTo)
        # d(sin(a)) = cos(a) * da
        return (
            aLacksVariables,
            math.cos(aValue) * aPartial
        )

    def _deriveMulti(
        self: Sine,
        multiResult: InternalMultiResult,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        aValue = self.a._evaluate(variableValues)
        # d(sin(a)) = cos(a) * da
        self.a._deriveMulti(multiResult, variableValues, seed * math.cos(aValue))
