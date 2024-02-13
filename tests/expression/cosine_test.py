from pytest import approx
import math
from smoothmath import Point
from smoothmath.expression import Variable, Constant, Negation, Cosine


def test_Cosine():
    theta = Variable("theta")
    z = Cosine(theta)
    global_theta_partial = z.global_partial(theta)
    global_differential = z.global_differential()
    # at theta = 0
    point = Point(theta = 0)
    assert z.evaluate(point) == approx(1)
    assert z.local_partial(theta, point) == approx(0)
    assert global_theta_partial.at(point) == approx(0)
    assert z.local_differential(point).component(theta) == approx(0)
    assert global_differential.component_at(theta, point) == approx(0)
    # at theta = tau / 4
    point = Point(theta = math.tau / 4)
    assert z.evaluate(point) == approx(0)
    assert z.local_partial(theta, point) == approx(-1)
    assert global_theta_partial.at(point) == approx(-1)
    assert z.local_differential(point).component(theta) == approx(-1)
    assert global_differential.component_at(theta, point) == approx(-1)


def test_Cosine_composition():
    theta = Variable("theta")
    z = Cosine(Constant(2) * theta)
    point = Point(theta = math.tau / 8)
    assert z.evaluate(point) == approx(0)
    assert z.local_partial(theta, point) == approx(-2)
    assert z.global_partial(theta).at(point) == approx(-2)
    assert z.local_differential(point).component(theta) == approx(-2)
    assert z.global_differential().component_at(theta, point) == approx(-2)


def test_Cosine_normalization():
    theta = Variable("theta")
    z = Cosine(theta)
    assert z._normalize() == Cosine(theta)
    z = Cosine(Negation(theta))
    assert z._normalize() == Cosine(theta)
