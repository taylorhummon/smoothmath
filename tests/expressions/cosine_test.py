from pytest import approx
import math
from smoothmath.point import Point
from smoothmath.expressions import Constant, Variable, Cosine


def test_Cosine():
    theta = Variable("theta")
    z = Cosine(theta)
    synthetic = z.synthetic()
    # at theta = 0
    point = Point({theta: 0})
    assert z.evaluate(point) == approx(1)
    assert z.partial_at(point, theta) == approx(0)
    assert z.all_partials_at(point).partial_with_respect_to(theta) == approx(0)
    assert synthetic.partial_at(point, theta) == approx(0)
    # theta = pi / 2
    point = Point({theta: math.pi / 2})
    assert z.evaluate(point) == approx(0)
    assert z.partial_at(point, theta) == approx(-1)
    assert z.all_partials_at(point).partial_with_respect_to(theta) == approx(-1)
    assert synthetic.partial_at(point, theta) == approx(-1)


def test_Cosine_composition():
    theta = Variable("theta")
    z = Cosine(Constant(2) * theta)
    point = Point({theta: math.pi / 4})
    assert z.evaluate(point) == approx(0)
    assert z.partial_at(point, theta) == approx(-2)
    assert z.all_partials_at(point).partial_with_respect_to(theta) == approx(-2)
    assert z.synthetic().partial_at(point, theta) == approx(-2)
