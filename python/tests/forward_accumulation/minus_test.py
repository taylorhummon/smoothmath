from pytest import approx
from src.forward_accumulation.constant import Constant
from src.forward_accumulation.variable import Variable
from src.forward_accumulation.minus import Minus

def testMinus():
    x = Variable("x")
    y = Variable("y")
    z = Minus(x, y)
    variableValues = { x: 2, y: 3 }
    resultForX = z.derive(variableValues, x)
    assert resultForX.value == approx(-1)
    assert resultForX.partial == approx(1)
    resultForY = z.derive(variableValues, y)
    assert resultForY.value == approx(-1)
    assert resultForY.partial == approx(-1)

def testMinusComposition():
    x = Variable("x")
    y = Variable("y")
    z = Minus(Constant(5) * x, Constant(4) * y)
    variableValues = { x: 2, y: 3 }
    resultForX = z.derive(variableValues, x)
    assert resultForX.value == approx(-2)
    assert resultForX.partial == approx(5)
    resultForY = z.derive(variableValues, y)
    assert resultForY.value == approx(-2)
    assert resultForY.partial == approx(-4)
