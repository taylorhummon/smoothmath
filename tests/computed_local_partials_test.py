from smoothmath.computed_local_partials import ComputedLocalPartials
from smoothmath.expressions import Variable


def test_ComputedLocalPartials():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    computed_local_partials = ComputedLocalPartials()
    computed_local_partials._add_to(x, 3)
    computed_local_partials._add_to(y, 4)
    computed_local_partials._add_to(y, 2)
    assert computed_local_partials.partial_with_respect_to(w) == 0
    assert computed_local_partials.partial_with_respect_to(x) == 3
    assert computed_local_partials.partial_with_respect_to(y) == 6
    assert computed_local_partials.partial_with_respect_to("y") == 6
