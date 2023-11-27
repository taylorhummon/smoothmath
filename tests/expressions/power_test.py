from pytest import approx, raises
from smoothmath.errors import DomainError
from smoothmath.point import Point
from smoothmath.expressions import Constant, Variable, SquareRoot, Power


def test_Power():
    x = Variable("x")
    y = Variable("y")
    z = Power(x, y)
    computed_global_partials = z.compute_global_partials()
    # at (x, y) = (3, 2.5)
    point = Point({x: 3, y: 2.5})
    assert z.evaluate(point) == approx(15.588457268)
    assert z.partial_at(point, x) == approx(12.990381056)
    assert z.partial_at(point, y) == approx(17.125670716)
    computed_local_partials = z.compute_local_partials(point)
    assert computed_local_partials.partial_with_respect_to(x) == approx(12.990381056)
    assert computed_local_partials.partial_with_respect_to(y) == approx(17.125670716)
    assert computed_global_partials.partial_at(point, x) == approx(12.990381056)
    assert computed_global_partials.partial_at(point, y) == approx(17.125670716)
    # at (x, y) = (3, 0)
    point = Point({x: 3, y: 0})
    assert z.evaluate(point) == approx(1)
    assert z.partial_at(point, x) == approx(0)
    assert z.partial_at(point, y) == approx(1.0986122886)
    computed_local_partials = z.compute_local_partials(point)
    assert computed_local_partials.partial_with_respect_to(x) == approx(0)
    assert computed_local_partials.partial_with_respect_to(y) == approx(1.0986122886)
    assert computed_global_partials.partial_at(point, x) == approx(0)
    assert computed_global_partials.partial_at(point, y) == approx(1.0986122886)
    # at (x, y) = (3, -2.5)
    point = Point({x: 3, y: -2.5})
    assert z.evaluate(point) == approx(0.0641500299)
    assert z.partial_at(point, x) == approx(-0.0534583582)
    assert z.partial_at(point, y) == approx(0.0704760111)
    computed_local_partials = z.compute_local_partials(point)
    assert computed_local_partials.partial_with_respect_to(x) == approx(-0.0534583582)
    assert computed_local_partials.partial_with_respect_to(y) == approx(0.0704760111)
    assert computed_global_partials.partial_at(point, x) == approx(-0.0534583582)
    assert computed_global_partials.partial_at(point, y) == approx(0.0704760111)
    # at (x, y) = (0, 2.5)
    point = Point({x: 0, y: 2.5})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.partial_at(point, y)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        computed_global_partials.partial_at(point, x)
    with raises(DomainError):
        computed_global_partials.partial_at(point, y)
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
        computed_global_partials.partial_at(point, x)
    with raises(DomainError):
        computed_global_partials.partial_at(point, y)
    # at (x, y) = (0, -2.5)
    point = Point({x: 0, y: -2.5})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.partial_at(point, y)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        computed_global_partials.partial_at(point, x)
    with raises(DomainError):
        computed_global_partials.partial_at(point, y)
    # at (x, y) = (-3, 2.5)
    point = Point({x: -3, y: 2.5})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.partial_at(point, y)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        computed_global_partials.partial_at(point, x)
    with raises(DomainError):
        computed_global_partials.partial_at(point, y)
    # at (x, y) = (-3, 0)
    point = Point({x: -3, y: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.partial_at(point, y)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        computed_global_partials.partial_at(point, x)
    with raises(DomainError):
        computed_global_partials.partial_at(point, y)
    # at (x, y) = (-3, -2.5)
    point = Point({x: -3, y: -2.5})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.partial_at(point, y)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        computed_global_partials.partial_at(point, x)
    with raises(DomainError):
        computed_global_partials.partial_at(point, y)


def test_Power_composition():
    x = Variable("x")
    y = Variable("y")
    z = Power(Constant(2) * x, Constant(3) * y)
    point = Point({x: 1, y: 1})
    assert z.evaluate(point) == approx(8)
    assert z.partial_at(point, x) == approx(24)
    assert z.partial_at(point, y) == approx(16.63553233343)
    computed_local_partials = z.compute_local_partials(point)
    assert computed_local_partials.partial_with_respect_to(x) == approx(24)
    assert computed_local_partials.partial_with_respect_to(y) == approx(16.63553233343)
    computed_global_partials = z.compute_global_partials()
    assert computed_global_partials.partial_at(point, x) == approx(24)
    assert computed_global_partials.partial_at(point, y) == approx(16.63553233343)


def test_Power_with_constant_base_one():
    y = Variable("y")
    z = Power(Constant(1), y)
    computed_global_partials = z.compute_global_partials()
    # at y = 3
    point = Point({y: 3})
    assert z.evaluate(point) == approx(1)
    assert z.partial_at(point, y) == approx(0)
    assert z.compute_local_partials(point).partial_with_respect_to(y) == approx(0)
    assert computed_global_partials.partial_at(point, y) == approx(0)
    # at y = 0
    point = Point({y: 0})
    assert z.evaluate(point) == approx(1)
    assert z.partial_at(point, y) == approx(0)
    assert z.compute_local_partials(point).partial_with_respect_to(y) == approx(0)
    assert computed_global_partials.partial_at(point, y) == approx(0)
    # at y = -5
    point = Point({y: -5})
    assert z.evaluate(point) == approx(1)
    assert z.partial_at(point, y) == approx(0)
    assert z.compute_local_partials(point).partial_with_respect_to(y) == approx(0)
    assert computed_global_partials.partial_at(point, y) == approx(0)


def test_Power_with_constant_base_zero():
    y = Variable("y")
    z = Power(Constant(0), y)
    computed_global_partials = z.compute_global_partials()
    # at y = 3
    point = Point({y: 3})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, y)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        computed_global_partials.partial_at(point, y)
    # at y = 0
    point = Point({y: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, y)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        computed_global_partials.partial_at(point, y)
    # at y = -5
    point = Point({y: -5})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, y)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        computed_global_partials.partial_at(point, y)


def test_Power_with_constant_base_negative_one():
    y = Variable("y")
    z = Power(Constant(-1), y)
    computed_global_partials = z.compute_global_partials()
    # at y = 3
    point = Point({y: 3})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, y)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        computed_global_partials.partial_at(point, y)
    # at y = 0
    point = Point({y: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, y)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        computed_global_partials.partial_at(point, y)
    # at y = -5
    point = Point({y: -5})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, y)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        computed_global_partials.partial_at(point, y)


def test_Power_with_constant_exponent_two():
    x = Variable("x")
    z = Power(x, Constant(2))
    computed_global_partials = z.compute_global_partials()
    # at y = 3
    point = Point({x: 3})
    assert z.evaluate(point) == approx(9)
    assert z.partial_at(point, x) == approx(6)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(6)
    assert computed_global_partials.partial_at(point, x) == approx(6)
    # at y = 0
    point = Point({x: 0})
    assert z.evaluate(point) == approx(0)
    assert z.partial_at(point, x) == approx(0)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(0)
    assert computed_global_partials.partial_at(point, x) == approx(0)
    # at y = -5
    point = Point({x: -5})
    assert z.evaluate(point) == approx(25)
    assert z.partial_at(point, x) == approx(-10)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(-10)
    assert computed_global_partials.partial_at(point, x) == approx(-10)


def test_Power_with_constant_exponent_two_composition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(2))
    point = Point({x: 1})
    assert z.evaluate(point) == approx(4)
    assert z.partial_at(point, x) == approx(12)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(12)
    assert z.compute_global_partials().partial_at(point, x) == approx(12)


def test_Power_with_constant_exponent_one():
    x = Variable("x")
    z = Power(x, Constant(1))
    computed_global_partials = z.compute_global_partials()
    # at y = 3
    point = Point({x: 3})
    assert z.evaluate(point) == approx(3)
    assert z.partial_at(point, x) == approx(1)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(1)
    assert computed_global_partials.partial_at(point, x) == approx(1)
    # at y = 0
    point = Point({x: 0})
    assert z.evaluate(point) == approx(0)
    assert z.partial_at(point, x) == approx(1)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(1)
    assert computed_global_partials.partial_at(point, x) == approx(1)
    # at y = -5
    point = Point({x: -5})
    assert z.evaluate(point) == approx(-5)
    assert z.partial_at(point, x) == approx(1)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(1)
    assert computed_global_partials.partial_at(point, x) == approx(1)


def test_Power_with_constant_exponent_one_composition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(1))
    point = Point({x: 1})
    assert z.evaluate(point) == approx(2)
    assert z.partial_at(point, x) == approx(3)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(3)
    assert z.compute_global_partials().partial_at(point, x) == approx(3)


def test_Power_with_constant_exponent_zero():
    x = Variable("x")
    z = Power(x, Constant(0))
    computed_global_partials = z.compute_global_partials()
    # at x = 3
    point = Point({x: 3})
    assert z.evaluate(point) == approx(1)
    assert z.partial_at(point, x) == approx(0)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(0)
    assert computed_global_partials.partial_at(point, x) == approx(0)
    # at x = 0
    point = Point({x: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        computed_global_partials.partial_at(point, x)
    # at x = -5
    point = Point({x: -5})
    assert z.evaluate(point) == approx(1)
    assert z.partial_at(point, x) == approx(0)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(0)
    assert computed_global_partials.partial_at(point, x) == approx(0)


def test_Power_with_constant_exponent_zero_composition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(0))
    point = Point({x: 1})
    assert z.evaluate(point) == approx(1)
    assert z.partial_at(point, x) == approx(0)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(0)
    assert z.compute_global_partials().partial_at(point, x) == approx(0)


def test_Power_with_constant_exponent_zero_doesnt_short_circuit():
    x = Variable("x")
    z = Power(SquareRoot(x), Constant(0))
    point = Point({x: -1})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.compute_local_partials(point)
    computed_global_partials = z.compute_global_partials()
    with raises(DomainError):
        computed_global_partials.partial_at(point, x)


def test_Power_with_constant_exponent_negative_one():
    x = Variable("x")
    z = Power(x, Constant(-1))
    computed_global_partials = z.compute_global_partials()
    # at x = 2
    point = Point({x: 2})
    assert z.evaluate(point) == approx(0.5)
    assert z.partial_at(point, x) == approx(-0.25)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(-0.25)
    assert computed_global_partials.partial_at(point, x) == approx(-0.25)
    # at x = 0
    point = Point({x: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        computed_global_partials.partial_at(point, x)
    # at x = -5
    point = Point({x: -5})
    assert z.evaluate(point) == approx(-0.2)
    assert z.partial_at(point, x) == approx(-0.04)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(-0.04)
    assert computed_global_partials.partial_at(point, x) == approx(-0.04)


def test_Power_with_constant_exponent_negative_one_composition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(-1))
    point = Point({x: 1})
    assert z.evaluate(point) == approx(0.5)
    assert z.partial_at(point, x) == approx(-0.75)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(-0.75)
    assert z.compute_global_partials().partial_at(point, x) == approx(-0.75)


def test_Power_with_constant_exponent_negative_two():
    x = Variable("x")
    z = Power(x, Constant(-2))
    computed_global_partials = z.compute_global_partials()
    # at x = 2
    point = Point({x: 2})
    assert z.evaluate(point) == approx(0.25)
    assert z.partial_at(point, x) == approx(-0.25)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(-0.25)
    assert computed_global_partials.partial_at(point, x) == approx(-0.25)
    # at x = 0
    point = Point({x: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.compute_local_partials(point)
    with raises(DomainError):
        computed_global_partials.partial_at(point, x)
    # at x = -5
    point = Point({x: -5})
    assert z.evaluate(point) == approx(0.04)
    assert z.partial_at(point, x) == approx(0.016)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(0.016)
    assert computed_global_partials.partial_at(point, x) == approx(0.016)


def test_Power_with_constant_exponent_negative_two_composition():
    x = Variable("x")
    z = Power(Constant(3) * x - Constant(1), Constant(-2))
    point = Point({x: 1})
    assert z.evaluate(point) == approx(0.25)
    assert z.partial_at(point, x) == approx(-0.75)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(-0.75)
    assert z.compute_global_partials().partial_at(point, x) == approx(-0.75)


def test_Power_one_to_the_zero():
    z = Power(Constant(1), Constant(0))
    assert z.evaluate(Point({})) == approx(1)


def test_Power_with_exponent_made_from_adding_constants():
    x = Variable("x")
    z = Power(x, Constant(1) + Constant(1))
    computed_global_partials = z.compute_global_partials()
    # at x = 3
    point = Point({x: 3})
    assert z.evaluate(point) == approx(9)
    assert z.partial_at(point, x) == approx(6)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(6)
    assert computed_global_partials.partial_at(point, x) == approx(6)
    # at x = 0
    point = Point({x: 0})
    assert z.evaluate(point) == approx(0)
    assert z.partial_at(point, x) == approx(0)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(0)
    assert computed_global_partials.partial_at(point, x) == approx(0)
    # at x = -5
    point = Point({x: -5})
    assert z.evaluate(point) == approx(25)
    assert z.partial_at(point, x) == approx(-10)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(-10)
    assert computed_global_partials.partial_at(point, x) == approx(-10)


def test_Power_where_exponent_is_an_integer_represented_as_a_float():
    x = Variable("x")
    z = Power(x, Constant(2.0))
    point = Point({x: -5})
    assert z.evaluate(point) == approx(25)
    assert z.partial_at(point, x) == approx(-10)
    assert z.compute_local_partials(point).partial_with_respect_to(x) == approx(-10)
    assert z.compute_global_partials().partial_at(point, x) == approx(-10)
