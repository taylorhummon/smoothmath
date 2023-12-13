from smoothmath.expression import (
    Constant,
    Variable,
    Negation,
    Reciprocal,
    NthPower,
    NthRoot,
    Exponential,
    Logarithm,
    Cosine,
    Sine,
    Plus,
    Minus,
    Multiply,
    Divide,
    Power
)
from smoothmath._private.reducers import (
    reduce_synthetic,
    _reduce_expressions_that_lack_variables,
    _reduce_negation_of_negation_of_u,
    _reduce_reciprocal_of_reciprocal_of_u,
    _reduce_reciprocal_of_negation_of_u,
    _reduce_nth_power_where_n_is_one,
    _reduce_nth_power_of_mth_power_of_u,
    _reduce_nth_power_of_negation_of_u,
    _reduce_nth_power_of_reciprocal_of_u,
    _reduce_nth_root_where_n_is_one,
    _reduce_nth_root_of_mth_root_of_u,
    _reduce_odd_nth_root_of_negation_of_u,
    _reduce_nth_root_of_reciprocal_of_u,
    _reduce_nth_root_of_mth_power_of_u,
    _reduce_nth_power_of_mth_root_of_u,
    _reduce_exponential_of_negation_of_u,
    _reduce_logarithm_of_reciprocal_of_u,
    _reduce_logarithm_of_exponential_of_u,
    _reduce_exponential_of_logarithm_of_u,
    _reduce_cosine_of_negation_of_u,
    _reduce_sine_of_negation_of_u,
    _reduce_by_associating_plus_right,
    _reduce_by_commuting_constants_right_for_plus,
    _reduce_u_plus_zero,
    _reduce_u_minus_zero,
    _reduce_zero_minus_u,
    _reduce_negation_of_u_minus_v,
    _reduce_by_associating_multiply_left,
    _reduce_by_commuting_constants_left_for_multiply,
    _reduce_one_times_u,
    _reduce_zero_times_u,
    _reduce_negative_one_times_u,
    _reduce_product_of_reciprocals,
    _reduce_product_of_nth_powers,
    _reduce_product_of_nth_roots,
    _reduce_product_of_exponentials,
    _reduce_sum_of_logarithms,
    _reduce_u_over_one,
    _reduce_one_over_u,
    _reduce_negated_numerator,
    _reduce_negated_denominator,
    _reduce_reciprocal_of_u_over_v,
    _reduce_one_to_the_u,
    _reduce_u_to_the_n_at_least_two,
    _reduce_u_to_the_one,
    _reduce_u_to_the_zero,
    _reduce_u_to_the_negative_one,
    _reduce_u_to_the_one_half,
    _reduce_power_with_constant_base,
    _reduce_power_of_power
)


def test_reduce_synthetic():
    x = Variable("x")
    y = Variable("y")
    z = Constant(0) + x
    assert reduce_synthetic(z) == x
    z = x * Constant(1)
    assert reduce_synthetic(z) == x
    z = x * Constant(0)
    assert reduce_synthetic(z) == Constant(0)
    z = x + NthPower(Plus(Constant(1), Constant(2)), n = 2)
    assert reduce_synthetic(z) == x + Constant(9)
    z = Reciprocal(NthPower(Reciprocal(x), n = 2))
    assert reduce_synthetic(z) == NthPower(x, n = 2)
    z = Multiply(NthPower(Reciprocal(x), n = 2), NthPower(Reciprocal(y), n = 2))
    assert reduce_synthetic(z) == Reciprocal(NthPower(Multiply(x, y), n = 2))
    z = Multiply(Constant(1) + x + Constant(-1), Constant(2))
    assert reduce_synthetic(z) == Multiply(Constant(2), x)


def test_reduce_expressions_that_lack_variables():
    z = Minus(NthPower(Plus(Constant(2), Constant(1)), n = 2), Constant(1))
    assert _reduce_expressions_that_lack_variables(z) == Constant(8)
    z = Logarithm(Constant(-1))
    assert _reduce_expressions_that_lack_variables(z) == None


def test_reduce_negation_of_negation_of_u():
    u = Variable("u")
    z = Negation(Negation(u))
    assert _reduce_negation_of_negation_of_u(z) == u


def test_reduce_reciprocal_of_reciprocal_of_u():
    u = Variable("u")
    z = Reciprocal(Reciprocal(u))
    assert _reduce_reciprocal_of_reciprocal_of_u(z) == u


def test_reduce_reciprocal_of_negation_of_u():
    u = Variable("u")
    z = Reciprocal(Negation(u))
    assert _reduce_reciprocal_of_negation_of_u(z) == Negation(Reciprocal(u))


def test_reduce_nth_power_where_n_is_one():
    u = Variable("u")
    z = NthPower(u, n = 1)
    assert _reduce_nth_power_where_n_is_one(z) == u


def test_reduce_nth_power_of_mth_power_of_u():
    u = Variable("u")
    z = NthPower(NthPower(u, n = 3), n = 2)
    assert _reduce_nth_power_of_mth_power_of_u(z) == NthPower(u, n = 6)


def test_reduce_nth_power_of_negation_of_u():
    u = Variable("u")
    z = NthPower(Negation(u), n = 2)
    assert _reduce_nth_power_of_negation_of_u(z) == NthPower(u, n = 2)
    z = NthPower(Negation(u), n = 3)
    assert _reduce_nth_power_of_negation_of_u(z) == Negation(NthPower(u, n = 3))


def test_reduce_nth_power_of_reciprocal_of_u():
    u = Variable("u")
    z = NthPower(Reciprocal(u), n = 2)
    assert _reduce_nth_power_of_reciprocal_of_u(z) == Reciprocal(NthPower(u, n = 2))


def test_reduce_nth_root_where_n_is_one():
    u = Variable("u")
    z = NthRoot(u, n = 1)
    assert _reduce_nth_root_where_n_is_one(z) == u


def test_reduce_nth_root_of_mth_root_of_u():
    u = Variable("u")
    z = NthRoot(NthRoot(u, n = 3), n = 2)
    assert _reduce_nth_root_of_mth_root_of_u(z) == NthRoot(u, n = 6)


def test_reduce_odd_nth_root_of_negation_of_u():
    u = Variable("u")
    z = NthRoot(Negation(u), n = 3)
    assert _reduce_odd_nth_root_of_negation_of_u(z) == Negation(NthRoot(u, n = 3))


def test_reduce_nth_root_of_reciprocal_of_u():
    u = Variable("u")
    z = NthRoot(Reciprocal(u), n = 2)
    assert _reduce_nth_root_of_reciprocal_of_u(z) == Reciprocal(NthRoot(u, n = 2))


def test_reduce_nth_root_of_mth_power_of_u():
    u = Variable("u")
    z = NthRoot(NthPower(u, n = 2), n = 3)
    assert _reduce_nth_root_of_mth_power_of_u(z) == NthPower(NthRoot(u, n = 3), n = 2)


def test_reduce_nth_power_of_mth_root_of_u():
    u = Variable("u")
    z = NthPower(NthRoot(u, n = 2), n = 2)
    assert _reduce_nth_power_of_mth_root_of_u(z) == u
    z = NthPower(NthRoot(u, n = 6), n = 2)
    assert _reduce_nth_power_of_mth_root_of_u(z) == NthRoot(u, n = 3)
    z = NthPower(NthRoot(u, n = 2), n = 6)
    assert _reduce_nth_power_of_mth_root_of_u(z) == NthPower(u, n = 3)
    z = NthPower(NthRoot(u, n = 6), n = 4)
    assert _reduce_nth_power_of_mth_root_of_u(z) == NthPower(NthRoot(u, n = 3), n = 2)
    z = NthPower(NthRoot(u, n = 4), n = 6)
    assert _reduce_nth_power_of_mth_root_of_u(z) == NthPower(NthRoot(u, n = 2), n = 3)


def test_reduce_exponential_of_negation_of_u():
    u = Variable("u")
    z = Exponential(Negation(u))
    assert _reduce_exponential_of_negation_of_u(z) == Reciprocal(Exponential(u))
    z = Exponential(Negation(u), base = 2)
    assert _reduce_exponential_of_negation_of_u(z) == Reciprocal(Exponential(u, base = 2))


def test_reduce_logarithm_of_reciprocal_of_u():
    u = Variable("u")
    z = Logarithm(Reciprocal(u))
    assert _reduce_logarithm_of_reciprocal_of_u(z) == Negation(Logarithm(u))
    z = Logarithm(Reciprocal(u), base = 2)
    assert _reduce_logarithm_of_reciprocal_of_u(z) == Negation(Logarithm(u, base = 2))


def test_reduce_logarithm_of_exponential_of_u():
    u = Variable("u")
    z = Logarithm(Exponential(u))
    assert _reduce_logarithm_of_exponential_of_u(z) == u
    z = Logarithm(Exponential(u, base = 2), base = 2)
    assert _reduce_logarithm_of_exponential_of_u(z) == u


def test_reduce_exponential_of_logarithm_of_u():
    u = Variable("u")
    z = Exponential(Logarithm(u))
    assert _reduce_exponential_of_logarithm_of_u(z) == u
    z = Exponential(Logarithm(u, base = 2), base = 2)
    assert _reduce_exponential_of_logarithm_of_u(z) == u


def test_reduce_cosine_of_negation_of_u():
    u = Variable("u")
    z = Cosine(Negation(u))
    assert _reduce_cosine_of_negation_of_u(z) == Cosine(u)


def test_reduce_sine_of_negation_of_u():
    u = Variable("u")
    z = Sine(Negation(u))
    assert _reduce_sine_of_negation_of_u(z) == Negation(Sine(u))


def test_reduce_by_associating_plus_right():
    u = Variable("u")
    v = Variable("v")
    w = Variable("w")
    z = Plus(Plus(u, v), w)
    assert _reduce_by_associating_plus_right(z) == Plus(u, Plus(v, w))


def test_reduce_by_commuting_constants_right_for_plus():
    u = Variable("u")
    z = Plus(Constant(7), u)
    assert _reduce_by_commuting_constants_right_for_plus(z) == Plus(u, Constant(7))


def test_reduce_u_plus_zero():
    u = Variable("u")
    z = Plus(u, Constant(0))
    assert _reduce_u_plus_zero(z) == u


def test_reduce_u_minus_zero():
    u = Variable("u")
    z = Minus(u, Constant(0))
    assert _reduce_u_minus_zero(z) == u


def test_reduce_zero_minus_u():
    u = Variable("u")
    z = Minus(Constant(0), u)
    assert _reduce_zero_minus_u(z) == Negation(u)


def test_reduce_negation_of_u_minus_v():
    u = Variable("u")
    v = Variable("v")
    z = Negation(Minus(u, v))
    assert _reduce_negation_of_u_minus_v(z) == Minus(v, u)


def test_reduce_by_associating_multiply_left():
    u = Variable("u")
    v = Variable("v")
    w = Variable("w")
    z = Multiply(u, Multiply(v, w))
    assert _reduce_by_associating_multiply_left(z) == Multiply(Multiply(u, v), w)


def test_reduce_by_commuting_constants_left_for_multiply():
    u = Variable("u")
    z = Multiply(u, Constant(12))
    assert _reduce_by_commuting_constants_left_for_multiply(z) == Multiply(Constant(12), u)


def test_reduce_one_times_u():
    u = Variable("u")
    z = Multiply(Constant(1), u)
    assert _reduce_one_times_u(z) == u


def test_reduce_zero_times_u():
    u = Variable("u")
    z = Multiply(Constant(0), u)
    assert _reduce_zero_times_u(z) == Constant(0)


def test_reduce_negative_one_times_u():
    u = Variable("u")
    z = Multiply(Constant(-1), u)
    assert _reduce_negative_one_times_u(z) == Negation(u)


def test_reduce_product_of_reciprocals():
    u = Variable("u")
    v = Variable("v")
    z = Multiply(Reciprocal(u), Reciprocal(v))
    assert _reduce_product_of_reciprocals(z) == Reciprocal(Multiply(u, v))


def test_reduce_product_of_nth_powers():
    u = Variable("u")
    v = Variable("v")
    z = Multiply(NthPower(u, n = 2), NthPower(v, n = 2))
    assert _reduce_product_of_nth_powers(z) == NthPower(Multiply(u, v), n = 2)


def test_reduce_product_of_nth_roots():
    u = Variable("u")
    v = Variable("v")
    z = Multiply(NthRoot(u, n = 2), NthRoot(v, n = 2))
    assert _reduce_product_of_nth_roots(z) == NthRoot(Multiply(u, v), n = 2)


def test_reduce_product_of_exponentials():
    u = Variable("u")
    v = Variable("v")
    z = Multiply(Exponential(u), Exponential(v))
    assert _reduce_product_of_exponentials(z) == Exponential(Plus(u, v))
    z = Multiply(Exponential(u, base = 2), Exponential(v, base = 2))
    assert _reduce_product_of_exponentials(z) == Exponential(Plus(u, v), base = 2)


def test_reduce_sum_of_logarithms():
    u = Variable("u")
    v = Variable("v")
    z = Plus(Logarithm(u), Logarithm(v))
    assert _reduce_sum_of_logarithms(z) == Logarithm(Multiply(u, v))
    z = Plus(Logarithm(u, base = 2), Logarithm(v, base = 2))
    assert _reduce_sum_of_logarithms(z) == Logarithm(Multiply(u, v), base = 2)


def test_reduce_u_over_one():
    u = Variable("u")
    z = Divide(u, Constant(1))
    assert _reduce_u_over_one(z) == u


def test_reduce_one_over_u():
    u = Variable("u")
    z = Divide(Constant(1), u)
    assert _reduce_one_over_u(z) == Reciprocal(u)


def test_reduce_negated_numerator():
    u = Variable("u")
    v = Variable("v")
    z = Divide(Negation(u), v)
    assert _reduce_negated_numerator(z) == Negation(Divide(u, v))


def test_reduce_negated_denominator():
    u = Variable("u")
    v = Variable("v")
    z = Divide(u, Negation(v))
    assert _reduce_negated_denominator(z) == Negation(Divide(u, v))


def test_reduce_reciprocal_of_u_over_v():
    u = Variable("u")
    v = Variable("v")
    z = Reciprocal(Divide(u, v))
    assert _reduce_reciprocal_of_u_over_v(z) == Divide(v, u)


def test_reduce_one_to_the_u():
    u = Variable("u")
    z = Power(Constant(1), u)
    assert _reduce_one_to_the_u(z) == Constant(1)


def test_reduce_u_to_the_n_at_least_two():
    u = Variable("u")
    z = Power(u, Constant(2))
    assert _reduce_u_to_the_n_at_least_two(z) == NthPower(u, n = 2)
    z = Power(u, Constant(3))
    assert _reduce_u_to_the_n_at_least_two(z) == NthPower(u, n = 3)


def test_reduce_u_to_the_one():
    u = Variable("u")
    z = Power(u, Constant(1))
    assert _reduce_u_to_the_one(z) == u


def test_reduce_u_to_the_zero():
    u = Variable("u")
    z = Power(u, Constant(0))
    assert _reduce_u_to_the_zero(z) == Constant(1)


def test_reduce_u_to_the_negative_one():
    u = Variable("u")
    z = Power(u, Constant(-1))
    assert _reduce_u_to_the_negative_one(z) == Reciprocal(u)


def test_reduce_u_to_the_one_half():
    u = Variable("u")
    z = Power(u, Constant(0.5))
    assert _reduce_u_to_the_one_half(z) == NthRoot(u, n = 2)


def test_reduce_power_with_constant_base():
    u = Variable("u")
    z = Power(Constant(2), u)
    assert _reduce_power_with_constant_base(z) == Exponential(u, base = 2)


def test_reduce_power_of_power():
    u = Variable("u")
    v = Variable("v")
    w = Variable("w")
    z = Power(Power(u, v), w)
    assert _reduce_power_of_power(z) == Power(u, Multiply(v, w))
