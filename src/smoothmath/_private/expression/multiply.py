from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Optional
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.base_expression as base
from smoothmath._private.math_functions import add, multiply
from smoothmath._private.utilities import (
    is_even,
    list_without_entry_at,
    group_by_key, map_dictionary_values,
    first_of_given_type, partition_by_given_type
)
if TYPE_CHECKING:
    from smoothmath import RealNumber
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


class Multiply(base.NAryExpression):
    """
    The product of several expressions.

    :param \\*args: the expressions being multiplied together
    """

    ## Evaluation ##

    def _verify_domain_constraints(
        self: Multiply,
        *inner_values: RealNumber
    ) -> None:
        pass

    def _value_formula(
        self: Multiply,
        *inner_values: RealNumber
    ) -> RealNumber:
        return multiply(*inner_values)

    ## Partials and Differentials ##

    def _local_partial(
        self: Multiply,
        point: sm.Point,
        variable: str
    ) -> RealNumber:
        inner_values = [inner._evaluate(point) for inner in self._inners]
        return add(*(
            multiply(
                inner._local_partial(point, variable),
                *list_without_entry_at(inner_values, i)
            )
            for (i, inner) in enumerate(self._inners)
        ))

    def _synthetic_partial(
        self: Multiply,
        variable: str
    ) -> sm.Expression:
        return ex.Add(*(
            ex.Multiply(
                inner._synthetic_partial(variable),
                *list_without_entry_at(self._inners, i)
            )
            for (i, inner) in enumerate(self._inners)
        ))

    def _compute_local_differential(
        self: Multiply,
        builder: LocalDifferentialBuilder,
        accumulated: RealNumber
    ) -> None:
        inner_values = [inner._evaluate(builder.point) for inner in self._inners]
        for i, inner in enumerate(self._inners):
            next_accumulated = multiply(
                accumulated,
                *list_without_entry_at(inner_values, i)
            )
            inner._compute_local_differential(builder, next_accumulated)

    def _compute_global_differential(
        self: Multiply,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        for i, inner in enumerate(self._inners):
            next_accumulated = ex.Multiply(
                accumulated,
                *list_without_entry_at(self._inners, i)
            )
            inner._compute_global_differential(builder, next_accumulated)

    ## Normalization and Reduction ##

    @property
    def _reducers(
        self: Multiply
    ) -> list[Callable[[], Optional[sm.Expression]]]:
        return [
            self._reduce_by_flattening_nested_products,
            self._reduce_product_when_multiplying_by_zero,
            self._reduce_product_by_eliminating_ones,
            self._reduce_product_by_eliminating_negations,
            self._reduce_product_by_consolidating_nth_powers,
            self._reduce_product_by_consolidating_nth_roots,
            self._reduce_product_by_consolidating_exponentials,
            self._reduce_product_by_consolidating_constants
        ]

    def _reduce_by_flattening_nested_products(
        self: Multiply
    ) -> Optional[sm.Expression]:
        pair_or_none = first_of_given_type(self._inners, Multiply)
        if pair_or_none is None:
            return None
        i, inner_multiply = pair_or_none
        nested_inners = inner_multiply._inners
        before = self._inners[:i]
        after = self._inners[i + 1:]
        return Multiply(*before, *nested_inners, *after)

    def _reduce_product_when_multiplying_by_zero(
        self: Multiply
    ) -> Optional[sm.Expression]:
        if any(
            isinstance(inner, ex.Constant) and inner.value == 0
            for inner in self._inners
        ):
            return ex.Constant(0)
        else:
            return None

    def _reduce_product_by_eliminating_ones(
        self: Multiply
    ) -> Optional[sm.Expression]:
        non_ones: list[sm.Expression]
        non_ones = [
            inner
            for inner in self._inners
            if not (isinstance(inner, ex.Constant) and inner.value == 1)
        ]
        if len(non_ones) == len(self._inners):
            return None
        return Multiply(*non_ones)

    def _reduce_product_by_eliminating_negations(
        self: Multiply
    ) -> Optional[sm.Expression]:
        negations: list[ex.Negation]; non_negations: list[sm.Expression]
        negations, non_negations = partition_by_given_type(self._inners, ex.Negation)
        negations_count = len(negations)
        if negations_count == 0:
            return None
        negation_inners = (negation._inner for negation in negations)
        if is_even(negations_count):
            return Multiply(*non_negations, *negation_inners)
        else: # negations_count is odd
            return Multiply(*non_negations, *negation_inners, ex.Constant(-1))

    def _reduce_product_by_consolidating_nth_powers(
        self: Multiply
    ) -> Optional[sm.Expression]:
        nth_powers: list[ex.NthPower]; non_nth_powers: list[sm.Expression]
        nth_powers, non_nth_powers = partition_by_given_type(self._inners, ex.NthPower)
        if len(nth_powers) <= 1:
            return None
        nth_powers_by_n = group_by_key(nth_powers, lambda nth_power: nth_power.n)
        if all(len(nth_powers) <= 1 for nth_powers in nth_powers_by_n.values()):
            return None
        nth_power_inners_by_n = map_dictionary_values(
            nth_powers_by_n,
            lambda _, nth_powers: [nth_power._inner for nth_power in nth_powers]
        )
        consolidated_nth_powers = [
            ex.NthPower(Multiply(*inners), n)
            for n, inners in nth_power_inners_by_n.items()
        ]
        return Multiply(*non_nth_powers, *consolidated_nth_powers)

    def _reduce_product_by_consolidating_nth_roots(
        self: Multiply
    ) -> Optional[sm.Expression]:
        nth_roots: list[ex.NthRoot]; non_nth_roots: list[sm.Expression]
        nth_roots, non_nth_roots = partition_by_given_type(self._inners, ex.NthRoot)
        if len(nth_roots) <= 1:
            return None
        nth_roots_by_n = group_by_key(nth_roots, lambda nth_root: nth_root.n)
        if all(len(nth_roots) <= 1 for nth_roots in nth_roots_by_n.values()):
            return None
        nth_root_inners_by_n = map_dictionary_values(
            nth_roots_by_n,
            lambda _, nth_roots: [nth_root._inner for nth_root in nth_roots]
        )
        consolidated_nth_roots = [
            ex.NthRoot(Multiply(*inners), n)
            for n, inners in nth_root_inners_by_n.items()
        ]
        return Multiply(*non_nth_roots, *consolidated_nth_roots)

    def _reduce_product_by_consolidating_exponentials(
        self: Multiply
    ) -> Optional[sm.Expression]:
        exponentials: list[ex.Exponential]; non_exponentials: list[sm.Expression]
        exponentials, non_exponentials = partition_by_given_type(self._inners, ex.Exponential)
        if len(exponentials) <= 1:
            return None
        exponentials_by_base = group_by_key(exponentials, lambda exponential: exponential.base)
        if all(len(exponentials) <= 1 for exponentials in exponentials_by_base.values()):
            return None
        exponential_inners_by_base = map_dictionary_values(
            exponentials_by_base,
            lambda _, exponentials: [exponential._inner for exponential in exponentials]
        )
        consolidated_exponentials = [
            ex.Exponential(ex.Add(*inners), base = base)
            for base, inners in exponential_inners_by_base.items()
        ]
        return Multiply(*non_exponentials, *consolidated_exponentials)

    def _reduce_product_by_consolidating_constants(
        self: Multiply
    ) -> Optional[sm.Expression]:
        constants: list[ex.Constant]; non_constants: list[sm.Expression]
        constants, non_constants = partition_by_given_type(self._inners, ex.Constant)
        if len(constants) <= 1:
            return None
        product = multiply(*(constant.value for constant in constants))
        return Multiply(*non_constants, ex.Constant(product))

    def _normalize_fully_reduced(
        self: Multiply
    ) -> sm.Expression:
        reciprocals: list[ex.Reciprocal]; non_reciprocals: list[sm.Expression]
        reciprocals, non_reciprocals = partition_by_given_type(self._inners, ex.Reciprocal)
        numerator_terms = [non_reciprocal._normalize() for non_reciprocal in non_reciprocals]
        denominator_terms = [reciprocal._inner._normalize() for reciprocal in reciprocals]
        numerator_count = len(numerator_terms)
        denominator_count = len(denominator_terms)
        if numerator_count >= 1 and denominator_count >= 1:
            return ex.Divide(
                _simplified_Multiply(numerator_terms),
                _simplified_Multiply(denominator_terms)
            )
        elif numerator_count >= 1 and denominator_count == 0:
            return _simplified_Multiply(numerator_terms)
        elif numerator_count == 0 and denominator_count >= 1:
            return ex.Reciprocal(_simplified_Multiply(denominator_terms))
        else: # numerator_count == 0 and denominator_count == 0
            return ex.Constant(1)


def _simplified_Multiply(
    terms: list[sm.Expression]
) -> sm.Expression:
    term_count = len(terms)
    if term_count == 0:
        return ex.Constant(1)
    elif term_count == 1:
        return terms[0]
    else: # inners_count >= 2
        return Multiply(*terms)
