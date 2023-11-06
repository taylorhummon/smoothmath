from __future__ import annotations
from typing import Any
from abc import ABC, abstractmethod
from src.reverse_accumulation.custom_types import Real, VariableValues
from src.reverse_accumulation.result import Result, InternalResult

class Expression(ABC):
    def __init__(
        self: Expression,
        lacksVariables: bool
    ) -> None:
        self.lacksVariables: bool
        self.lacksVariables = lacksVariables
        self._value: Real | None
        self._value = None

    def derive(
        self: Expression,
        variableValues: VariableValues
    ) -> Result:
        try:
            value = self._evaluateUsingCache(variableValues)
            result = InternalResult(value)
            self._derive(result, variableValues, 1)
            return result.toResult()
        finally:
            self._resetEvaluationCache()

    @abstractmethod
    def _derive(
        self: Expression,
        result: InternalResult,
        variableValues: VariableValues,
        seed: Real
    ) -> None:
        raise Exception("concrete classes derived from Expression must implement _derive()")

    def _evaluateUsingCache(
        self: Expression,
        variableValues: VariableValues
    ) -> Real:
        if self._value is None:
            self._value = self._evaluate(variableValues)
        return self._value

    @abstractmethod
    def _evaluate(
        self: Expression,
        variableValues: VariableValues
    ) -> Real:
        raise Exception("concrete classes derived from Expression must implement _evaluate()")

    @abstractmethod
    def _resetEvaluationCache(
        self: Expression
    ) -> None:
        raise Exception("concrete classes derived from Expression must implement _resetEvaluationCache()")

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
    def __init__(
        self: NullaryExpression,
        lacksVariables: bool
    ) -> None:
        super().__init__(lacksVariables)

    def _resetEvaluationCache(
        self: NullaryExpression
    ) -> None:
        self._value = None

class UnaryExpression(Expression):
    def __init__(
        self: UnaryExpression,
        a: Expression
    ) -> None:
        super().__init__(lacksVariables = a.lacksVariables)
        if not isinstance(a, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {a}")
        self.a = a

    def _resetEvaluationCache(
        self: UnaryExpression
    ) -> None:
        self._value = None
        self.a._resetEvaluationCache()

    def __eq__(
        self: UnaryExpression,
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
        self: BinaryExpression,
        a: Expression,
        b: Expression,
    ) -> None:
        super().__init__(lacksVariables = a.lacksVariables and b.lacksVariables)
        if not isinstance(a, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {a}")
        if not isinstance(b, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {b}")
        self.a = a
        self.b = b

    def _resetEvaluationCache(
        self: BinaryExpression
    ) -> None:
        self._value = None
        self.a._resetEvaluationCache()
        self.b._resetEvaluationCache()

    def __eq__(
        self: BinaryExpression,
        other: Any
    ) -> bool:
        return other.__class__ == self.__class__ and (other.a == self.a) and (other.b == self.b)

    def __str__(
        self: BinaryExpression
    ) -> str:
        className = type(self).__name__
        return f"{className}({self.a}, {self.b})"

from src.reverse_accumulation.negation import Negation
from src.reverse_accumulation.plus import Plus
from src.reverse_accumulation.minus import Minus
from src.reverse_accumulation.multiply import Multiply
from src.reverse_accumulation.divide import Divide
from src.reverse_accumulation.power import Power
