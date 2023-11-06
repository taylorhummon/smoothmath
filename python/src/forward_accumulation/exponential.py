from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.forward_accumulation.expression import Expression
    from src.forward_accumulation.variable import Variable
import math
from src.forward_accumulation.custom_types import VariableValues, Real
from src.forward_accumulation.result import InternalResult
from src.forward_accumulation.expression import UnaryExpression

class Exponential(UnaryExpression):
    def __init__(
        self: Exponential,
        exponent: Expression,
        base: Real = math.e
    ) -> None:
        super().__init__(exponent)
        if base <= 0:
            raise Exception("Exponentials must have a positive base")
        self.base: Real
        self.base = base

    def _derive(
        self: Exponential,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
        aLacksVariables, aValue, aPartial = self.a._derive(variableValues, withRespectTo).toTriple()
        resultValue = self.base ** aValue
        # d(C ** b) = ln(C) * C ** b * db
        return InternalResult(
            lacksVariables = aLacksVariables,
            value = resultValue,
            partial = math.log(self.base) * resultValue * aPartial
        )

    def __str__(
        self: Exponential
    ) -> str:
        if self.base == math.e:
            return f"Exponential({self.a})"
        else:
            return f"Exponential({self.a}, base = {self.base})"
