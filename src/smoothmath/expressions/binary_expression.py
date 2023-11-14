from __future__ import annotations
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.typing import real_number

# imports needed for class declaration
from smoothmath.expressions.expression import Expression

class BinaryExpression(Expression):
    def __init__(
        self: BinaryExpression,
        a: Expression,
        b: Expression
    ) -> None:
        if not isinstance(a, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {a}")
        if not isinstance(b, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {b}")
        super().__init__(lacks_variables = a.lacks_variables and b.lacks_variables)
        self._a : Expression
        self._a = a
        self._b : Expression
        self._b = b
        self._value : real_number | None
        self._value = None

    def _reset_evaluation_cache(
        self: BinaryExpression
    ) -> None:
        self._value = None
        self._a._reset_evaluation_cache()
        self._b._reset_evaluation_cache()

    def __eq__(
        self: BinaryExpression,
        other: Any
    ) -> bool:
        return (other.__class__ == self.__class__) and (other._a == self._a) and (other._b == self._b)

    def __str__(
        self: BinaryExpression
    ) -> str:
        class_name = type(self).__name__
        return f"{class_name}({self._a}, {self._b})"
