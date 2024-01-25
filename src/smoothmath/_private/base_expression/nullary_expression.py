from __future__ import annotations
import smoothmath as sm
import smoothmath._private.base_expression as base


class NullaryExpression(base.Expression):
    def __init__(
        self: NullaryExpression,
        lacks_variables: bool
    ) -> None:
        super().__init__(lacks_variables)

    def _reset_evaluation_cache(
        self: NullaryExpression
    ) -> None:
        pass

    def _take_reduction_step(
        self: sm.Expression
    ) -> sm.Expression:
        self._is_fully_reduced = True
        return self
