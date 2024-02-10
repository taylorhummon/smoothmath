from __future__ import annotations
from typing import TYPE_CHECKING, Any
from smoothmath._private.utilities import get_variable_name
if TYPE_CHECKING:
    from smoothmath import RealNumber, Point, Expression
    from smoothmath.expression import Variable

class LocalDifferential:
    """
    The differential of an expression localized at a point.
    """

    def __init__(
        self: LocalDifferential,
        original_expression: Expression,
        point: Point,
        local_partials: dict[str, RealNumber]
    ) -> None:
        #: The expression which this is the differential of.
        self.original_expression: Expression
        self.original_expression = original_expression
        #: The point at which this differential is located.
        self.point: Point
        self.point = point
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
        original_expression: Expression,
        point: Point
    ) -> None:
        self._original_expression: Expression
        self._original_expression = original_expression
        self.point: Point
        self.point = point
        self._local_partials: dict[str, RealNumber]
        self._local_partials = {}

    def add_to(
        self: LocalDifferentialBuilder,
        variable: Variable | str,
        contribution: RealNumber
    ) -> None:
        variable_name = get_variable_name(variable)
        existing = self._local_partials.get(variable_name, 0)
        self._local_partials[variable_name] = existing + contribution

    def build(
        self: LocalDifferentialBuilder
    ) -> LocalDifferential:
        return LocalDifferential(self._original_expression, self.point, self._local_partials)
