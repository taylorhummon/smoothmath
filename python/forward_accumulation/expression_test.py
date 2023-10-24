from pytest import approx, raises
import math
from expression import *

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

def testNaturalLogarithmAt0():
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

def testSineAt0():
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

def testCosineAt0():
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

def testPowerWithNegativeIntegralExponent():
    x = Variable(2)
    c = Constant(-2)
    z = PowerWithIntegralExponent(x, c)
    valueAndPartial = z.evaluateAndDerive(x)
    assert valueAndPartial.value == approx(0.25)
    assert valueAndPartial.partial == approx(-0.25)

def testPowerWithPositiveIntegralExponentAndZeroBase():
    x = Variable(0)
    c = Constant(2)
    z = PowerWithIntegralExponent(x, c)
    valueAndPartial = z.evaluateAndDerive(x)
    assert valueAndPartial.value == approx(0.0)
    assert valueAndPartial.partial == approx(0.0)

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
    valueAndPartial = z.evaluateAndDerive(x)
    assert valueAndPartial.value == approx(15.588457268)
    assert valueAndPartial.partial == approx(12.990381056)

def testPowerWithNegativeBase():
    x = Variable(-3.0)
    y = Variable(2.5)
    z = Power(x, y)
    with raises(Exception):
        z.evaluateAndDerive(x)

### Other

def testPolynomialOfTwoVariables():
    x = Variable(2)
    y = Variable(3)
    c = Constant(5)
    z = x * (x + y) + c * y * y
    xPartial = z.evaluateAndDerive(x).partial
    yPartial = z.evaluateAndDerive(y).partial
    assert xPartial == 7
    assert yPartial == 32


# !!! test chain rule
# !!! test expression aliasing
