from __future__ import annotations
from typing import TYPE_CHECKING, Callable
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.base_expression as base
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


class Multiply(base.BinaryExpression):
    def _verify_domain_constraints(
        self: Multiply,
        left_value: sm.real_number,
        right_value: sm.real_number
    ) -> None:
        pass

    def _value_formula(
        self: Multiply,
        left_value: sm.real_number,
        right_value: sm.real_number
    ) -> sm.real_number:
        return left_value * right_value

    def _evaluate(
        self: Multiply,
        point: sm.Point
    ) -> sm.real_number:
        inner_pair_or_none = self._get_inner_inner_pair_or_none(point)
        if inner_pair_or_none == None:
            self._value = 0
        else: # inner_pair_or_none is the pair (left_value, right_value)
            left_value, right_value = inner_pair_or_none
            self._value = left_value * right_value
        return self._value

    def _local_partial(
        self: Multiply,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        inner_pair_or_none = self._get_inner_inner_pair_or_none(point)
        if inner_pair_or_none == None:
            return 0
        else: # inner_pair_or_none is the pair (left_value, right_value)
            left_value, right_value = inner_pair_or_none
            left_partial = self._left._local_partial(point, with_respect_to)
            right_partial = self._right._local_partial(point, with_respect_to)
            return right_value * left_partial + left_value * right_partial

    def _synthetic_partial(
        self: Multiply,
        with_respect_to: str
    ) -> sm.Expression:
        left_partial = self._left._synthetic_partial(with_respect_to)
        right_partial = self._right._synthetic_partial(with_respect_to)
        return ex.Plus(
            ex.Multiply(self._right, left_partial),
            ex.Multiply(self._left, right_partial)
        )

    def _compute_local_differential(
        self: Multiply,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        inner_pair_or_none = self._get_inner_inner_pair_or_none(builder.point)
        if inner_pair_or_none == None:
            return
        else: # inner_pair_or_none is the pair (left_value, right_value)
            left_value, right_value = inner_pair_or_none
            self._left._compute_local_differential(builder, right_value * accumulated)
            self._right._compute_local_differential(builder, left_value * accumulated)

    def _compute_global_differential(
        self: Multiply,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        self._left._compute_global_differential(builder, ex.Multiply(self._right, accumulated))
        self._right._compute_global_differential(builder, ex.Multiply(self._left, accumulated))

    # the following method is used to allow shirt-circuiting of either left * 0 or 0 * right
    def _get_inner_inner_pair_or_none(
        self: Multiply,
        point: sm.Point
    ) -> tuple[sm.real_number, sm.real_number] | None:
        try:
            left_value = self._left._evaluate(point)
        except sm.DomainError as error:
            try:
                _right_value = self._right._evaluate(point)
            except sm.DomainError:
                raise error
            if _right_value == 0:
                return None
            raise
        try:
            right_value = self._right._evaluate(point)
        except sm.DomainError as error:
            try:
                _left_value = self._left._evaluate(point)
            except sm.DomainError:
                raise error
            if _left_value == 0:
                return None
            raise
        return (left_value, right_value)

    @property
    def _reducers(
        self: Multiply
    ) -> list[Callable[[], sm.Expression | None]]:
        return [
            self._reduce_by_associating_multiply_left,
            self._reduce_one_times_u,
            self._reduce_zero_times_u,
            self._reduce_negative_one_times_u,
            self._reduce_by_commuting_constant_left_across_multiply,
            self._reduce_negation_of_u__times_v,
            self._reduce_u_times_negation_of_v,
            self._reduce_by_commuting_reciprocal_left_across_multiply,
            self._reduce_product_of_reciprocals,
            self._reduce_product_of_nth_powers,
            self._reduce_product_of_nth_roots,
            self._reduce_product_of_exponentials
        ]

    # Multiply(u, Multiply(v, w)) => Multiply(Multiply(u, v), w)
    def _reduce_by_associating_multiply_left(
        self: Multiply
    ) -> sm.Expression | None:
        if isinstance(self._right, ex.Multiply):
            return ex.Multiply(
                ex.Multiply(self._left, self._right._left),
                self._right._right
            )
        else:
            return None

    # Multiply(Constant(1), u) => u
    def _reduce_one_times_u(
        self: Multiply
    ) -> sm.Expression | None:
        if (
            isinstance(self._left, ex.Constant) and
            self._left.value == 1
        ):
            return self._right
        else:
            return None

    # Multiply(Constant(0), u) => Constant(0)
    def _reduce_zero_times_u(
        self: Multiply
    ) -> sm.Expression | None:
        if (
            isinstance(self._left, ex.Constant) and
            self._left.value == 0
        ):
            return ex.Constant(0)
        else:
            return None

    # Multiply(Constant(-1), u) => Negation(u)
    def _reduce_negative_one_times_u(
        self: Multiply
    ) -> sm.Expression | None:
        if (
            isinstance(self._left, ex.Constant) and
            self._left.value == -1
        ):
            return ex.Negation(self._right)
        else:
            return None

    # Multiply(u, Constant(c)) => Multiply(Constant(c), u)
    def _reduce_by_commuting_constant_left_across_multiply(
        self: Multiply
    ) -> sm.Expression | None:
        if (
            isinstance(self._right, ex.Constant) and
            not isinstance(self._left, (ex.Constant, ex.Reciprocal, ex.Multiply))
        ):
            return ex.Multiply(self._right, self._left)
        else:
            return None

    # Multiply(Negation(u), v) => Negation(Multiply(u, v))
    def _reduce_negation_of_u__times_v(
        self: Multiply
    ) -> sm.Expression | None:
        if (
            isinstance(self._left, ex.Negation)
        ):
            return ex.Negation(ex.Multiply(self._left._inner, self._right))
        else:
            return None

    # Multiply(u, Negation(v)) => Negation(Multiply(u, v))
    def _reduce_u_times_negation_of_v(
        self: Multiply
    ) -> sm.Expression | None:
        if isinstance(self._right, ex.Negation):
            return ex.Negation(ex.Multiply(self._left, self._right._inner))
        else:
            return None

    # Multiply(u, Reciprocal(v)) => Multiply(Reciprocal(v), u)
    def _reduce_by_commuting_reciprocal_left_across_multiply(
        self: Multiply
    ) -> sm.Expression | None:
        if (
            isinstance(self._right, ex.Reciprocal) and
            not isinstance(self._left, (ex.Reciprocal, ex.Multiply))
        ):
            return ex.Multiply(self._right, self._left)
        else:
            return None

    # Multiply(Reciprocal(u), Reciprocal(v)) => Reciprocal(Multiply(u, v))
    def _reduce_product_of_reciprocals(
        self: Multiply
    ) -> sm.Expression | None:
        if (
            isinstance(self._left, ex.Reciprocal) and
            isinstance(self._right, ex.Reciprocal)
        ):
            return ex.Reciprocal(ex.Multiply(self._left._inner, self._right._inner))
        else:
            return None

    # Multiply(NthPower(u, n), NthPower(v, n)) => NthPower(Multiply(u, v), n)
    def _reduce_product_of_nth_powers(
        self: Multiply
    ) -> sm.Expression | None:
        if (
            isinstance(self._left, ex.NthPower) and
            isinstance(self._right, ex.NthPower) and
            self._left.n == self._right.n
        ):
            return ex.NthPower(
                ex.Multiply(self._left._inner, self._right._inner),
                self._left.n
            )
        else:
            return None

    # Multiply(NthRoot(u, n), NthRoot(v, n)) => NthRoot(Multiply(u, v), n)
    def _reduce_product_of_nth_roots(
        self: Multiply
    ) -> sm.Expression | None:
        if (
            isinstance(self._left, ex.NthRoot) and
            isinstance(self._right, ex.NthRoot) and
            self._left.n == self._right.n
        ):
            return ex.NthRoot(
                ex.Multiply(self._left._inner, self._right._inner),
                self._left.n
            )
        else:
            return None

    # Multiply(Exponential(u), Exponential(v)) => Exponential(Plus(u, v))
    def _reduce_product_of_exponentials(
        self: Multiply
    ) -> sm.Expression | None:
        if (
            isinstance(self._left, ex.Exponential) and
            isinstance(self._right, ex.Exponential) and
            self._left.base == self._right.base
        ):
            return ex.Exponential(
                ex.Plus(self._left._inner, self._right._inner),
                base = self._left.base
            )
        else:
            return None
