from __future__ import annotations
import smoothmath as sm
import smoothmath.expression as ex
from smoothmath._private.local_differential import LocalDifferentialBuilder
from smoothmath._private.reducers import reduce_synthetic
from smoothmath._private.utilities import get_variable_name


class GlobalDifferential:
    def __init__(
        self: GlobalDifferential,
        original_expression: sm.Expression,
        synthetic_partials: dict[str, sm.Expression]
    ) -> None:
        self.original_expression: sm.Expression
        self.original_expression = original_expression
        self._synthetic_partials: dict[str, sm.Expression]
        self._synthetic_partials = synthetic_partials.copy()

    def component_at(
        self: GlobalDifferential,
        point: sm.Point,
        variable: ex.Variable | str
    ) -> sm.real_number:
        return self.component(variable).at(point)

    def component(
        self: GlobalDifferential,
        variable: ex.Variable | str
    ) -> sm.GlobalPartial:
        variable_name = get_variable_name(variable)
        existing = self._synthetic_partials.get(variable_name, None)
        synthetic_partial = existing if existing is not None else ex.Constant(0)
        return sm.GlobalPartial(self.original_expression, synthetic_partial)

    def at(
        self: GlobalDifferential,
        point: sm.Point
    ) -> sm.LocalDifferential:
        self.original_expression.evaluate(point)
        builder = LocalDifferentialBuilder(self.original_expression, point)
        for variable_name, synthetic_partial in self._synthetic_partials.items():
            local_partial = synthetic_partial.evaluate(point)
            builder.add_to(variable_name, local_partial)
        return builder.build()

    def __eq__(
        self: GlobalDifferential,
        other: GlobalDifferential
    ) -> bool:
        # We'll assume correctness of the synthetic partials, so it suffices to compare
        # the original expressions.
        return self.original_expression == other.original_expression

    def __str__(
        self: GlobalDifferential
    ) -> str:
        return f"({self._partials_string()})"

    def __repr__(
        self: GlobalDifferential
    ) -> str:
        return f"(original: {self.original_expression}; partials: {self._partials_string()})"

    def _partials_string(
        self: GlobalDifferential
    ) -> str:
        return ", ".join(
            f"{variable_name}-partial = {synthetic_partial}"
            for variable_name, synthetic_partial in self._synthetic_partials.items()
        )


class GlobalDifferentialBuilder:
    def __init__(
        self: GlobalDifferentialBuilder,
        original_expression: sm.Expression
    ) -> None:
        self.original_expression: sm.Expression
        self.original_expression = original_expression
        self._synthetic_partials: dict[str, sm.Expression]
        self._synthetic_partials = {}

    def add_to(
        self: GlobalDifferentialBuilder,
        variable: ex.Variable | str,
        contribution: sm.Expression
    ) -> None:
        variable_name = get_variable_name(variable)
        existing = self._synthetic_partials.get(variable_name, None)
        next = existing + contribution if existing is not None else contribution
        self._synthetic_partials[variable_name] = next

    def build(
        self: GlobalDifferentialBuilder
    ) -> GlobalDifferential:
        reduced_synthetic_partials = _reduce_synthetic_partials(self._synthetic_partials)
        return GlobalDifferential(self.original_expression, reduced_synthetic_partials)


def _reduce_synthetic_partials(
    synthetic_partials: dict[str, sm.Expression]
) -> dict[str, sm.Expression]:
    reduced_synthetic_partials = {}
    for variable_name, synthetic_partial in synthetic_partials.items():
        reduced_synthetic_partials[variable_name] = reduce_synthetic(synthetic_partial)
    return reduced_synthetic_partials
