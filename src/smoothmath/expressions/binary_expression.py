from __future__ import annotations
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.typing import real_number
from smoothmath.expressions.expression import Expression

class BinaryExpression(Expression):
    def __init__(
        self: BinaryExpression,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(lacks_variables = a.lacks_variables and b.lacks_variables)
        if not isinstance(a, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {a}")
        if not isinstance(b, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {b}")
        self.a : Expression
        self.a = a
        self.b : Expression
        self.b = b
        self._value : real_number | None
        self._value = None

    def _reset_evaluation_cache(
        self: BinaryExpression
    ) -> None:
        self._value = None
        self.a._reset_evaluation_cache()
        self.b._reset_evaluation_cache()

    def __eq__(
        self: BinaryExpression,
        other: Any
    ) -> bool:
        return (other.__class__ == self.__class__) and (other.a == self.a) and (other.b == self.b)

    def __str__(
        self: BinaryExpression
    ) -> str:
        class_name = type(self).__name__
        return f"{class_name}({self.a}, {self.b})"
