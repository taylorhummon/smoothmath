from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real, VariableValues
    from src.smooth_expression.multi_result import InternalMultiResult
    from src.smooth_expression.expression import Expression
    from src.smooth_expression.variable import Variable
from src.smooth_expression.single_result import InternalSingleResult
from src.smooth_expression.unary_expression import UnaryExpression


class Negation(UnaryExpression):
    def __init__(
        self: Negation,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Negation,
        variableValues: VariableValues
    ) -> Real:
        if self._value is not None:
            return self._value
        aValue = self.a._evaluate(variableValues)
        self._value = - aValue
        return self._value

    def _deriveSingle(
        self: Negation,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalSingleResult:
        aLacksVariables, aValue, aPartial = self.a._deriveSingle(variableValues, withRespectTo).toTriple()
        # d(-a) = -da
        return InternalSingleResult(
            lacksVariables = aLacksVariables,
            value = -aValue,
            partial = -aPartial
        )

    def _deriveMulti(
        self: Negation,
        multiResult: InternalMultiResult,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        # d(-a) = -da
        self.a._deriveMulti(multiResult, variableValues, -seed)
