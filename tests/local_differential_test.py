from smoothmath.local_differential import LocalDifferential
from smoothmath.expressions import Variable, Constant


def test_LocalDifferential():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    local_differential = LocalDifferential(Constant(17))
    local_differential._add_to(x, 3)
    local_differential._add_to(y, 4)
    local_differential._add_to(y, 2)
    local_differential._freeze()
    assert local_differential.component(w) == 0
    assert local_differential.component(x) == 3
    assert local_differential.component(y) == 6
    assert local_differential.component("y") == 6
