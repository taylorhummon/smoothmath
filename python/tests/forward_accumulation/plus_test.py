from pytest import approx
from src.forward_accumulation.constant import Constant
from src.forward_accumulation.variable import Variable
from src.forward_accumulation.plus import Plus

def testPlus():
    x = Variable("x")
    y = Variable("y")
    z = Plus(x, y)
    variableValues = { x: 2, y: 3 }
    resultForX = z.derive(variableValues, x)
    assert resultForX.value == approx(5)
    assert resultForX.partial == approx(1)
    resultForY = z.derive(variableValues, y)
    assert resultForY.value == approx(5)
    assert resultForY.partial == approx(1)

def testPlusComposition():
    x = Variable("x")
    y = Variable("y")
    z = Plus(Constant(5) * x, Constant(4) * y)
    variableValues = { x: 2, y: 3 }
    resultForX = z.derive(variableValues, x)
    assert resultForX.value == approx(22)
    assert resultForX.partial == approx(5)
    resultForY = z.derive(variableValues, y)
    assert resultForY.value == approx(22)
    assert resultForY.partial == approx(4)
