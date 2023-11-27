from pytest import approx, raises
from smoothmath.errors import DomainError
from smoothmath.point import Point
from smoothmath.expressions import Constant, Variable, Logarithm, Divide


def test_Divide():
    x = Variable("x")
    y = Variable("y")
    z = Divide(x, y)
    global_differential = z.compute_global_partials()
    # at (x, y) = (5, 2)
    point = Point({x: 5, y: 2})
    assert z.evaluate(point) == approx(2.5)
    assert z.partial_at(point, x) == approx(0.5)
    assert z.partial_at(point, y) == approx(-1.25)
    local_differential = z.compute_local_partials(point)
    assert local_differential.partial_with_respect_to(x) == approx(0.5)
    assert local_differential.partial_with_respect_to(y) == approx(-1.25)
    assert global_differential.partial_at(point, x) == approx(0.5)
    assert global_differential.partial_at(point, y) == approx(-1.25)
    # at (x, y) = (3, 0)
    point = Point({x: 3, y: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.partial_at(point, y)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        global_differential.partial_at(point, x)
    with raises(DomainError):
        global_differential.partial_at(point, y)
    # at (x, y) = (0, 0)
    point = Point({x: 0, y: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.partial_at(point, y)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        global_differential.partial_at(point, x)
    with raises(DomainError):
        global_differential.partial_at(point, y)


def test_Divide_composition():
    x = Variable("x")
    y = Variable("y")
    z = Divide(Constant(2) * x + Constant(4), Constant(5) * y)
    point = Point({x: 3, y: 1})
    assert z.evaluate(point) == approx(2)
    assert z.partial_at(point, x) == approx(0.4)
    assert z.partial_at(point, y) == approx(-2)
    local_differential = z.compute_local_partials(point)
    assert local_differential.partial_with_respect_to(x) == approx(0.4)
    assert local_differential.partial_with_respect_to(y) == approx(-2)
    global_differential = z.compute_global_partials()
    assert global_differential.partial_at(point, x) == approx(0.4)
    assert global_differential.partial_at(point, y) == approx(-2)


def test_Divide_with_constant_numerator_zero():
    y = Variable("y")
    z = Divide(Constant(0), y)
    global_differential = z.compute_global_partials()
    # at y = 3
    point = Point({y: 3})
    assert z.evaluate(point) == approx(0)
    assert z.partial_at(point, y) == approx(0)
    assert z.compute_local_partials(point).partial_with_respect_to(y) == approx(0)
    assert global_differential.partial_at(point, y) == approx(0)
    # at y = 0
    point = Point({y: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, y)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        global_differential.partial_at(point, y)


def test_Divide_with_constant_numerator_zero_composition():
    y = Variable("y")
    z = Divide(Constant(0), Constant(2) * y + Constant(4))
    point = Point({y: 3})
    assert z.evaluate(point) == approx(0)
    assert z.partial_at(point, y) == approx(0)
    assert z.compute_local_partials(point).partial_with_respect_to(y) == approx(0)
    assert z.compute_global_partials().partial_at(point, y) == approx(0)


def test_Divide_with_constant_numerator_zero_doesnt_short_circuit():
    y = Variable("y")
    z = Divide(Constant(0), Logarithm(y))
    point = Point({y: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, y)
    with raises(DomainError):
        z.compute_local_partials(point)
    global_differential = z.compute_global_partials()
    with raises(DomainError):
        global_differential.partial_at(point, y)


def test_Divide_with_constant_denominator_one():
    x = Variable("x")
    z = Divide(x, Constant(1))
    global_differential = z.compute_global_partials()
    # at x = 3
    point = Point({x: 3})
    assert z.evaluate(point) == approx(3)
    assert z.partial_at(point, x) == approx(1)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(1)
    assert global_differential.partial_at(point, x) == approx(1)
    # at x = 0
    point = Point({x: 0})
    assert z.evaluate(point) == approx(0)
    assert z.partial_at(point, x) == approx(1)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(1)
    assert global_differential.partial_at(point, x) == approx(1)


def test_divide_with_constant_denominator_zero():
    x = Variable("x")
    z = Divide(x, Constant(0))
    global_differential = z.compute_global_partials()
    # at x = 3
    point = Point({x: 3})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        global_differential.partial_at(point, x)
    # at x = 0
    point = Point({x: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        global_differential.partial_at(point, x)
