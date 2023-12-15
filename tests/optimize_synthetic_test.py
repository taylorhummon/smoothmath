from smoothmath.expression import (
    Constant, Variable,
    Negation, Reciprocal, Cosine, Sine,
    NthPower, NthRoot, Exponential, Logarithm,
    Plus, Minus, Multiply, Divide, Power
)
from smoothmath._private.optimize_synthetic import (
    optimize_synthetic, _reduce_synthetic,
    _disassemble_minus_and_divide, _reassemble_minus_and_divide
)


def test_reduce_synthetic():
    x = Variable("x")
    y = Variable("y")
    z = Constant(0) + x
    assert _reduce_synthetic(z) == x
    z = x * Constant(1)
    assert _reduce_synthetic(z) == x
    z = x * Constant(0)
    assert _reduce_synthetic(z) == Constant(0)
    z = x + NthPower(Plus(Constant(1), Constant(2)), n = 2)
    assert _reduce_synthetic(z) == x + Constant(9)
    z = Reciprocal(NthPower(Reciprocal(x), n = 2))
    assert _reduce_synthetic(z) == NthPower(x, n = 2)
    z = Multiply(NthPower(Reciprocal(x), n = 2), NthPower(Reciprocal(y), n = 2))
    assert _reduce_synthetic(z) == Reciprocal(NthPower(Multiply(x, y), n = 2))
    z = Multiply(Constant(1) + x + Constant(-1), Constant(2))
    assert _reduce_synthetic(z) == Multiply(Constant(2), x)
