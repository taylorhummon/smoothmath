from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real, VariableValues
    from src.smooth_expression.all_partials import AllPartials
    from src.smooth_expression.expression import Expression
    from src.smooth_expression.variable import Variable
import math
from src.smooth_expression.custom_exceptions import DomainException
from src.smooth_expression.unary_expression import UnaryExpression

class SquareRoot(UnaryExpression):
    def __init__(
        self: SquareRoot,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: SquareRoot,
        variableValues: VariableValues
    ) -> Real:
        if self._value is not None:
            return self._value
        aValue = self.a._evaluate(variableValues)
        self._ensureValueIsInDomain(aValue)
        self._value = math.sqrt(aValue)
        return self._value

    def _partialAt(
        self: SquareRoot,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> tuple[bool, Real]:
        aValue = self.a._evaluate(variableValues)
        aLacksVariables, aPartial = self.a._partialAt(variableValues, withRespectTo)
        if aValue == 0:
            raise DomainException("SquareRoot(x) is not smooth around x = 0")
        elif aValue < 0:
            raise DomainException("SquareRoot(x) is undefined for x < 0")
        # d(sqrt(a)) = (1 / (2 sqrt(a))) * da
        return (
            aLacksVariables,
            aPartial / (2 * math.sqrt(aValue))
        )

    def _allPartialsAt(
        self: SquareRoot,
        allPartials: AllPartials,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        aValue = self.a._evaluate(variableValues)
        self._ensureValueIsInDomain(aValue)
        selfValue = self._evaluate(variableValues)
        # d(sqrt(a)) = (1 / (2 sqrt(a))) * da
        self.a._allPartialsAt(allPartials, variableValues, seed / (2 * selfValue))

    def _ensureValueIsInDomain(
        self: SquareRoot,
        aValue: Real
    ) -> None:
        if aValue == 0:
            raise DomainException("SquareRoot(x) is not smooth around x = 0")
        elif aValue < 0:
            raise DomainException("SquareRoot(x) is undefined for x < 0")