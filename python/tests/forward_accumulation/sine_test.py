from pytest import approx
import math
from src.forward_accumulation.constant import Constant
from src.forward_accumulation.variable import Variable
from src.forward_accumulation.sine import Sine

def testSine():
    theta = Variable("theta")
    z = Sine(theta)
    result = z.derive({ theta: 0 }, theta)
    assert result.value == approx(0)
    assert result.partial == approx(1)
    result = z.derive({ theta: math.pi / 2 }, theta)
    assert result.value == approx(1)
    assert result.partial == approx(0)

def testSineComposition():
    theta = Variable("theta")
    z = Sine(Constant(2) * theta)
    result = z.derive({ theta: 0 }, theta)
    assert result.value == approx(0)
    assert result.partial == approx(2)
