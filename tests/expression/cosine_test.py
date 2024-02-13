from pytest import approx
import math
from smoothmath import Point
from smoothmath.expression import Variable, Constant, Negation, Cosine
from assert_derivatives import assert_1_ary_derivatives # type: ignore


def test_Cosine():
    theta = Variable("theta")
    z = Cosine(theta)
    # at theta = 0
    point = Point(theta = 0)
    assert z.evaluate(point) == approx(1)
    assert_1_ary_derivatives(z, point, theta, 0)
    # at theta = tau / 4
    point = Point(theta = math.tau / 4)
    assert z.evaluate(point) == approx(0)
    assert_1_ary_derivatives(z, point, theta, -1)


def test_Cosine_composition():
    theta = Variable("theta")
    z = Cosine(Constant(2) * theta)
    point = Point(theta = math.tau / 8)
    assert z.evaluate(point) == approx(0)
    assert_1_ary_derivatives(z, point, theta, -2)


def test_Cosine_normalization():
    theta = Variable("theta")
    z = Cosine(theta)
    assert z._normalize() == Cosine(theta)
    z = Cosine(Negation(theta))
    assert z._normalize() == Cosine(theta)
