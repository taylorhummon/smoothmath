from __future__ import annotations
from typing import TYPE_CHECKING, Any
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


# differential rule: d(C) = 0

class Constant(base.NullaryExpression):
    def __init__(
        self: Constant,
        value: sm.real_number
    ) -> None:
        super().__init__(lacks_variables = True)
        self._value: sm.real_number
        self._value = value

    def __eq__(
        self: Constant,
        other: Any
    ) -> bool:
        return isinstance(other, Constant) and (other._value == self._value)

    def __hash__(
        self: Constant
    ) -> int:
        if self._cached_hash is None:
            self._cached_hash = hash(self._value)
        return self._cached_hash

    def __str__(
        self: Constant
    ) -> str:
        return f"Constant({self._value})"

    def _evaluate(
        self: Constant,
        point: sm.Point
    ) -> sm.real_number:
        return self._value

    def _local_partial(
        self: Constant,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        return 0

    def _synthetic_partial(
        self: Constant,
        with_respect_to: str
    ) -> sm.Expression:
        return ex.Constant(0)

    def _compute_local_differential(
        self: Constant,
        builder: LocalDifferentialBuilder,
        point: sm.Point,
        accumulated: sm.real_number
    ) -> None:
        pass

    def _compute_global_differential(
        self: Constant,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        pass
