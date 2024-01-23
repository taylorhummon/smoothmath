from smoothmath.expression import (
    Constant, Variable,
    Negation, Reciprocal, Cosine, Sine,
    NthPower, NthRoot, Exponential, Logarithm,
    Plus, Multiply, Power
)
import smoothmath._private.reducers as r


# Constant and Variable


def test_reduce_expressions_that_lack_variables():
    z = Multiply(NthPower(Plus(Constant(2), Constant(1)), n = 2), Constant(2))
    assert r._reduce_expressions_that_lack_variables(z) == Constant(18)
    z = Logarithm(Constant(-1))
    assert r._reduce_expressions_that_lack_variables(z) == None


# Negation and Reciprocal


def test_reduce_negation_of_negation_of_u():
    u = Variable("u")
    z = Negation(Negation(u))
    assert r._reduce_negation_of_negation_of_u(z) == u


def test_reduce_reciprocal_of_reciprocal_of_u():
    u = Variable("u")
    z = Reciprocal(Reciprocal(u))
    assert r._reduce_reciprocal_of_reciprocal_of_u(z) == u


def test_reduce_reciprocal_of_negation_of_u():
    u = Variable("u")
    z = Reciprocal(Negation(u))
    assert r._reduce_reciprocal_of_negation_of_u(z) == Negation(Reciprocal(u))


# Plus


def test_reduce_by_associating_plus_right():
    u = Variable("u")
    v = Variable("v")
    w = Variable("w")
    z = Plus(Plus(u, v), w)
    assert r._reduce_by_associating_plus_right(z) == Plus(u, Plus(v, w))


def test_reduce_u_plus_zero():
    u = Variable("u")
    z = Plus(u, Constant(0))
    assert r._reduce_u_plus_zero(z) == u


def test_reduce_by_commuting_constant_right_across_plus():
    u = Variable("u")
    z = Plus(Constant(7), u)
    assert r._reduce_by_commuting_constant_right_across_plus(z) == Plus(u, Constant(7))


def test_reduce_by_commuting_negation_right_across_plus():
    u = Variable("u")
    v = Variable("v")
    z = Plus(Negation(u), v)
    assert r._reduce_by_commuting_negation_right_across_plus(z) == Plus(v, Negation(u))


def test_reduce_sum_of_negations():
    u = Variable("u")
    v = Variable("v")
    z = Plus(Negation(u), Negation(v))
    assert r._reduce_sum_of_negations(z) == Negation(Plus(u, v))


# Multiply


def test_reduce_by_associating_multiply_left():
    u = Variable("u")
    v = Variable("v")
    w = Variable("w")
    z = Multiply(u, Multiply(v, w))
    assert r._reduce_by_associating_multiply_left(z) == Multiply(Multiply(u, v), w)


def test_reduce_one_times_u():
    u = Variable("u")
    z = Multiply(Constant(1), u)
    assert r._reduce_one_times_u(z) == u


def test_reduce_zero_times_u():
    u = Variable("u")
    z = Multiply(Constant(0), u)
    assert r._reduce_zero_times_u(z) == Constant(0)


def test_reduce_negative_one_times_u():
    u = Variable("u")
    z = Multiply(Constant(-1), u)
    assert r._reduce_negative_one_times_u(z) == Negation(u)


def test_reduce_by_commuting_constant_left_across_multiply():
    u = Variable("u")
    z = Multiply(u, Constant(12))
    assert r._reduce_by_commuting_constant_left_across_multiply(z) == Multiply(Constant(12), u)


def test_reduce_negation_of_u__times_v():
    u = Variable("u")
    v = Variable("v")
    z = Multiply(Negation(u), v)
    assert r._reduce_negation_of_u__times_v(z) == Negation(Multiply(u, v))


def test_reduce_u_times_negation_of_v():
    u = Variable("u")
    v = Variable("v")
    z = Multiply(u, Negation(v))
    assert r._reduce_u_times_negation_of_v(z) == Negation(Multiply(u, v))


def test_reduce_by_commuting_reciprocal_left_across_multiply():
    u = Variable("u")
    v = Variable("v")
    z = Multiply(u, Reciprocal(v))
    assert r._reduce_by_commuting_reciprocal_left_across_multiply(z) == Multiply(Reciprocal(v), u)


def test_reduce_product_of_reciprocals():
    u = Variable("u")
    v = Variable("v")
    z = Multiply(Reciprocal(u), Reciprocal(v))
    assert r._reduce_product_of_reciprocals(z) == Reciprocal(Multiply(u, v))


# Cosine and Sine


def test_reduce_cosine_of_negation_of_u():
    u = Variable("u")
    z = Cosine(Negation(u))
    assert r._reduce_cosine_of_negation_of_u(z) == Cosine(u)


def test_reduce_sine_of_negation_of_u():
    u = Variable("u")
    z = Sine(Negation(u))
    assert r._reduce_sine_of_negation_of_u(z) == Negation(Sine(u))


# NthPower and NthRoot


def test_reduce_nth_power_where_n_is_one():
    u = Variable("u")
    z = NthPower(u, n = 1)
    assert r._reduce_nth_power_where_n_is_one(z) == u


def test_reduce_nth_root_where_n_is_one():
    u = Variable("u")
    z = NthRoot(u, n = 1)
    assert r._reduce_nth_root_where_n_is_one(z) == u


def test_reduce_nth_power_of_mth_root_of_u():
    u = Variable("u")
    z = NthPower(NthRoot(u, n = 2), n = 2)
    assert r._reduce_nth_power_of_mth_root_of_u(z) == u
    z = NthPower(NthRoot(u, n = 6), n = 2)
    assert r._reduce_nth_power_of_mth_root_of_u(z) == NthRoot(u, n = 3)
    z = NthPower(NthRoot(u, n = 2), n = 6)
    assert r._reduce_nth_power_of_mth_root_of_u(z) == NthPower(u, n = 3)
    z = NthPower(NthRoot(u, n = 6), n = 4)
    assert r._reduce_nth_power_of_mth_root_of_u(z) == NthPower(NthRoot(u, n = 3), n = 2)
    z = NthPower(NthRoot(u, n = 4), n = 6)
    assert r._reduce_nth_power_of_mth_root_of_u(z) == NthPower(NthRoot(u, n = 2), n = 3)


def test_reduce_nth_root_of_mth_power_of_u():
    u = Variable("u")
    z = NthRoot(NthPower(u, n = 2), n = 3)
    assert r._reduce_nth_root_of_mth_power_of_u(z) == NthPower(NthRoot(u, n = 3), n = 2)


def test_reduce_product_of_nth_powers():
    u = Variable("u")
    v = Variable("v")
    z = Multiply(NthPower(u, n = 2), NthPower(v, n = 2))
    assert r._reduce_product_of_nth_powers(z) == NthPower(Multiply(u, v), n = 2)


def test_reduce_product_of_nth_roots():
    u = Variable("u")
    v = Variable("v")
    z = Multiply(NthRoot(u, n = 2), NthRoot(v, n = 2))
    assert r._reduce_product_of_nth_roots(z) == NthRoot(Multiply(u, v), n = 2)


def test_reduce_nth_power_of_mth_power_of_u():
    u = Variable("u")
    z = NthPower(NthPower(u, n = 3), n = 2)
    assert r._reduce_nth_power_of_mth_power_of_u(z) == NthPower(u, n = 6)


def test_reduce_nth_root_of_mth_root_of_u():
    u = Variable("u")
    z = NthRoot(NthRoot(u, n = 3), n = 2)
    assert r._reduce_nth_root_of_mth_root_of_u(z) == NthRoot(u, n = 6)


def test_reduce_nth_power_of_negation_of_u():
    u = Variable("u")
    z = NthPower(Negation(u), n = 2)
    assert r._reduce_nth_power_of_negation_of_u(z) == NthPower(u, n = 2)
    z = NthPower(Negation(u), n = 3)
    assert r._reduce_nth_power_of_negation_of_u(z) == Negation(NthPower(u, n = 3))


def test_reduce_odd_nth_root_of_negation_of_u():
    u = Variable("u")
    z = NthRoot(Negation(u), n = 3)
    assert r._reduce_odd_nth_root_of_negation_of_u(z) == Negation(NthRoot(u, n = 3))


def test_reduce_nth_power_of_reciprocal_of_u():
    u = Variable("u")
    z = NthPower(Reciprocal(u), n = 2)
    assert r._reduce_nth_power_of_reciprocal_of_u(z) == Reciprocal(NthPower(u, n = 2))


def test_reduce_nth_root_of_reciprocal_of_u():
    u = Variable("u")
    z = NthRoot(Reciprocal(u), n = 2)
    assert r._reduce_nth_root_of_reciprocal_of_u(z) == Reciprocal(NthRoot(u, n = 2))


# Exponential And Logarithm


def test_reduce_logarithm_of_exponential_of_u():
    u = Variable("u")
    z = Logarithm(Exponential(u))
    assert r._reduce_logarithm_of_exponential_of_u(z) == u
    z = Logarithm(Exponential(u, base = 2), base = 2)
    assert r._reduce_logarithm_of_exponential_of_u(z) == u


def test_reduce_exponential_of_logarithm_of_u():
    u = Variable("u")
    z = Exponential(Logarithm(u))
    assert r._reduce_exponential_of_logarithm_of_u(z) == u
    z = Exponential(Logarithm(u, base = 2), base = 2)
    assert r._reduce_exponential_of_logarithm_of_u(z) == u


def test_reduce_product_of_exponentials():
    u = Variable("u")
    v = Variable("v")
    z = Multiply(Exponential(u), Exponential(v))
    assert r._reduce_product_of_exponentials(z) == Exponential(Plus(u, v))
    z = Multiply(Exponential(u, base = 2), Exponential(v, base = 2))
    assert r._reduce_product_of_exponentials(z) == Exponential(Plus(u, v), base = 2)


def test_reduce_sum_of_logarithms():
    u = Variable("u")
    v = Variable("v")
    z = Plus(Logarithm(u), Logarithm(v))
    assert r._reduce_sum_of_logarithms(z) == Logarithm(Multiply(u, v))
    z = Plus(Logarithm(u, base = 2), Logarithm(v, base = 2))
    assert r._reduce_sum_of_logarithms(z) == Logarithm(Multiply(u, v), base = 2)


def test_reduce_exponential_of_negation_of_u():
    u = Variable("u")
    z = Exponential(Negation(u))
    assert r._reduce_exponential_of_negation_of_u(z) == Reciprocal(Exponential(u))
    z = Exponential(Negation(u), base = 2)
    assert r._reduce_exponential_of_negation_of_u(z) == Reciprocal(Exponential(u, base = 2))


def test_reduce_logarithm_of_reciprocal_of_u():
    u = Variable("u")
    z = Logarithm(Reciprocal(u))
    assert r._reduce_logarithm_of_reciprocal_of_u(z) == Negation(Logarithm(u))
    z = Logarithm(Reciprocal(u), base = 2)
    assert r._reduce_logarithm_of_reciprocal_of_u(z) == Negation(Logarithm(u, base = 2))


def test_reduce_nth_power_of_exponential_of_u():
    u = Variable("u")
    z = NthPower(Exponential(u), n = 2)
    assert r._reduce_nth_power_of_exponential_of_u(z) == Exponential(Multiply(Constant(2), u))
    z = NthPower(Exponential(u, base = 2), n = 3)
    assert r._reduce_nth_power_of_exponential_of_u(z) == Exponential(Multiply(Constant(3), u), base = 2)


def test_reduce_logarithm_of_nth_power_of_u():
    u = Variable("u")
    z = Logarithm(NthPower(u, n = 3))
    assert r._reduce_logarithm_of_nth_power_of_u(z) == Multiply(Constant(3), Logarithm(u))
    z = Logarithm(NthPower(u, n = 3), base = 2)
    assert r._reduce_logarithm_of_nth_power_of_u(z) == Multiply(Constant(3), Logarithm(u, base = 2))
    z = Logarithm(NthPower(u, n = 4))
    # We don't want to reduce to Multiply(Constant(4), Logarithm(u)) because u might be negative
    assert r._reduce_logarithm_of_nth_power_of_u(z) == None


# Power


def test_reduce_u_to_the_one():
    u = Variable("u")
    z = Power(u, Constant(1))
    assert r._reduce_u_to_the_one(z) == u


def test_reduce_u_to_the_zero():
    u = Variable("u")
    z = Power(u, Constant(0))
    assert r._reduce_u_to_the_zero(z) == Constant(1)


def test_reduce_one_to_the_u():
    u = Variable("u")
    z = Power(Constant(1), u)
    assert r._reduce_one_to_the_u(z) == Constant(1)


def test_reduce_u_to_the_n_at_least_two():
    u = Variable("u")
    z = Power(u, Constant(2))
    assert r._reduce_u_to_the_n_at_least_two(z) == NthPower(u, n = 2)
    z = Power(u, Constant(3))
    assert r._reduce_u_to_the_n_at_least_two(z) == NthPower(u, n = 3)


def test_reduce_u_to_the_negative_one():
    u = Variable("u")
    z = Power(u, Constant(-1))
    assert r._reduce_u_to_the_negative_one(z) == Reciprocal(u)


def test_reduce_u_to_the_one_over_n():
    u = Variable("u")
    z = Power(u, Reciprocal(Constant(2)))
    assert r._reduce_u_to_the_one_over_n(z) == NthRoot(u, n = 2)
    z = Power(u, Reciprocal(Constant(3)))
    assert r._reduce_u_to_the_one_over_n(z) == NthRoot(u, n = 3)


def test_reduce_power_with_constant_base():
    u = Variable("u")
    z = Power(Constant(2), u)
    assert r._reduce_power_with_constant_base(z) == Exponential(u, base = 2)


def test_reduce_power_of_power():
    u = Variable("u")
    v = Variable("v")
    w = Variable("w")
    z = Power(Power(u, v), w)
    assert r._reduce_power_of_power(z) == Power(u, Multiply(v, w))


def test_reduce_u_to_the_negation_of_v():
    u = Variable("u")
    v = Variable("v")
    z = Power(u, Negation(v))
    assert r._reduce_u_to_the_negation_of_v(z) == Reciprocal(Power(u, v))


def test_reduce_one_over_u__to_the_v():
    u = Variable("u")
    v = Variable("v")
    z = Power(Reciprocal(u), v)
    assert r._reduce_one_over_u__to_the_v(z) == Reciprocal(Power(u, v))
