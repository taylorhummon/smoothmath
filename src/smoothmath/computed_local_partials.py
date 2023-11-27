from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from smoothmath.types import real_number
    from smoothmath.expressions import Variable

import smoothmath.utilities as utilities


class ComputedLocalPartials:
    def __init__(
        self: ComputedLocalPartials
    ) -> None:
        self._partial_by_variable_name: dict[str, real_number]
        self._partial_by_variable_name = {}

    def partial_with_respect_to(
        self: ComputedLocalPartials,
        variable: Variable | str
    ) -> real_number:
        variable_name = utilities.get_variable_name(variable)
        return self._partial_by_variable_name.get(variable_name, 0)

    def _add_to(
        self: ComputedLocalPartials,
        variable: Variable,
        accumulated: real_number
    ) -> None:
        existing_value = self._partial_by_variable_name.get(variable.name, 0)
        self._partial_by_variable_name[variable.name] = existing_value + accumulated
