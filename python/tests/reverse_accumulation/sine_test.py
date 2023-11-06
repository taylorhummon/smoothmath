from pytest import approx
import math
from src.reverse_accumulation.constant import Constant
from src.reverse_accumulation.variable import Variable
from src.reverse_accumulation.sine import Sine

def testSine():
    theta = Variable("theta")
    z = Sine(theta)
    result = z.derive({ theta: 0 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(theta) == approx(1)
    result = z.derive({ theta: math.pi / 2 })
    assert result.value == approx(1)
    assert result.partialWithRespectTo(theta) == approx(0)

def testSineComposition():
    theta = Variable("theta")
    z = Sine(Constant(2) * theta)
    result = z.derive({ theta: 0 })
    assert result.value == approx(0)
    assert result.partialWithRespectTo(theta) == approx(2)
