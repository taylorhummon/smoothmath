from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.point import Point
    from smoothmath.global_differential import GlobalDifferential
    from smoothmath.local_differential import LocalDifferential
    from smoothmath.expression import Expression

from smoothmath.expression import BinaryExpression
import smoothmath.expressions as ex


# differential rule: d(a + b) = da + db

class Plus(BinaryExpression):
    def __init__(
        self: Plus,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Plus,
        point: Point
    ) -> real_number:
        if self._value is not None:
            return self._value
        a_value = self._a._evaluate(point)
        b_value = self._b._evaluate(point)
        self._value = a_value + b_value
        return self._value

    def _local_partial(
        self: Plus,
        point: Point,
        with_respect_to: str
    ) -> real_number:
        a_partial = self._a._local_partial(point, with_respect_to)
        b_partial = self._b._local_partial(point, with_respect_to)
        return a_partial + b_partial

    def _global_partial(
        self: Plus,
        with_respect_to: str
    ) -> Expression:
        a_partial = self._a._global_partial(with_respect_to)
        b_partial = self._b._global_partial(with_respect_to)
        return ex.Plus(a_partial, b_partial)

    def _compute_local_partials(
        self: Plus,
        local_differential: LocalDifferential,
        point: Point,
        accumulated: real_number
    ) -> None:
        self._a._compute_local_partials(local_differential, point, accumulated)
        self._b._compute_local_partials(local_differential, point, accumulated)

    def _compute_global_partials(
        self: Plus,
        global_differential: GlobalDifferential,
        accumulated: Expression
    ) -> None:
        self._a._compute_global_partials(global_differential, accumulated)
        self._b._compute_global_partials(global_differential, accumulated)
