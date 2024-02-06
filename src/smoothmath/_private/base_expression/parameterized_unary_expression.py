from __future__ import annotations
from typing import Any
import smoothmath as sm
import smoothmath._private.base_expression as base
from smoothmath._private.utilities import get_class_name


class ParameterizedUnaryExpression(base.UnaryExpression):
    def __init__(
        self: ParameterizedUnaryExpression,
        inner: sm.Expression,
        parameter: Any
    ) -> None:
        super().__init__(inner)
        self._parameter: Any
        self._parameter = parameter

    def _rebuild(
        self: ParameterizedUnaryExpression,
        inner: sm.Expression
    ) -> ParameterizedUnaryExpression:
        return self.__class__(inner, self._parameter)

    ## Operations ##

    def __eq__(
        self: ParameterizedUnaryExpression,
        other: Any
    ) -> bool:
        return super().__eq__(other) and (other._parameter == self._parameter)

    def __hash__(
        self: ParameterizedUnaryExpression
    ) -> int:
        return hash((get_class_name(self), self._inner, self._parameter))

    def __str__(
        self: ParameterizedUnaryExpression
    ) -> str:
        return f"{get_class_name(self)}({self._inner}, {self._parameter})"

    def __repr__(
        self: ParameterizedUnaryExpression
    ) -> str:
        return f"{get_class_name(self)}({self._inner}, {self._parameter})"