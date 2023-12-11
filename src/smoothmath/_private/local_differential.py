from __future__ import annotations
from typing import Any
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
        other: Any
    ) -> bool:
        return (
            (other.__class__ == self.__class__) and
            (self.original_expression == other.original_expression) and
            (self.point == other.point) and
            (self._local_partials == other._local_partials)
        )

    def __hash__(
        self: LocalDifferential
    ) -> int:
        data = tuple(sorted(self._local_partials.items()))
        return hash((self.original_expression, self.point, data))

    def __str__(
        self: LocalDifferential
    ) -> str:
        return f"({self._partials_string()})"

    def __repr__(
        self: LocalDifferential
    ) -> str:
        dictionary = {
            "original": self.original_expression,
            "point": self.point,
            "partials": self._partials_string()
        }
        pairs_string = "; ".join(f"{key}: {value}" for key, value in dictionary.items())
        return f"({pairs_string})"

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
