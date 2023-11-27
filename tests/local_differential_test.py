from smoothmath.local_differential import LocalDifferential
from smoothmath.expressions import Variable


def test_LocalDifferential():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    local_differential = LocalDifferential()
    local_differential._add_to(x, 3)
    local_differential._add_to(y, 4)
    local_differential._add_to(y, 2)
    assert local_differential.partial_with_respect_to(w) == 0
    assert local_differential.partial_with_respect_to(x) == 3
    assert local_differential.partial_with_respect_to(y) == 6
    assert local_differential.partial_with_respect_to("y") == 6
