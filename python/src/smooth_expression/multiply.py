from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real
    from src.smooth_expression.variable_values import VariableValues
    from src.smooth_expression.all_partials import AllPartials
    from src.smooth_expression.expression import Expression
from src.smooth_expression.binary_expression import BinaryExpression

class Multiply(BinaryExpression):
    def __init__(
        self: Multiply,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Multiply,
        variableValues: VariableValues
    ) -> Real:
        if self._value is not None:
            return self._value
        aValue = self.a._evaluate(variableValues)
        bValue = self.b._evaluate(variableValues)
        self._value = aValue * bValue
        return self._value

    def _partialAt(
        self: Multiply,
        variableValues: VariableValues,
        withRespectTo: str
    ) -> tuple[bool, Real]:
        aValue = self.a._evaluate(variableValues)
        bValue = self.b._evaluate(variableValues)
        aLacksVariables, aPartial = self.a._partialAt(variableValues, withRespectTo)
        bLacksVariables, bPartial = self.b._partialAt(variableValues, withRespectTo)
        # d(a * b) = b * da + a * db
        return (
            aLacksVariables and bLacksVariables,
            bValue * aPartial + aValue * bPartial
        )

    def _allPartialsAt(
        self: Multiply,
        allPartials: AllPartials,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        aValue = self.a._evaluate(variableValues)
        bValue = self.b._evaluate(variableValues)
        # d(a * b) = b * da + a * db
        self.a._allPartialsAt(allPartials, variableValues, seed * bValue)
        self.b._allPartialsAt(allPartials, variableValues, seed * aValue)
