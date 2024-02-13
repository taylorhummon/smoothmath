from __future__ import annotations
from typing import TYPE_CHECKING, Any
import smoothmath._private.utilities as util
if TYPE_CHECKING:
    from smoothmath import RealNumber, Point, Expression
    from smoothmath.expression import Variable


class LocalDifferential:
    """
    The differential of an expression localized at a point.
    """

    def __init__(
        self: LocalDifferential,
        expression: Expression,
        point: Point,
        local_partials: dict[str, RealNumber]
    ) -> None:
        self._original_expression: Expression
        self._original_expression = expression
        self._point: Point
        self._point = point
        self._local_partials: dict[str, RealNumber]
        self._local_partials = local_partials.copy()

    def component(
        self: LocalDifferential,
        variable: Variable | str
    ) -> RealNumber:
        """
        The component of the differential.

        :param variable: selects which component
        """
        variable_name = util.get_variable_name(variable)
        return self._local_partials.get(variable_name, 0)

    def __eq__(
        self: LocalDifferential,
        other: Any
    ) -> bool:
        return (
            (other.__class__ == self.__class__) and
            (self._original_expression == other._original_expression) and
            (self._point == other._point) and
            (self._local_partials == other._local_partials)
        )

    def __hash__(
        self: LocalDifferential
    ) -> int:
        data = tuple(sorted(self._local_partials.items()))
        return hash((self._original_expression, self._point, data))

    def __str__(
        self: LocalDifferential
    ) -> str:
        return f"({self._partials_string()})"

    def __repr__(
        self: LocalDifferential
    ) -> str:
        dictionary = {
            "original": self._original_expression,
            "point": self._point,
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
        expression: Expression,
        point: Point
    ) -> None:
        self._original_expression: Expression
        self._original_expression = expression
        self.point: Point
        self.point = point
        self._local_partials: dict[str, RealNumber]
        self._local_partials = {}

    def add_to(
        self: LocalDifferentialBuilder,
        variable: Variable | str,
        contribution: RealNumber
    ) -> None:
        variable_name = util.get_variable_name(variable)
        existing = self._local_partials.get(variable_name, 0)
        self._local_partials[variable_name] = existing + contribution

    def build(
        self: LocalDifferentialBuilder
    ) -> LocalDifferential:
        return LocalDifferential(self._original_expression, self.point, self._local_partials)
