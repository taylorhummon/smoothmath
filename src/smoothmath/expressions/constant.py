from __future__ import annotations
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.point import Point
    from smoothmath.computed_local_partials import ComputedLocalPartials
    from smoothmath.computed_global_partials import ComputedGlobalPartials
    from smoothmath.expression import Expression

from smoothmath.expression import NullaryExpression
import smoothmath.expressions as ex


# differential rule: d(C) = 0

class Constant(NullaryExpression):
    def __init__(
        self: Constant,
        value: real_number
    ) -> None:
        super().__init__(lacks_variables = True)
        self._value: real_number
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
        point: Point
    ) -> real_number:
        return self._value

    def _local_partial(
        self: Constant,
        point: Point,
        with_respect_to: str
    ) -> real_number:
        return 0

    def _global_partial(
        self: Constant,
        with_respect_to: str
    ) -> Expression:
        return ex.Constant(0)

    def _compute_local_partials(
        self: Constant,
        computed_local_partials: ComputedLocalPartials,
        point: Point,
        accumulated: real_number
    ) -> None:
        pass

    def _compute_global_partials(
        self: Constant,
        computed_global_partials: ComputedGlobalPartials,
        accumulated: Expression
    ) -> None:
        pass
