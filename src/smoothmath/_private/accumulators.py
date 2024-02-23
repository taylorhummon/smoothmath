from __future__ import annotations
from typing import TYPE_CHECKING, Iterable
import smoothmath._private.expression.variable as va
import smoothmath._private.expression as ex
if TYPE_CHECKING:
    from smoothmath import Expression
    from smoothmath.expression import Variable


class NumericPartialsAccumulator:
    def __init__(
        self: NumericPartialsAccumulator
    ) -> None:
        self._numeric_partials: dict[str, float]
        self._numeric_partials = {}

    def add_to(
        self: NumericPartialsAccumulator,
        variable: Variable | str,
        contribution: float
    ) -> None:
        variable_name = va.get_variable_name(variable)
        existing = self._numeric_partials.get(variable_name, 0)
        self._numeric_partials[variable_name] = existing + contribution

    def numeric_partials_for(
        self: NumericPartialsAccumulator,
        variable_names: Iterable[str]
    ) -> dict[str, float]:
        results: dict[str, float]
        results = {}
        for variable_name in variable_names:
            results[variable_name] = self._numeric_partials.get(variable_name, 0)
        return results


class SyntheticPartialsAccumulator:
    def __init__(
        self: SyntheticPartialsAccumulator,
    ) -> None:
        self._synthetic_partials: dict[str, Expression]
        self._synthetic_partials = {}

    def add_to(
        self: SyntheticPartialsAccumulator,
        variable: Variable | str,
        contribution: Expression
    ) -> None:
        variable_name = va.get_variable_name(variable)
        existing = self._synthetic_partials.get(variable_name, None)
        next = existing + contribution if existing is not None else contribution
        self._synthetic_partials[variable_name] = next

    def synthetic_partials_for(
        self: SyntheticPartialsAccumulator,
        variable_names: Iterable[str]
    ) -> dict[str, Expression]:
        results: dict[str, Expression]
        results = {}
        for variable_name in variable_names:
            optional = self._synthetic_partials.get(variable_name, None)
            if optional is None:
                results[variable_name] = ex.Constant(0)
            else:
                results[variable_name] = optional
        return results
