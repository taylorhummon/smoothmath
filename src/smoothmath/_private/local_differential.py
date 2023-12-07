from __future__ import annotations
import smoothmath as sm
import smoothmath.expression as ex
from smoothmath._private.utilities import get_variable_name


class LocalDifferential:
    def __init__(
        self: LocalDifferential,
        original_expression: sm.Expression,
        point: sm.Point,
        local_partials: dict[str, sm.real_number]
    ) -> None:
        self.original_expression: sm.Expression
        self.original_expression = original_expression
        self.point: sm.Point
        self.point = point
        self._local_partials: dict[str, sm.real_number]
        self._local_partials = local_partials.copy()

    def component(
        self: LocalDifferential,
        variable: ex.Variable | str
    ) -> sm.real_number:
        variable_name = get_variable_name(variable)
        return self._local_partials.get(variable_name, 0)

    def __eq__(
        self: LocalDifferential,
        other: LocalDifferential
    ) -> bool:
        # We'll assume correctness of the local partials, so it suffices to compare
        # the original expressions.
        return self.original_expression == other.original_expression

    def __str__(
        self: LocalDifferential
    ) -> str:
        return f"({self._partials_string()})"

    def __repr__(
        self: LocalDifferential
    ) -> str:
        data = {
            "original": self.original_expression,
            "point": self.point,
            "partials": self._partials_string()
        }
        inner = "; ".join(f"{key}: {value}" for key, value in data.items())
        return f"({inner})"

    def _partials_string(
        self: LocalDifferential
    ) -> str:
        return ", ".join(
            f"{variable_name}-partial = {local_partial}"
            for variable_name, local_partial in self._local_partials.items()
        )


class LocalDifferentialBuilder:
    def __init__(
        self: LocalDifferentialBuilder,
        original_expression: sm.Expression,
        point: sm.Point
    ) -> None:
        self._original_expression: sm.Expression
        self._original_expression = original_expression
        self.point: sm.Point
        self.point = point
        self._local_partials: dict[str, sm.real_number]
        self._local_partials = {}

    def add_to(
        self: LocalDifferentialBuilder,
        variable: ex.Variable | str,
        contribution: sm.real_number
    ) -> None:
        variable_name = get_variable_name(variable)
        existing = self._local_partials.get(variable_name, 0)
        self._local_partials[variable_name] = existing + contribution

    def build(
        self: LocalDifferentialBuilder
    ) -> LocalDifferential:
        return LocalDifferential(self._original_expression, self.point, self._local_partials)
