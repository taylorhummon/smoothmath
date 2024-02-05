from __future__ import annotations
from typing import TYPE_CHECKING, Callable
import smoothmath as sm
import smoothmath.expression as ex
import smoothmath._private.base_expression as base
from smoothmath._private.math_functions import add
from smoothmath._private.utilities import (
    group_by_key, map_dictionary_values,
    first_of_given_type, partition_by_given_type
)
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


class Add(base.NAryExpression):

    ## Evaluation ##

    def _verify_domain_constraints(
        self: Add,
        *inner_values: sm.real_number
    ) -> None:
        pass

    def _value_formula(
        self: Add,
        *inner_values: sm.real_number
    ) -> sm.real_number:
        return add(*inner_values)

    ## Partials and Differentials ##

    def _local_partial(
        self: Add,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        return add(*(
            inner._local_partial(point, with_respect_to)
            for inner in self._inners
        ))

    def _synthetic_partial(
        self: Add,
        with_respect_to: str
    ) -> sm.Expression:
        return ex.Add(*(
            inner._synthetic_partial(with_respect_to)
            for inner in self._inners
        ))

    def _compute_local_differential(
        self: Add,
        builder: LocalDifferentialBuilder,
        accumulated: sm.real_number
    ) -> None:
        for inner in self._inners:
            inner._compute_local_differential(builder, accumulated)

    def _compute_global_differential(
        self: Add,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        for inner in self._inners:
            inner._compute_global_differential(builder, accumulated)

    ## Normalization and Reduction ##

    @property
    def _reducers(
        self: Add
    ) -> list[Callable[[], sm.Expression | None]]:
        return [
            self._reduce_by_flattening_nested_sums,
            self._reduce_sum_by_eliminating_zeros,
            self._reduce_sum_by_consolidating_logarithms,
            self._reduce_sum_by_consolidating_constants
        ]

    def _reduce_by_flattening_nested_sums(
        self: Add
    ) -> sm.Expression | None:
        pair_or_none = first_of_given_type(self._inners, Add)
        if pair_or_none is None:
            return None
        i, inner_add = pair_or_none
        nested_inners = inner_add._inners
        before = self._inners[:i]
        after = self._inners[i + 1:]
        return Add(*before, *nested_inners, *after)

    def _reduce_sum_by_eliminating_zeros(
        self: Add
    ) -> sm.Expression | None:
        non_zeros: list[sm.Expression]
        non_zeros = [
            inner
            for inner in self._inners
            if not (isinstance(inner, ex.Constant) and inner.value == 0)
        ]
        if len(non_zeros) == len(self._inners):
            return None
        return Add(*non_zeros)

    def _reduce_sum_by_consolidating_logarithms(
        self: Add
    ) -> sm.Expression | None:
        logarithms: list[ex.Logarithm]
        non_logarithms: list[sm.Expression]
        logarithms, non_logarithms = partition_by_given_type(self._inners, ex.Logarithm)
        if len(logarithms) <= 1:
            return None
        logarithms_by_base = group_by_key(logarithms, lambda logarithm: logarithm.base)
        if all(len(logarithms) <= 1 for logarithms in logarithms_by_base.values()):
            return None
        logarithm_inners_by_base = map_dictionary_values(
            logarithms_by_base,
            lambda _, logarithms: [logarithm._inner for logarithm in logarithms]
        )
        consolidated_logarithms = [
            ex.Logarithm(ex.Multiply(*inners), base = base)
            for base, inners in logarithm_inners_by_base.items()
        ]
        return Add(*non_logarithms, *consolidated_logarithms)

    def _reduce_sum_by_consolidating_constants(
        self: Add
    ) -> sm.Expression | None:
        constants: list[ex.Constant]
        non_constants: list[sm.Expression]
        constants, non_constants = partition_by_given_type(self._inners, ex.Constant)
        if len(constants) <= 1:
            return None
        summed = add(*(constant.value for constant in constants))
        return Add(*non_constants, ex.Constant(summed))

    def _normalize_fully_reduced(
        self: Add
    ) -> sm.Expression:
        negations: list[ex.Negation]
        non_negations: list[sm.Expression]
        negations, non_negations = partition_by_given_type(self._inners, ex.Negation)
        type_i_terms = [term._normalize() for term in non_negations]
        type_ii_terms = [negation._inner._normalize() for negation in negations]
        type_i_count = len(type_i_terms)
        type_ii_count = len(type_ii_terms)
        if type_i_count >= 1 and type_ii_count >= 1:
            return ex.Minus(
                _simplified_Add(type_i_terms),
                _simplified_Add(type_ii_terms)
            )
        elif type_i_count >= 1 and type_ii_count == 0:
            return _simplified_Add(type_i_terms)
        elif type_i_count == 0 and type_ii_count >= 1:
            return ex.Negation(_simplified_Add(type_ii_terms))
        else: # type_i_count == 0 and type_ii_count == 0
            return ex.Constant(0)


def _simplified_Add(
    terms: list[sm.Expression]
) -> sm.Expression:
    term_count = len(terms)
    if term_count == 0:
        return ex.Constant(0)
    elif term_count == 1:
        return terms[0]
    else: # inners_count >= 2
        return Add(*terms)
