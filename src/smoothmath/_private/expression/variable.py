from __future__ import annotations
from typing import TYPE_CHECKING, Any
import smoothmath as sm
import smoothmath.expression as ex
from smoothmath._private.expression.base import NullaryExpression
if TYPE_CHECKING:
    from smoothmath._private.local_differential import LocalDifferentialBuilder
    from smoothmath._private.global_differential import GlobalDifferentialBuilder


class Variable(NullaryExpression):
    def __init__(
        self: Variable,
        name: str
    ) -> None:
        super().__init__(lacks_variables = False)
        if not name:
            raise Exception("Variables must be given a non-blank name")
        self.name: str
        self.name = name
        self._cached_hash: int | None
        self._cached_hash = None

    def __eq__(
        self: Variable,
        other: Any
    ) -> bool:
        return isinstance(other, Variable) and (other.name == self.name)

    def __hash__(
        self: Variable
    ) -> int:
        if self._cached_hash is None:
            self._cached_hash = hash(self.name)
        return self._cached_hash

    def __str__(
        self: Variable
    ) -> str:
        return f"Variable(\"{self.name}\")"

    def _evaluate(
        self: Variable,
        point: sm.Point
    ) -> sm.real_number:
        return point.value_for(self.name)

    def _local_partial(
        self: Variable,
        point: sm.Point,
        with_respect_to: str
    ) -> sm.real_number:
        if self.name == with_respect_to:
            return 1
        else:
            return 0

    def _synthetic_partial(
        self: Variable,
        with_respect_to: str
    ) -> sm.Expression:
        if self.name == with_respect_to:
            return ex.Constant(1)
        else:
            return ex.Constant(0)

    def _compute_local_differential(
        self: Variable,
        builder: LocalDifferentialBuilder,
        point: sm.Point,
        accumulated: sm.real_number
    ) -> None:
        builder.add_to(self, accumulated)

    def _compute_global_differential(
        self: Variable,
        builder: GlobalDifferentialBuilder,
        accumulated: sm.Expression
    ) -> None:
        builder.add_to(self, accumulated)
