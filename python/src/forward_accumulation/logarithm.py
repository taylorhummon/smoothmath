from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.forward_accumulation.expression import Expression
    from src.forward_accumulation.variable import Variable
import math
from src.forward_accumulation.custom_types import VariableValues, Real
from src.forward_accumulation.custom_exceptions import DomainException
from src.forward_accumulation.single_result import InternalSingleResult
from src.forward_accumulation.expression import UnaryExpression

class Logarithm(UnaryExpression):
    def __init__(
        self: Logarithm,
        a: Expression,
        base: Real = math.e
    ) -> None:
        super().__init__(a)
        if base <= 0:
            raise Exception("Logarithms must have a positive base")
        elif base == 1:
            raise Exception("Logarithms cannot have base = 1")
        base: Real
        self.base = base

    def _derive(
        self: Logarithm,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalSingleResult:
        aLacksVariables, aValue, aPartial = self.a._derive(variableValues, withRespectTo).toTriple()
        if aValue == 0:
            raise DomainException("Logarithm(x) blows up around x = 0")
        elif aValue < 0:
            raise DomainException("Logarithm(x) is undefined for x < 0")
        # d(log_C(a)) = (1 / (ln(C) * a)) * da
        return InternalSingleResult(
            lacksVariables = aLacksVariables,
            value = math.log(aValue, self.base),
            partial = aPartial / (math.log(self.base) * aValue)
        )

    def __str__(
        self: Logarithm
    ) -> str:
        if self.base == math.e:
            return f"Logarithm({self.a})"
        else:
            return f"Logarithm({self.a}, base = {self.base})"
