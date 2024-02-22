from pytest import approx, raises
from smoothmath import DomainError, Point, Partial, Differential, LocatedDifferential
from smoothmath.expression import Variable, Constant, Divide, Reciprocal, Logarithm
from assert_partials import ( # type: ignore
    assert_1_ary_partials,
    assert_1_ary_partials_raise,
    assert_2_ary_partials,
    assert_2_ary_partials_raise
)


def test_Divide():
    x = Variable("x")
    y = Variable("y")
    z = Divide(x, y)
    # at (x, y) = (5, 2)
    point = Point(x = 5, y = 2)
    assert z.at(point) == approx(2.5)
    assert_2_ary_partials(z, point, x, 0.5, y, -1.25)
    # at (x, y) = (3, 0)
    point = Point(x = 3, y = 0)
    with raises(DomainError):
        z.at(point)
    assert_2_ary_partials_raise(z, point, x, y)
    # at (x, y) = (0, 0)
    point = Point(x = 0, y = 0)
    with raises(DomainError):
        z.at(point)
    assert_2_ary_partials_raise(z, point, x, y)


def test_Divide_composition():
    x = Variable("x")
    y = Variable("y")
    z = Divide(Constant(2) * x + Constant(4), Constant(5) * y)
    point = Point(x = 3, y = 1)
    assert z.at(point) == approx(2)
    assert_2_ary_partials(z, point, x, 0.4, y, -2)


def test_Divide_with_constant_numerator_zero():
    y = Variable("y")
    z = Divide(Constant(0), y)
    # at y = 3
    point = Point(y = 3)
    assert z.at(point) == approx(0)
    assert_1_ary_partials(z, point, y, 0)
    # at y = 0
    point = Point(y = 0)
    with raises(DomainError):
        z.at(point)
    assert_1_ary_partials_raise(z, point, y)


def test_Divide_with_constant_numerator_zero_composition():
    y = Variable("y")
    z = Divide(Constant(0), Constant(2) * y + Constant(4))
    point = Point(y = 3)
    assert z.at(point) == approx(0)
    assert_1_ary_partials(z, point, y, 0)


def test_Divide_with_constant_numerator_zero_doesnt_short_circuit():
    y = Variable("y")
    z = Divide(Constant(0), Logarithm(y))
    point = Point(y = 0)
    with raises(DomainError):
        z.at(point)
    partial = Partial(z, y)
    with raises(DomainError):
        partial.at(point)
    partial = Partial(z, y, compute_eagerly = True)
    with raises(DomainError):
        partial.at(point)
    differential = Differential(z)
    with raises(DomainError):
        differential.part_at(y, point)
    with raises(DomainError):
        LocatedDifferential(z, point)


def test_Divide_with_constant_denominator_one():
    x = Variable("x")
    z = Divide(x, Constant(1))
    # at x = 3
    point = Point(x = 3)
    assert z.at(point) == approx(3)
    assert_1_ary_partials(z, point, x, 1)
    # at x = 0
    point = Point(x = 0)
    assert z.at(point) == approx(0)
    assert_1_ary_partials(z, point, x, 1)


def test_Divide_with_constant_denominator_zero():
    x = Variable("x")
    z = Divide(x, Constant(0))
    # at x = 3
    point = Point(x = 3)
    with raises(DomainError):
        z.at(point)
    assert_1_ary_partials_raise(z, point, x)
    # at x = 0
    point = Point(x = 0)
    with raises(DomainError):
        z.at(point)
    assert_1_ary_partials_raise(z, point, x)


def test_Divide_normalization():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    z = Divide(x, y)
    assert z._normalize() == Divide(x, y)
    z = Divide(x, Constant(1))
    assert z._normalize() == x
    z = Divide(Constant(1), x)
    assert z._normalize() == Reciprocal(x)
    z = Divide(w * x, y)
    assert z._normalize() == Divide(w * x, y)
    z = Divide(w, x * y)
    assert z._normalize() == Divide(w, x * y)
    z = Divide(Divide(w, x), y)
    assert z._normalize() == Divide(w, x * y)
    z = Divide(w, Divide(x, y))
    assert z._normalize() == Divide(w * y, x)
