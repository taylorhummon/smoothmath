from pytest import approx, raises
import math
from smoothmath.errors import DomainError
from smoothmath.point import Point
from smoothmath.expressions import Constant, Variable, Logarithm


def test_Logarithm():
    x = Variable("x")
    z = Logarithm(x)
    synthetic = z.synthetic()
    # at x = 1
    point = Point({x: 1})
    assert z.evaluate(point) == approx(0)
    assert z.partial_at(point, x) == approx(1)
    assert z.all_partials_at(point).partial_with_respect_to(x) == approx(1)
    assert synthetic.partial_at(point, x) == approx(1)
    # at x = e
    point = Point({x: math.e})
    assert z.evaluate(point) == approx(1)
    assert z.partial_at(point, x) == approx(1 / math.e)
    assert z.all_partials_at(point).partial_with_respect_to(x) == approx(1 / math.e)
    assert synthetic.partial_at(point, x) == approx(1 / math.e)
    # at x = 0
    point = Point({x: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.all_partials_at(point)
    with raises(DomainError):
        synthetic.partial_at(point, x)
    # at x = -1
    point = Point({x: -1})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.all_partials_at(point)
    with raises(DomainError):
        synthetic.partial_at(point, x)


def test_Logarithm_composition():
    x = Variable("x")
    z = Logarithm(Constant(2) * x - Constant(3))
    point = Point({x: 2})
    assert z.evaluate(point) == approx(0)
    assert z.partial_at(point, x) == approx(2)
    assert z.all_partials_at(point).partial_with_respect_to(x) == approx(2)
    assert z.synthetic().partial_at(point, x) == approx(2)


def test_base_two_Logarithm():
    x = Variable("x")
    z = Logarithm(x, base = 2)
    synthetic = z.synthetic()
    # at x = 1
    point = Point({x: 1})
    assert z.evaluate(point) == approx(0)
    assert z.partial_at(point, x) == approx(1.442695040888)
    assert z.all_partials_at(point).partial_with_respect_to(x) == approx(1.442695040888)
    assert synthetic.partial_at(point, x) == approx(1.442695040888)
    # at x = 2
    point = Point({x: 2})
    assert z.evaluate(point) == approx(1)
    assert z.partial_at(point, x) == approx(0.721347520444)
    assert z.all_partials_at(point).partial_with_respect_to(x) == approx(0.721347520444)
    assert synthetic.partial_at(point, x) == approx(0.721347520444)
    # at x = 0
    point = Point({x: 0})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.all_partials_at(point)
    with raises(DomainError):
        synthetic.partial_at(point, x)
    # at x = -1
    point = Point({x: -1})
    with raises(DomainError):
        z.evaluate(point)
    with raises(DomainError):
        z.partial_at(point, x)
    with raises(DomainError):
        z.all_partials_at(point)
    with raises(DomainError):
        synthetic.partial_at(point, x)


def test_base_two_Logarithm_composition():
    x = Variable("x")
    z = Logarithm(Constant(2) * x - Constant(6), base = 2)
    point = Point({x: 7})
    assert z.evaluate(point) == approx(3)
    assert z.partial_at(point, x) == approx(0.3606737602222)
    assert z.all_partials_at(point).partial_with_respect_to(x) == approx(0.3606737602222)
    assert z.synthetic().partial_at(point, x) == approx(0.3606737602222)
