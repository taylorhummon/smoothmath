from __future__ import annotations
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import Real
from src.smooth_expression.expression import Expression

class UnaryExpression(Expression):
    def __init__(
        self: UnaryExpression,
        a: Expression
    ) -> None:
        super().__init__(lacksVariables = a.lacksVariables)
        if not isinstance(a, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {a}")
        self.a : Expression
        self.a = a
        self._value : Real | None
        self._value = None

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
