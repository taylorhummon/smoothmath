from __future__ import annotations
from typing import TYPE_CHECKING, Any
import re
import smoothmath.expression as ex
import smoothmath._private.base_expression as base
if TYPE_CHECKING:
    from smoothmath import RealNumber, Expression, Point
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


alphanumeric_pattern = re.compile(r"\A\w*\Z")


class Variable(base.Expression):
    """
    A variable.

    :param name: the variable's name
    """

    def __init__(
        self: Variable,
        name: str
    ) -> None:
        super().__init__(lacks_variables = False)
        if (not name) or (alphanumeric_pattern.match(name) is None):
            raise Exception(f"Illegal variable name: {name}")
        self.name: str
        self.name = name

    ## Evaluation ##

    def _reset_evaluation_cache(
        self: Variable
    ) -> None:
        pass

    def _evaluate(
        self: Variable,
        point: Point
    ) -> RealNumber:
        return point.coordinate(self.name)

    ## Partials and Differentials ##

    def _local_partial(
        self: Variable,
        point: Point,
        variable_name: str
    ) -> RealNumber:
        if self.name == variable_name:
            return 1
        else:
            return 0

    def _synthetic_partial(
        self: Variable,
        variable_name: str
    ) -> Expression:
        if self.name == variable_name:
            return ex.Constant(1)
        else:
            return ex.Constant(0)

    def _compute_local_differential(
        self: Variable,
        builder: LocalDifferentialBuilder,
        accumulated: RealNumber
    ) -> None:
        builder.add_to(self, accumulated)

    def _compute_global_differential(
        self: Variable,
        builder: GlobalDifferentialBuilder,
        accumulated: Expression
    ) -> None:
        builder.add_to(self, accumulated)

    ## Normalization and Reduction ##

    def _take_reduction_step(
        self: Variable
    ) -> Variable:
        self._is_fully_reduced = True
        return self

    def _normalize_fully_reduced(
        self: Variable
    ) -> Expression:
        return self

    ## Operations ##

    def __eq__(
        self: Variable,
        other: Any
    ) -> bool:
        return (other.__class__ == self.__class__) and (other.name == self.name)

    def __hash__(
        self: Variable
    ) -> int:
        return hash(("Variable", self.name))

    def __str__(
        self: Variable
    ) -> str:
        return f"Variable(\"{self.name}\")"

    def __repr__(
        self: Variable
    ) -> str:
        return f"Variable(\"{self.name}\")"
