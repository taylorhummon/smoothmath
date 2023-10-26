from pytest import approx, raises
import math
from src.forward_accumulation.expression import *

### Constant

def testConstant():
    c = Constant(7)
    assert c.value == 7
    x = Variable(2)
    valueAndPartial = c.evaluateAndDerive(x)
    assert valueAndPartial.value == 7
    assert valueAndPartial.partial == 0

### Variable

def testVariable():
    x = Variable(2)
    valueAndPartial = x.evaluateAndDerive(x)
    assert valueAndPartial.value == 2
    assert valueAndPartial.partial == 1

def testUnrelatedVariables():
    x = Variable(2)
    y = Variable(3)
    valueAndPartial = y.evaluateAndDerive(x)
    assert valueAndPartial.value == 3
    assert valueAndPartial.partial == 0

### Negation

def testNegation():
    x = Variable(2)
    z = Negation(x)
    valueAndPartial = z.evaluateAndDerive(x)
    assert valueAndPartial.value == -2
    assert valueAndPartial.partial == -1

### Reciprocal

def testReciprocal():
    x = Variable(2)
    z = Reciprocal(x)
    valueAndPartial = z.evaluateAndDerive(x)
    assert valueAndPartial.value == approx(0.5)
    assert valueAndPartial.partial == approx(-0.25)

def testReciprocalAtZero():
    x = Variable(0)
    z = Reciprocal(x)
    with raises(Exception):
        z.evaluateAndDerive(x)

### Natural Exponential

def testNaturalExponentialAtZero():
    x = Variable(0)
    z = NaturalExponential(x)
    valueAndPartial = z.evaluateAndDerive(x)
    assert valueAndPartial.value == approx(1.0)
    assert valueAndPartial.partial == approx(1.0)

def testNaturalExponentialAtOne():
    x = Variable(1)
    z = NaturalExponential(x)
    valueAndPartial = z.evaluateAndDerive(x)
    assert valueAndPartial.value == approx(math.e)
    assert valueAndPartial.partial == approx(math.e)

### Natural Logarithm

def testNaturalLogarithmAtOne():
    x = Variable(1)
    z = NaturalLogarithm(x)
    valueAndPartial = z.evaluateAndDerive(x)
    assert valueAndPartial.value == approx(0.0)
    assert valueAndPartial.partial == approx(1.0)

def testNaturalLogarithmAtE():
    x = Variable(math.e)
    z = NaturalLogarithm(x)
    valueAndPartial = z.evaluateAndDerive(x)
    assert valueAndPartial.value == approx(1.0)
    assert valueAndPartial.partial == approx(1.0 / math.e)

def testNaturalLogarithmAtZero():
    x = Variable(0.0)
    z = NaturalLogarithm(x)
    with raises(Exception):
        z.evaluateAndDerive(x)

def testNaturalLogarithmAtNegative():
    x = Variable(-3.0)
    z = NaturalLogarithm(x)
    with raises(Exception):
        z.evaluateAndDerive(x)

### Sine

def testSineAtZero():
    theta = Variable(0.0)
    z = Sine(theta)
    valueAndPartial = z.evaluateAndDerive(theta)
    assert valueAndPartial.value == approx(0.0)
    assert valueAndPartial.partial == approx(1.0)

def testSineAtOneQuarterTurn():
    theta = Variable(math.pi / 2)
    z = Sine(theta)
    valueAndPartial = z.evaluateAndDerive(theta)
    assert valueAndPartial.value == approx(1.0)
    assert valueAndPartial.partial == approx(0.0)

### Cosine

def testCosineAtZero():
    theta = Variable(0.0)
    z = Cosine(theta)
    valueAndPartial = z.evaluateAndDerive(theta)
    assert valueAndPartial.value == approx(1.0)
    assert valueAndPartial.partial == approx(0.0)

def testCosineAtOneQuarterTurn():
    theta = Variable(math.pi / 2)
    z = Cosine(theta)
    valueAndPartial = z.evaluateAndDerive(theta)
    assert valueAndPartial.value == approx(0.0)
    assert valueAndPartial.partial == approx(-1.0)

### Plus

def testPlus():
    x = Variable(2)
    y = Variable(3)
    z = Plus(x, y)
    valueAndPartialForX = z.evaluateAndDerive(x)
    assert valueAndPartialForX.value == approx(5.0)
    assert valueAndPartialForX.partial == approx(1.0)
    valueAndPartialForY = z.evaluateAndDerive(y)
    assert valueAndPartialForY.value == approx(5.0)
    assert valueAndPartialForY.partial == approx(1.0)

### Minus

def testMinus():
    x = Variable(2)
    y = Variable(3)
    z = Minus(x, y)
    valueAndPartialForX = z.evaluateAndDerive(x)
    assert valueAndPartialForX.value == approx(-1.0)
    assert valueAndPartialForX.partial == approx(1.0)
    valueAndPartialForY = z.evaluateAndDerive(y)
    assert valueAndPartialForY.value == approx(-1.0)
    assert valueAndPartialForY.partial == approx(-1.0)

### Multiply

def testMultiply():
    x = Variable(2)
    y = Variable(3)
    z = Multiply(x, y)
    valueAndPartialForX = z.evaluateAndDerive(x)
    assert valueAndPartialForX.value == approx(6.0)
    assert valueAndPartialForX.partial == approx(3.0)
    valueAndPartialForY = z.evaluateAndDerive(y)
    assert valueAndPartialForY.value == approx(6.0)
    assert valueAndPartialForY.partial == approx(2.0)

### Divide

def testDivide():
    x = Variable(5)
    y = Variable(2)
    z = Divide(x, y)
    valueAndPartialForX = z.evaluateAndDerive(x)
    assert valueAndPartialForX.value == approx(2.5)
    assert valueAndPartialForX.partial == approx(0.5)
    valueAndPartialForY = z.evaluateAndDerive(y)
    assert valueAndPartialForY.value == approx(2.5)
    assert valueAndPartialForY.partial == approx(-1.25)

### PowerWithIntegralExponent

def testPowerWithIntegralExponent():
    x = Variable(3)
    c = Constant(2)
    z = PowerWithIntegralExponent(x, c)
    valueAndPartial = z.evaluateAndDerive(x)
    assert valueAndPartial.value == approx(9.0)
    assert valueAndPartial.partial == approx(6.0)

def testPowerWithIntegralExponentAndNegativeBase():
    x = Variable(-5)
    c = Constant(2)
    z = PowerWithIntegralExponent(x, c)
    valueAndPartial = z.evaluateAndDerive(x)
    assert valueAndPartial.value == approx(25.0)
    assert valueAndPartial.partial == approx(-10.0)

def testPowerWithIntegralExponentAndZeroBase():
    x = Variable(0)
    c = Constant(2)
    z = PowerWithIntegralExponent(x, c)
    valueAndPartial = z.evaluateAndDerive(x)
    assert valueAndPartial.value == approx(0.0)
    assert valueAndPartial.partial == approx(0.0)

def testPowerWithNegativeIntegralExponent():
    x = Variable(2)
    c = Constant(-2)
    z = PowerWithIntegralExponent(x, c)
    valueAndPartial = z.evaluateAndDerive(x)
    assert valueAndPartial.value == approx(0.25)
    assert valueAndPartial.partial == approx(-0.25)

def testPowerWithNegativeIntegralExponentAndNegativeBase():
    x = Variable(-2)
    c = Constant(-2)
    z = PowerWithIntegralExponent(x, c)
    valueAndPartial = z.evaluateAndDerive(x)
    assert valueAndPartial.value == approx(0.25)
    assert valueAndPartial.partial == approx(0.25)

def testPowerWithNegativeIntegralExponentAndZeroBase():
    x = Variable(0)
    c = Constant(-2)
    z = PowerWithIntegralExponent(x, c)
    with raises(Exception):
        z.evaluateAndDerive(x)

### Power

def testPower():
    x = Variable(3.0)
    y = Variable(2.5)
    z = Power(x, y)
    valueAndPartialForX = z.evaluateAndDerive(x)
    assert valueAndPartialForX.value == approx(15.588457268)
    assert valueAndPartialForX.partial == approx(12.990381056)
    valueAndPartialForY = z.evaluateAndDerive(y)
    assert valueAndPartialForY.value == approx(15.588457268)
    assert valueAndPartialForY.partial == approx(17.125670716)

def testPowerWithNegativeBase():
    x = Variable(-3.0)
    y = Variable(2.5)
    z = Power(x, y)
    with raises(Exception):
        z.evaluateAndDerive(x)
    with raises(Exception):
        z.evaluateAndDerive(y)

def testPowerWithZeroBase():
    x = Variable(0.0)
    y = Variable(2.5)
    z = Power(x, y)
    with raises(Exception):
        z.evaluateAndDerive(x)
    with raises(Exception):
        z.evaluateAndDerive(y)

def testPowerWithNegativeExponent():
    x = Variable(3.0)
    y = Variable(-2.5)
    z = Power(x, y)
    valueAndPartialForX = z.evaluateAndDerive(x)
    assert valueAndPartialForX.value == approx(0.0641500299)
    assert valueAndPartialForX.partial == approx(-0.0534583582)
    valueAndPartialForY = z.evaluateAndDerive(y)
    assert valueAndPartialForY.value == approx(0.0641500299)
    assert valueAndPartialForY.partial == approx(0.0704760111)

def testPowerWithZeroExponent():
    x = Variable(3.0)
    y = Variable(0.0)
    z = Power(x, y)
    valueAndPartialForX = z.evaluateAndDerive(x)
    assert valueAndPartialForX.value == approx(1.0)
    assert valueAndPartialForX.partial == approx(0.0)
    valueAndPartialForY = z.evaluateAndDerive(y)
    assert valueAndPartialForY.value == approx(1.0)
    assert valueAndPartialForY.partial == approx(1.0986122886)

def testPowerWithZeroBaseAndZeroExponent():
    x = Variable(0.0)
    y = Variable(0.0)
    z = Power(x, y)
    with raises(Exception):
        z.evaluateAndDerive(x)
    with raises(Exception):
        z.evaluateAndDerive(y)

### Polynomials

def testPolynomialOfOneVariable():
    x = Variable(2)
    z = x * x - Constant(6) * x + Constant(4)
    valueAndPartial = z.evaluateAndDerive(x)
    assert valueAndPartial.value == -4
    assert valueAndPartial.partial == -2

def testPolynomialOfTwoVariables():
    x = Variable(2)
    y = Variable(3)
    z = x * (x + y) - Constant(5) * y * y
    valueAndPartialForX = z.evaluateAndDerive(x)
    valueAndPartialForY = z.evaluateAndDerive(y)
    assert valueAndPartialForX.value == -35
    assert valueAndPartialForX.partial == 7
    assert valueAndPartialForY.value == -35
    assert valueAndPartialForY.partial == -28

def testPolynomialOfThreeVariables():
    w = Variable(2)
    x = Variable(3)
    y = Variable(4)
    z = w * w + Constant(5) * w * x * x - w * x * y
    valueAndPartialForW = z.evaluateAndDerive(w)
    valueAndPartialForX = z.evaluateAndDerive(x)
    valueAndPartialForY = z.evaluateAndDerive(y)
    assert valueAndPartialForW.value == 70
    assert valueAndPartialForW.partial == 37
    assert valueAndPartialForX.value == 70
    assert valueAndPartialForX.partial == 52
    assert valueAndPartialForY.value == 70
    assert valueAndPartialForY.partial == -6

### Other

def testCompositeFunction():
    x = Variable(2)
    z = NaturalExponential(x ** Constant(2))
    valueAndPartial = z.evaluateAndDerive(x)
    assert valueAndPartial.value == approx(54.598150033)
    assert valueAndPartial.partial == approx(218.392600132)

def testExpressionReuse():
    x = Variable(2)
    w = x ** Constant(2)
    z = (w + Constant(1)) / w
    valueAndPartial = z.evaluateAndDerive(x)
    assert valueAndPartial.value == approx(1.25)
    assert valueAndPartial.partial == approx(-0.25)
