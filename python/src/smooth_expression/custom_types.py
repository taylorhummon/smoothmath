from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.variable import Variable

type Real = float | int
type VariableOrName = Variable | str
