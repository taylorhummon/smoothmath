from smoothmath.expression import (
    Constant, Variable,
    Negation, Reciprocal, Cosine, Sine,
    NthPower, NthRoot, Exponential, Logarithm,
    Plus, Minus, Multiply, Divide, Power
)
from smoothmath._private.optimize_synthetic import (
    optimize_synthetic, _fully_reduce_synthetic,
    _disassemble_minus_and_divide, _reassemble_minus_and_divide
)


def test_reducing_constant_expressions():
    x = Variable("x")
    z = x + NthPower(Plus(Constant(1), Constant(2)), n = 2)
    assert _fully_reduce_synthetic(z) == x + Constant(9)


def test_reducing_negation_and_reciprocal():
    x = Variable("x")
    z = Negation(Reciprocal(Negation(Reciprocal(Negation(x)))))
    assert _fully_reduce_synthetic(z) == Negation(x)


def test_reducing_plus_with_constants():
    x = Variable("x")
    z = Constant(0) + x
    assert _fully_reduce_synthetic(z) == x
    z = Constant(1) + x + Constant(2)
    assert _fully_reduce_synthetic(z) == x + Constant(3)


def test_reducing_plus_with_negation():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = (Negation(y) + w) + x
    assert _fully_reduce_synthetic(z) == w + (x + Negation(y))


def test_reducing_multiply_with_constants():
    x = Variable("x")
    z = x * Constant(1)
    assert _fully_reduce_synthetic(z) == x
    z = x * Constant(0)
    assert _fully_reduce_synthetic(z) == Constant(0)
    z = x * Constant(-1)
    assert _fully_reduce_synthetic(z) == Negation(x)
    # z = Constant(2) * x * Constant(3)
    # assert _fully_reduce_synthetic(z) == Constant(6) * x # !!! come back to this


def test_reducing_multiply_with_negation():
    x = Variable("x")
    z = Negation(x) * Negation(x)
    assert _fully_reduce_synthetic(z) == x * x


def test_reducing_multiply_with_reciprocal():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = x * (y * Reciprocal(w))
    assert _fully_reduce_synthetic(z) == (Reciprocal(w) * x) * y


def test_reducing_nth_root_of_mth_power():
    u = Variable("u")
    z = NthRoot(NthPower(u, n = 4), n = 6)
    assert _fully_reduce_synthetic(z) == NthPower(NthRoot(u, n = 3), n = 2)
