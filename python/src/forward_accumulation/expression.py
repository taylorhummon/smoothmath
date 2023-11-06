from __future__ import annotations
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from src.forward_accumulation.variable import Variable
from abc import ABC, abstractmethod
from src.forward_accumulation.custom_types import VariableValues
from src.forward_accumulation.result import Result, InternalResult

class Expression(ABC):
    def derive(
        self: Expression,
        variableValues: VariableValues,
        withRespectTo: Variable,
    ) -> Result:
        return self._derive(variableValues, withRespectTo).toResult()

    @abstractmethod
    def _derive(
        self: Expression,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
        raise Exception("concrete classes derived from Expression must implement _derive()")

    @abstractmethod
    def __str__(
        self: Expression,
    ) -> InternalResult:
        raise Exception("concrete classes derived from Expression must implement __str__()")

    ## Operations ##

    def __neg__(
        self: Expression
    ) -> Negation:
        return Negation(self)

    def __add__(
        self: Expression,
        other: Expression
    ) -> Plus:
        return Plus(self, other)

    def __sub__(
        self: Expression,
        other: Expression
    ) -> Minus:
        return Minus(self, other)

    def __mul__(
        self: Expression,
        other: Expression
    ) -> Multiply:
        return Multiply(self, other)

    def __truediv__(
        self: Expression,
        other: Expression
    ) -> Divide:
        return Divide(self, other)

    def __pow__(
        self: Expression,
        other: Expression
    ) -> Power:
        return Power(self, other)

class NullaryExpression(Expression):
    pass

class UnaryExpression(Expression):
    def __init__(
        self: UnaryExpression,
        a: Expression
    ) -> None:
        if not isinstance(a, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {a}")
        self.a = a

    def __eq__(
        self: Variable,
        other: Any
    ) -> bool:
        return other.__class__ == self.__class__ and (other.a == self.a)

    def __str__(
        self: UnaryExpression
    ) -> str:
        className = type(self).__name__
        return f"{className}({self.a})"

class BinaryExpression(Expression):
    def __init__(
        self: UnaryExpression,
        a: Expression,
        b: Expression
    ) -> None:
        if not isinstance(a, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {a}")
        if not isinstance(b, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {b}")
        self.a = a
        self.b = b

    def __eq__(
        self: Variable,
        other: Any
    ) -> bool:
        return other.__class__ == self.__class__ and (other.a == self.a) and (other.b == self.b)

    def __str__(
        self: UnaryExpression
    ) -> str:
        className = type(self).__name__
        return f"{className}({self.a}, {self.b})"

from src.forward_accumulation.negation import Negation
from src.forward_accumulation.plus import Plus
from src.forward_accumulation.minus import Minus
from src.forward_accumulation.multiply import Multiply
from src.forward_accumulation.divide import Divide
from src.forward_accumulation.power import Power
