from typing import TYPE_CHECKING, Mapping
if TYPE_CHECKING:
    from src.smooth_expression.variable import Variable

type Real = float | int
type VariableValues = Mapping[Variable, Real]
