from __future__ import annotations
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real
from src.smooth_expression.expression import Expression

class BinaryExpression(Expression):
    def __init__(
        self: BinaryExpression,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(lacksVariables = a.lacksVariables and b.lacksVariables)
        if not isinstance(a, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {a}")
        if not isinstance(b, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {b}")
        self.a : Expression
        self.a = a
        self.b : Expression
        self.b = b
        self._value : Real | None
        self._value = None

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
        return (other.__class__ == self.__class__) and (other.a == self.a) and (other.b == self.b)

    def __str__(
        self: BinaryExpression
    ) -> str:
        className = type(self).__name__
        return f"{className}({self.a}, {self.b})"
