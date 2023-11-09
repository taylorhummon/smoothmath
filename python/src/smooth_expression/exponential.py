from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real, VariableValues
    from src.smooth_expression.all_partials import AllPartials
    from src.smooth_expression.expression import Expression
    from src.smooth_expression.variable import Variable
import math
from src.smooth_expression.unary_expression import UnaryExpression

class Exponential(UnaryExpression):
    def __init__(
        self: Exponential,
        exponent: Expression,
        base: Real = math.e
    ) -> None:
        super().__init__(exponent)
        if base <= 0:
            raise Exception("Exponentials must have a positive base")
        self._base : Real
        self._base = base

    def _evaluate(
        self: Exponential,
        variableValues: VariableValues
    ) -> Real:
        if self._value is not None:
            return self._value
        aValue = self.a._evaluate(variableValues)
        self._value = self._base ** aValue
        return self._value

    def _partialAt(
        self: Exponential,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> tuple[bool, Real]:
        aValue = self.a._evaluate(variableValues)
        aLacksVariables, aPartial = self.a._partialAt(variableValues, withRespectTo)
        resultValue = self._base ** aValue
        # d(C ** b) = ln(C) * C ** b * db
        return (
            aLacksVariables,
            math.log(self._base) * resultValue * aPartial
        )

    def _allPartialsAt(
        self: Exponential,
        allPartials: AllPartials,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        selfValue = self._evaluate(variableValues)
        # d(e ** a) = e ** a * da
        self.a._allPartialsAt(allPartials, variableValues, seed * math.log(self._base) * selfValue)


    def __str__(
        self: Exponential
    ) -> str:
        if self._base == math.e:
            return f"Exponential({self.a})"
        else:
            return f"Exponential({self.a}, base = {self._base})"