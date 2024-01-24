from __future__ import annotations
from typing import TYPE_CHECKING, Callable
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.expression.base as base
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


class Plus(base.BinaryExpression):
    def _verify_domain_constraints(
        self: Plus,
        left_value: sm.real_number,
        right_value: sm.real_number
    ) -> None:
        pass

    def _value_formula(
        self: Plus,
        left_value: sm.real_number,
        right_value: sm.real_number
    ) -> sm.real_number:
        return left_value + right_value

    def _local_partial(
        self: Plus,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        left_partial = self._left._local_partial(point, with_respect_to)
        right_partial = self._right._local_partial(point, with_respect_to)
        return left_partial + right_partial

    def _synthetic_partial(
        self: Plus,
        with_respect_to: str
    ) -> sm.Expression:
        left_partial = self._left._synthetic_partial(with_respect_to)
        right_partial = self._right._synthetic_partial(with_respect_to)
        return ex.Plus(left_partial, right_partial)

    def _compute_local_differential(
        self: Plus,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        self._left._compute_local_differential(builder, accumulated)
        self._right._compute_local_differential(builder, accumulated)

    def _compute_global_differential(
        self: Plus,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        self._left._compute_global_differential(builder, accumulated)
        self._right._compute_global_differential(builder, accumulated)

    @property
    def _reducers(
        self: Plus
    ) -> list[Callable[[], sm.Expression | None]]:
        return [
            self._reduce_by_associating_plus_right,
            self._reduce_u_plus_zero,
            self._reduce_by_commuting_constant_right_across_plus,
            self._reduce_by_commuting_negation_right_across_plus,
            self._reduce_sum_of_negations,
            self._reduce_sum_of_logarithms
        ]

    # Plus(Plus(u, v), w) => Plus(u, Plus(v, w))
    def _reduce_by_associating_plus_right(
        self: Plus
    ) -> sm.Expression | None:
        if isinstance(self._left, ex.Plus):
            return ex.Plus(
                self._left._left,
                ex.Plus(self._left._right, self._right)
            )
        else:
            return None

    # Plus(u, Constant(0)) => u
    def _reduce_u_plus_zero(
        self: Plus
    ) -> sm.Expression | None:
        if (
            isinstance(self._right, ex.Constant) and
            self._right.value == 0
        ):
            return self._left
        else:
            return None

    # Plus(Constant(c), u) => Plus(u, Constant(c))
    def _reduce_by_commuting_constant_right_across_plus(
        self: Plus
    ) -> sm.Expression | None:
        if (
            isinstance(self._left, ex.Constant) and
            not isinstance(self._right, (ex.Constant, ex.Negation))
        ):
            return ex.Plus(self._right, self._left)
        else:
            return None

    # Plus(Negation(u), v) => Plus(v, Negation(u))
    def _reduce_by_commuting_negation_right_across_plus(
        self: Plus
    ) -> sm.Expression | None:
        if (
            isinstance(self._left, ex.Negation) and
            not isinstance(self._right, ex.Negation)
        ):
            return ex.Plus(self._right, self._left)
        else:
            return None

    # Plus(Negation(u), Negation(v)) => Negation(Plus(u, v))
    def _reduce_sum_of_negations(
        self: Plus
    ) -> sm.Expression | None:
        if (
            isinstance(self._left, ex.Negation) and
            isinstance(self._right, ex.Negation)
        ):
            return ex.Negation(ex.Plus(self._left._inner, self._right._inner))
        else:
            return None

    # Plus(Logarithm(u), Logarithm(v)) => Logarithm(Multiply(u, v))
    def _reduce_sum_of_logarithms(
        self: Plus
    ) -> sm.Expression | None:
        if (
            isinstance(self._left, ex.Logarithm) and
            isinstance(self._right, ex.Logarithm) and
            self._left.base == self._right.base
        ):
            return ex.Logarithm(
                ex.Multiply(self._left._inner, self._right._inner),
                base = self._left.base
            )
        else:
            return None
