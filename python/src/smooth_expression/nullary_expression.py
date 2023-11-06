from __future__ import annotations
from src.smooth_expression.expression import Expression

class NullaryExpression(Expression):
    def __init__(
        self: NullaryExpression,
        lacksVariables: bool
    ) -> None:
        super().__init__(lacksVariables)

    def _resetEvaluationCache(
        self: NullaryExpression
    ) -> None:
        pass
