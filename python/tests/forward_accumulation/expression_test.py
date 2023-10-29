from pytest import approx, raises
import math
from src.forward_accumulation.custom_exceptions import ArithmeticException
from src.forward_accumulation.expression import *

# !!! test 3.0 vs 3
# !!! test square root
# !!! clean up Power tests

### Constant

def testConstant():
    c = Constant(7)
    assert c.value == 7
    x = Variable()
    result = c.derive({ x: 2 }, x)
    assert result.value == 7
    assert result.partial == 0

### Variable

def testVariable():
    x = Variable()
    result = x.derive({ x: 2 }, x)
    assert result.value == 2
    assert result.partial == 1

def testUnrelatedVariables():
    x = Variable()
    y = Variable()
    result = y.derive({ x: 2, y: 3 }, x)
    assert result.value == 3
    assert result.partial == 0

### Negation

def testNegation():
    x = Variable()
    z = Negation(x)
    result = z.derive({ x: 2 }, x)
    assert result.value == -2
    assert result.partial == -1

### Reciprocal

def testReciprocal():
    x = Variable()
    z = Reciprocal(x)
    result = z.derive({ x: 2 }, x)
    assert result.value == approx(0.5)
    assert result.partial == approx(-0.25)
    with raises(ArithmeticException):
        z.derive({ x: 0 }, x)

### Natural Exponential

def testNaturalExponential():
    x = Variable()
    z = NaturalExponential(x)
    result = z.derive({ x: 0 }, x)
    assert result.value == approx(1.0)
    assert result.partial == approx(1.0)
    result = z.derive({ x: 1 }, x)
    assert result.value == approx(math.e)
    assert result.partial == approx(math.e)

### Natural Logarithm

def testNaturalLogarithm():
    x = Variable()
    z = NaturalLogarithm(x)
    result = z.derive({ x: 1 }, x)
    assert result.value == approx(0.0)
    assert result.partial == approx(1.0)
    result = z.derive({ x: math.e }, x)
    assert result.value == approx(1.0)
    assert result.partial == approx(1.0 / math.e)
    with raises(ArithmeticException):
        z.derive({ x: 0.0 }, x)
    with raises(ArithmeticException):
        z.derive({ x: -3.0 }, x)

### Sine

def testSine():
    theta = Variable()
    z = Sine(theta)
    result = z.derive({ theta: 0.0 }, theta)
    assert result.value == approx(0.0)
    assert result.partial == approx(1.0)
    result = z.derive({ theta: math.pi / 2 }, theta)
    assert result.value == approx(1.0)
    assert result.partial == approx(0.0)

### Cosine

def testCosine():
    theta = Variable()
    z = Cosine(theta)
    result = z.derive({ theta: 0.0 }, theta)
    assert result.value == approx(1.0)
    assert result.partial == approx(0.0)
    result = z.derive({ theta: math.pi / 2 }, theta)
    assert result.value == approx(0.0)
    assert result.partial == approx(-1.0)

### Plus

def testPlus():
    x = Variable()
    y = Variable()
    z = Plus(x, y)
    resultForX = z.derive({ x: 2, y: 3 }, x)
    assert resultForX.value == approx(5.0)
    assert resultForX.partial == approx(1.0)
    resultForY = z.derive({ x: 2, y: 3 }, y)
    assert resultForY.value == approx(5.0)
    assert resultForY.partial == approx(1.0)

### Minus

def testMinus():
    x = Variable()
    y = Variable()
    z = Minus(x, y)
    resultForX = z.derive({ x: 2, y: 3 }, x)
    assert resultForX.value == approx(-1.0)
    assert resultForX.partial == approx(1.0)
    resultForY = z.derive({ x: 2, y: 3 }, y)
    assert resultForY.value == approx(-1.0)
    assert resultForY.partial == approx(-1.0)

### Multiply

def testMultiply():
    x = Variable()
    y = Variable()
    z = Multiply(x, y)
    resultForX = z.derive({ x: 2, y: 3 }, x)
    assert resultForX.value == approx(6.0)
    assert resultForX.partial == approx(3.0)
    resultForY = z.derive({ x: 2, y: 3 }, y)
    assert resultForY.value == approx(6.0)
    assert resultForY.partial == approx(2.0)

### Divide

def testDivide():
    x = Variable()
    y = Variable()
    z = Divide(x, y)
    resultForX = z.derive({ x: 5, y: 2 }, x)
    assert resultForX.value == approx(2.5)
    assert resultForX.partial == approx(0.5)
    resultForY = z.derive({ x: 5, y: 2 }, y)
    assert resultForY.value == approx(2.5)
    assert resultForY.partial == approx(-1.25)
    with raises(ArithmeticException):
        z.derive({ x: 3.0, y: 0.0 }, x)
    with raises(ArithmeticException):
        z.derive({ x: 3.0, y: 0.0 }, y)

### PowerWithIntegralExponent

def testPowerWithIntegralExponent():
    x = Variable()
    c = Constant(2)
    z = Power(x, c)
    result = z.derive({ x: 3 }, x)
    assert result.value == approx(9.0)
    assert result.partial == approx(6.0)

def testPowerWithIntegralExponentAndNegativeBase():
    x = Variable()
    c = Constant(2)
    z = Power(x, c)
    result = z.derive({ x: -5 }, x)
    assert result.value == approx(25.0)
    assert result.partial == approx(-10.0)

def testPowerWithIntegralExponentAndZeroBase():
    x = Variable()
    c = Constant(2)
    z = Power(x, c)
    result = z.derive({ x: 0 }, x)
    assert result.value == approx(0.0)
    assert result.partial == approx(0.0)

def testPowerWithNegativeIntegralExponent():
    x = Variable()
    c = Constant(-2)
    z = Power(x, c)
    result = z.derive({ x: 2 }, x)
    assert result.value == approx(0.25)
    assert result.partial == approx(-0.25)

def testPowerWithNegativeIntegralExponentAndNegativeBase():
    x = Variable()
    c = Constant(-2)
    z = Power(x, c)
    result = z.derive({ x: -2 }, x)
    assert result.value == approx(0.25)
    assert result.partial == approx(0.25)

def testPowerWithNegativeIntegralExponentAndZeroBase():
    x = Variable()
    c = Constant(-2)
    z = Power(x, c)
    with raises(ArithmeticException):
        z.derive({ x: 0 }, x)

### Power

def testPower():
    x = Variable()
    y = Variable()
    z = Power(x, y)
    resultForX = z.derive({ x: 3.0, y: 2.5 }, x)
    assert resultForX.value == approx(15.588457268)
    assert resultForX.partial == approx(12.990381056)
    resultForY = z.derive({ x: 3.0, y: 2.5 }, y)
    assert resultForY.value == approx(15.588457268)
    assert resultForY.partial == approx(17.125670716)

def testPowerWithNegativeBase():
    x = Variable()
    y = Variable()
    z = Power(x, y)
    with raises(ArithmeticException):
        z.derive({ x: -3.0, y: 2.5 }, x)
    with raises(ArithmeticException):
        z.derive({ x: -3.0, y: 2.5 }, y)

def testPowerWithZeroBase():
    x = Variable()
    y = Variable()
    z = Power(x, y)
    with raises(ArithmeticException):
        z.derive({ x: 0.0, y: 2.5 }, x)
    with raises(ArithmeticException):
        z.derive({ x: 0.0, y: 2.5 }, y)

def testPowerWithNegativeExponent():
    x = Variable()
    y = Variable()
    z = Power(x, y)
    resultForX = z.derive({ x: 3.0, y: -2.5 }, x)
    assert resultForX.value == approx(0.0641500299)
    assert resultForX.partial == approx(-0.0534583582)
    resultForY = z.derive({ x: 3.0, y: -2.5 }, y)
    assert resultForY.value == approx(0.0641500299)
    assert resultForY.partial == approx(0.0704760111)

def testPowerWithZeroExponent():
    x = Variable()
    y = Variable()
    z = Power(x, y)
    resultForX = z.derive({ x: 3.0, y: 0.0 }, x)
    assert resultForX.value == approx(1.0)
    assert resultForX.partial == approx(0.0)
    resultForY = z.derive({ x: 3.0, y: 0.0 }, y)
    assert resultForY.value == approx(1.0)
    assert resultForY.partial == approx(1.0986122886)

def testPowerWithZeroBaseAndZeroExponent():
    x = Variable()
    y = Variable()
    z = Power(x, y)
    with raises(ArithmeticException):
        z.derive({ x: 0.0, y: 0.0 }, x)
    with raises(ArithmeticException):
        z.derive({ x: 0.0, y: 0.0 }, y)

### Polynomials

def testPolynomialOfOneVariable():
    x = Variable()
    z = x * x - Constant(6) * x + Constant(4)
    result = z.derive({ x: 2 }, x)
    assert result.value == -4
    assert result.partial == -2

def testPolynomialOfTwoVariables():
    x = Variable()
    y = Variable()
    z = x * (x + y) - Constant(5) * y * y
    resultForX = z.derive({ x: 2, y: 3 }, x)
    resultForY = z.derive({ x: 2, y: 3 }, y)
    assert resultForX.value == -35
    assert resultForX.partial == 7
    assert resultForY.value == -35
    assert resultForY.partial == -28

def testPolynomialOfThreeVariables():
    w = Variable()
    x = Variable()
    y = Variable()
    z = w * w + Constant(5) * w * x * x - w * x * y
    resultForW = z.derive({ w: 2, x: 3, y: 4 }, w)
    resultForX = z.derive({ w: 2, x: 3, y: 4 }, x)
    resultForY = z.derive({ w: 2, x: 3, y: 4 }, y)
    assert resultForW.value == 70
    assert resultForW.partial == 37
    assert resultForX.value == 70
    assert resultForX.partial == 52
    assert resultForY.value == 70
    assert resultForY.partial == -6

### Other

def testCompositeFunction():
    x = Variable()
    z = NaturalExponential(x ** Constant(2))
    result = z.derive({ x: 2 }, x)
    assert result.value == approx(54.598150033)
    assert result.partial == approx(218.392600132)

def testExpressionReuse():
    x = Variable()
    w = x ** Constant(2)
    z = (w + Constant(1)) / w
    result = z.derive({ x: 2 }, x)
    assert result.value == approx(1.25)
    assert result.partial == approx(-0.25)
