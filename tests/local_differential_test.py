from smoothmath.local_differential import LocalDifferential, LocalDifferentialBuilder
from smoothmath.expressions import Variable, Constant


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
