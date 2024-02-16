from pytest import approx
import math
from smoothmath import Point
from smoothmath.expression import Variable, Constant, Negation, Sine
from assert_derivatives import assert_1_ary_derivatives # type: ignore


def test_Sine():
    theta = Variable("theta")
    z = Sine(theta)
    # at theta = 0
    point = Point(theta = 0)
    assert z.at(point) == approx(0)
    assert_1_ary_derivatives(z, point, theta, 1)
    # at theta = tau / 4
    point = Point(theta = math.tau / 4)
    assert z.at(point) == approx(1)
    assert_1_ary_derivatives(z, point, theta, 0)


def test_Sine_composition():
    theta = Variable("theta")
    z = Sine(Constant(2) * theta)
    point = Point(theta = 0)
    assert z.at(point) == approx(0)
    assert_1_ary_derivatives(z, point, theta, 2)


def test_Sine_normalization():
    theta = Variable("theta")
    z = Sine(theta)
    assert z._normalize() == Sine(theta)
    z = Sine(Negation(theta))
    assert z._normalize() == Negation(Sine(theta))
