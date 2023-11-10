from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.smooth_expression.custom_types import VariableOrString

def _nameFromVariableOrName(
    variableOrName: VariableOrString
) -> str:
    if isinstance(variableOrName, str):
        return variableOrName
    else:
        return variableOrName.name
