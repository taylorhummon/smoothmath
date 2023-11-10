from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real
    from src.smooth_expression.variable_values import VariableValues
    from src.smooth_expression.all_partials import AllPartials
    from src.smooth_expression.expression import Expression
    from src.smooth_expression.variable import Variable
from src.smooth_expression.binary_expression import BinaryExpression

class Minus(BinaryExpression):
    def __init__(
        self: Minus,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Minus,
        variableValues: VariableValues
    ) -> Real:
        if self._value is not None:
            return self._value
        aValue = self.a._evaluate(variableValues)
        bValue = self.b._evaluate(variableValues)
        self._value = aValue - bValue
        return self._value

    def _partialAt(
        self: Minus,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> tuple[bool, Real]:
        aLacksVariables, aPartial = self.a._partialAt(variableValues, withRespectTo)
        bLacksVariables, bPartial = self.b._partialAt(variableValues, withRespectTo)
        # d(a - b) = da - db
        return (
            aLacksVariables and bLacksVariables,
            aPartial - bPartial
        )

    def _allPartialsAt(
        self: Minus,
        allPartials: AllPartials,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        # d(a - b) = da - db
        self.a._allPartialsAt(allPartials, variableValues, seed)
        self.b._allPartialsAt(allPartials, variableValues, - seed)
