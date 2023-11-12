from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real
    from src.smooth_expression.variable_values import VariableValues
    from src.smooth_expression.expression import Expression
    from src.smooth_expression.all_partials import AllPartials
from src.smooth_expression.binary_expression import BinaryExpression

class Plus(BinaryExpression):
    def __init__(
        self: Plus,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Plus,
        variableValues: VariableValues
    ) -> Real:
        if self._value is not None:
            return self._value
        aValue = self.a._evaluate(variableValues)
        bValue = self.b._evaluate(variableValues)
        self._value = aValue + bValue
        return self._value

    def _partialAt(
        self: Plus,
        variableValues: VariableValues,
        withRespectTo: str
    ) -> Real:
        aPartial = self.a._partialAt(variableValues, withRespectTo)
        bPartial = self.b._partialAt(variableValues, withRespectTo)
        # d(a + b) = da + db
        return aPartial + bPartial

    def _computeAllPartialsAt(
        self: Plus,
        allPartials: AllPartials,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        # d(a + b) = da + db
        self.a._computeAllPartialsAt(allPartials, variableValues, seed)
        self.b._computeAllPartialsAt(allPartials, variableValues, seed)
