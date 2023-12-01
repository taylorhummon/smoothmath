from smoothmath.expression import Constant, Variable
from smoothmath._private.local_differential import LocalDifferentialBuilder


def test_LocalDifferential():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    builder = LocalDifferentialBuilder(Constant(17))
    builder.add_to(x, 3)
    builder.add_to(y, 4)
    builder.add_to(y, 2)
    local_differential = builder.build()
    assert local_differential.component(w) == 0
    assert local_differential.component(x) == 3
    assert local_differential.component(y) == 6
    assert local_differential.component("w") == 0
    assert local_differential.component("x") == 3
    assert local_differential.component("y") == 6
