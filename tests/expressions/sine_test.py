from pytest import approx
import math
from smoothmath.point import Point
from smoothmath.expressions import Constant, Variable, Sine


def test_Sine():
    theta = Variable("theta")
    z = Sine(theta)
    synthetic = z.synthetic()
    # at theta = 0
    point = Point({theta: 0})
    assert z.evaluate(point) == approx(0)
    assert z.partial_at(point, theta) == approx(1)
    assert z.compute_local_partials(point).partial_with_respect_to(theta) == approx(1)
    assert synthetic.partial_at(point, theta) == approx(1)
    # at theta = pi / 2
    point = Point({theta: math.pi / 2})
    assert z.evaluate(point) == approx(1)
    assert z.partial_at(point, theta) == approx(0)
    assert z.compute_local_partials(point).partial_with_respect_to(theta) == approx(0)
    assert synthetic.partial_at(point, theta) == approx(0)


def test_Sine_composition():
    theta = Variable("theta")
    z = Sine(Constant(2) * theta)
    point = Point({theta: 0})
    assert z.evaluate(point) == approx(0)
    assert z.partial_at(point, theta) == approx(2)
    assert z.compute_local_partials(point).partial_with_respect_to(theta) == approx(2)
    assert z.synthetic().partial_at(point, theta) == approx(2)
