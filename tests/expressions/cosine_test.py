from pytest import approx
import math
from smoothmath.point import Point
from smoothmath.expressions import Constant, Variable, Cosine


def test_Cosine():
    theta = Variable("theta")
    z = Cosine(theta)
    global_theta_partial = z.global_partial(theta)
    global_differential = z.global_differential()
    # at theta = 0
    point = Point({theta: 0})
    assert z.evaluate(point) == approx(1)
    assert z.local_partial(point, theta) == approx(0)
    assert global_theta_partial.at(point) == approx(0)
    assert z.local_differential(point).component(theta) == approx(0)
    assert global_differential.component_at(point, theta) == approx(0)
    # theta = pi / 2
    point = Point({theta: math.pi / 2})
    assert z.evaluate(point) == approx(0)
    assert z.local_partial(point, theta) == approx(-1)
    assert global_theta_partial.at(point) == approx(-1)
    assert z.local_differential(point).component(theta) == approx(-1)
    assert global_differential.component_at(point, theta) == approx(-1)


def test_Cosine_composition():
    theta = Variable("theta")
    z = Cosine(Constant(2) * theta)
    point = Point({theta: math.pi / 4})
    assert z.evaluate(point) == approx(0)
    assert z.local_partial(point, theta) == approx(-2)
    assert z.global_partial(theta).at(point) == approx(-2)
    assert z.local_differential(point).component(theta) == approx(-2)
    assert z.global_differential().component_at(point, theta) == approx(-2)
