from smoothmath.expression import Variable, Constant, Add, Reciprocal
from smoothmath._private.accumulators import LocalPartialsAccumulator, SyntheticPartialsAccumulator


def test_LocalPartialsAccumulator():
    x = Variable("x")
    y = Variable("y")
    accumulator = LocalPartialsAccumulator()
    accumulator.add_to(x, 3)
    accumulator.add_to(y, 5)
    accumulator.add_to("x", 1)
    assert accumulator.local_partials["x"] == 4
    assert accumulator.local_partials["y"] == 5


def test_SyntheticPartialsAccumulator():
    x = Variable("x")
    y = Variable("y")
    accumulator = SyntheticPartialsAccumulator()
    accumulator.add_to(x, Constant(3))
    accumulator.add_to(y, Variable("x"))
    accumulator.add_to("x", Reciprocal(Variable("x")))
    assert accumulator.synthetic_partials["x"] == Add(Constant(3), Reciprocal(Variable("x")))
    assert accumulator.synthetic_partials["y"] == Variable("x")
