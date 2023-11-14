from __future__ import annotations
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.typing import real_number

# imports needed for class declaration
from smoothmath.expressions.expression import Expression


class UnaryExpression(Expression):
    def __init__(
        self: UnaryExpression,
        a: Expression
    ) -> None:
        if not isinstance(a, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {a}")
        super().__init__(lacks_variables = a.lacks_variables)
        self._a: Expression
        self._a = a
        self._value: real_number | None
        self._value = None

    def _reset_evaluation_cache(
        self: UnaryExpression
    ) -> None:
        self._value = None
        self._a._reset_evaluation_cache()

    def __eq__(
        self: UnaryExpression,
        other: Any
    ) -> bool:
        return other.__class__ == self.__class__ and (other._a == self._a)

    def __str__(
        self: UnaryExpression
    ) -> str:
        class_name = type(self).__name__
        return f"{class_name}({self._a})"
