from pytest import approx
import math
from src.forward_accumulation.constant import Constant
from src.forward_accumulation.variable import Variable
from src.forward_accumulation.cosine import Cosine

def testCosine():
    theta = Variable("theta")
    z = Cosine(theta)
    result = z.derive({ theta: 0 }, theta)
    assert result.value == approx(1)
    assert result.partial == approx(0)
    result = z.derive({ theta: math.pi / 2 }, theta)
    assert result.value == approx(0)
    assert result.partial == approx(-1)

def testCosineComposition():
    theta = Variable("theta")
    z = Cosine(Constant(2) * theta)
    result = z.derive({ theta: math.pi / 4 }, theta)
    assert result.value == approx(0)
    assert result.partial == approx(-2)
