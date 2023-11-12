from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real
    from src.smooth_expression.variable_values import VariableValues
    from src.smooth_expression.all_partials import AllPartials
    from src.smooth_expression.expression import Expression
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

    def _computePartialAt(
        self: SquareRoot,
        variableValues: VariableValues,
        withRespectTo: str
    ) -> tuple[bool, Real]:
        aValue = self.a._evaluate(variableValues)
        self._ensureValueIsInDomain(aValue)
        aLacksVariables, aPartial = self.a._computePartialAt(variableValues, withRespectTo)
        # d(sqrt(a)) = (1 / (2 sqrt(a))) * da
        return (
            aLacksVariables,
            aPartial / (2 * math.sqrt(aValue))
        )

    def _computeAllPartialsAt(
        self: SquareRoot,
        allPartials: AllPartials,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        aValue = self.a._evaluate(variableValues)
        self._ensureValueIsInDomain(aValue)
        selfValue = self._evaluate(variableValues)
        # d(sqrt(a)) = (1 / (2 sqrt(a))) * da
        nextSeed = seed / (2 * selfValue)
        self.a._computeAllPartialsAt(allPartials, variableValues, nextSeed)

    def _ensureValueIsInDomain(
        self: SquareRoot,
        aValue: Real
    ) -> None:
        if aValue == 0:
            raise DomainException("SquareRoot(x) is not smooth around x = 0")
        elif aValue < 0:
            raise DomainException("SquareRoot(x) is undefined for x < 0")
