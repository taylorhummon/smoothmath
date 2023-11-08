from pytest import approx, raises
from src.smooth_expression.custom_exceptions import DomainException
from src.smooth_expression.constant import Constant
from src.smooth_expression.variable import Variable
from src.smooth_expression.reciprocal import Reciprocal

def testReciprocal():
    x = Variable("x")
    z = Reciprocal(x)
    partial = z.deriveSingle({ x: 2 }, x)
    assert partial == approx(-0.25)
    with raises(DomainException):
        z.deriveSingle({ x: 0 }, x)
    partial = z.deriveSingle({ x: -1 }, x)
    assert partial == approx(-1)

def testReciprocalComposition():
    x = Variable("x")
    z = Reciprocal(Constant(2) * x - Constant(4))
    partial = z.deriveSingle({ x: 3 }, x)
    assert partial == approx(-0.5)

def testReciprocalMulti():
    x = Variable("x")
    z = Reciprocal(x)
    multiResult = z.deriveMulti({ x: 2 })
    assert multiResult.value == approx(0.5)
    assert multiResult.partialWithRespectTo(x) == approx(-0.25)
    with raises(DomainException):
        z.deriveMulti({ x: 0 })
    multiResult = z.deriveMulti({ x: -1 })
    assert multiResult.value == approx(-1)
    assert multiResult.partialWithRespectTo(x) == approx(-1)

def testReciprocalCompositionMulti():
    x = Variable("x")
    z = Reciprocal(Constant(2) * x - Constant(4))
    multiResult = z.deriveMulti({ x: 3 })
    assert multiResult.value == approx(0.5)
    assert multiResult.partialWithRespectTo(x) == approx(-0.5)
