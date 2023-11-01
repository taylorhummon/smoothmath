from pytest import approx, raises
import math
from src.reverse_accumulation.custom_exceptions import DomainException
from src.reverse_accumulation.expression import (
    Constant, Variable,
    Negation, Reciprocal, SquareRoot, NaturalExponential, NaturalLogarithm, Sine, Cosine,
    Plus, Minus, Multiply, Divide, Power,
)

### Constant

def testConstant():
    c = Constant(7)
    x = Variable()
    result = c.derive({ x: 2 })
    assert result.value == 7
    assert result.partialWithRespectTo(x) == 0

### Variable

def testVariable():
    x = Variable()
    y = Variable()
    result = x.derive({ x: 2, y: 3 })
    assert result.value == 2
    assert result.partialWithRespectTo(x) == 1
    assert result.partialWithRespectTo(y) == 0

### Negation

def testNegation():
    x = Variable()
    z = Negation(x)
    result = z.derive({ x: 2 })
    assert result.value == -2
    assert result.partialWithRespectTo(x) == -1

### Reciprocal

def testReciprocal():
    x = Variable()
    z = Reciprocal(x)
    result = z.derive({ x: 2 })
    assert result.value == approx(0.5)
    assert result.partialWithRespectTo(x) == approx(-0.25)
    with raises(DomainException):
        z.derive({ x: 0 })
    result = z.derive({ x: -1 })
    assert result.value == approx(-1.0)
    assert result.partialWithRespectTo(x) == approx(-1.0)

### Square Root

def testSquareRoot():
    x = Variable()
    z = SquareRoot(x)
    result = z.derive({ x: 4 })
    assert result.value == approx(2.0)
    assert result.partialWithRespectTo(x) == approx(0.25)
    with raises(DomainException):
        z.derive({ x: 0 })
    with raises(DomainException):
        z.derive({ x: -1 })

### Natural Exponential

def testNaturalExponential():
    x = Variable()
    z = NaturalExponential(x)
    result = z.derive({ x: 0 })
    assert result.value == approx(1.0)
    assert result.partialWithRespectTo(x) == approx(1.0)
    result = z.derive({ x: 1 })
    assert result.value == approx(math.e)
    assert result.partialWithRespectTo(x) == approx(math.e)
    result = z.derive({ x: -1 })
    assert result.value == approx(1.0 / math.e)
    assert result.partialWithRespectTo(x) == approx(1.0 / math.e)

### Natural Logarithm

def testNaturalLogarithm():
    x = Variable()
    z = NaturalLogarithm(x)
    result = z.derive({ x: 1 })
    assert result.value == approx(0.0)
    assert result.partialWithRespectTo(x) == approx(1.0)
    result = z.derive({ x: math.e })
    assert result.value == approx(1.0)
    assert result.partialWithRespectTo(x) == approx(1.0 / math.e)
    with raises(DomainException):
        z.derive({ x: 0.0 })
    with raises(DomainException):
        z.derive({ x: -1.0 })

### Sine

def testSine():
    theta = Variable()
    z = Sine(theta)
    result = z.derive({ theta: 0.0 })
    assert result.value == approx(0.0)
    assert result.partialWithRespectTo(theta) == approx(1.0)
    result = z.derive({ theta: math.pi / 2 })
    assert result.value == approx(1.0)
    assert result.partialWithRespectTo(theta) == approx(0.0)

### Cosine

def testCosine():
    theta = Variable()
    z = Cosine(theta)
    result = z.derive({ theta: 0.0 })
    assert result.value == approx(1.0)
    assert result.partialWithRespectTo(theta) == approx(0.0)
    result = z.derive({ theta: math.pi / 2 })
    assert result.value == approx(0.0)
    assert result.partialWithRespectTo(theta) == approx(-1.0)

### Plus

def testPlus():
    x = Variable()
    y = Variable()
    z = Plus(x, y)
    result = z.derive({ x: 2, y: 3 })
    assert result.value == approx(5.0)
    assert result.partialWithRespectTo(x) == approx(1.0)
    assert result.partialWithRespectTo(y) == approx(1.0)

### Minus

def testMinus():
    x = Variable()
    y = Variable()
    z = Minus(x, y)
    result = z.derive({ x: 2, y: 3 })
    assert result.value == approx(-1.0)
    assert result.partialWithRespectTo(x) == approx(1.0)
    assert result.partialWithRespectTo(y) == approx(-1.0)

### Multiply

def testMultiply():
    x = Variable()
    y = Variable()
    z = Multiply(x, y)
    result = z.derive({ x: 2, y: 3 })
    assert result.value == approx(6.0)
    assert result.partialWithRespectTo(x) == approx(3.0)
    assert result.partialWithRespectTo(y) == approx(2.0)

### Divide

def testDivide():
    x = Variable()
    y = Variable()
    z = Divide(x, y)
    result = z.derive({ x: 5, y: 2 })
    assert result.value == approx(2.5)
    assert result.partialWithRespectTo(x) == approx(0.5)
    assert result.partialWithRespectTo(y) == approx(-1.25)
    with raises(DomainException):
        z.derive({ x: 3.0, y: 0.0 })
    with raises(DomainException):
        z.derive({ x: 0.0, y: 0.0 })

def testDivideWithConstantNumeratorZero():
    y = Variable()
    z = Divide(Constant(0), y)
    result = z.derive({ y: 3.0 })
    assert result.value == approx(0.0)
    assert result.partialWithRespectTo(y) == approx(0.0)
    result = z.derive({ y: 0.0 })
    assert result.value == approx(0.0)
    assert result.partialWithRespectTo(y) == approx(0.0)

def testDivideWithConstantDenominatorOne():
    x = Variable()
    z = Divide(x, Constant(1))
    result = z.derive({ x: 3.0 })
    assert result.value == approx(3.0)
    assert result.partialWithRespectTo(x) == approx(1.0)
    result = z.derive({ x: 0.0 })
    assert result.value == approx(0.0)
    assert result.partialWithRespectTo(x) == approx(1.0)

def testDivideWithConstantDenominatorZero():
    x = Variable()
    z = Divide(x, Constant(0))
    with raises(DomainException):
        z.derive({ x: 3.0 })
    with raises(DomainException):
        z.derive({ x: 0.0 })

### Power

def testPower():
    x = Variable()
    y = Variable()
    z = Power(x, y)
    result = z.derive({ x: 3.0, y: 2.5 })
    assert result.value == approx(15.588457268)
    assert result.partialWithRespectTo(x) == approx(12.990381056)
    assert result.partialWithRespectTo(y) == approx(17.125670716)
    result = z.derive({ x: 3.0, y: 0.0 })
    assert result.value == approx(1.0)
    assert result.partialWithRespectTo(x) == approx(0.0)
    assert result.partialWithRespectTo(y) == approx(1.0986122886)
    result = z.derive({ x: 3.0, y: -2.5 })
    assert result.value == approx(0.0641500299)
    assert result.partialWithRespectTo(x) == approx(-0.0534583582)
    assert result.partialWithRespectTo(y) == approx(0.0704760111)
    with raises(DomainException):
        z.derive({ x: 0.0, y: 2.5 })
    with raises(DomainException):
        z.derive({ x: 0.0, y: 0.0 })
    with raises(DomainException):
        z.derive({ x: 0.0, y: -2.5 })
    with raises(DomainException):
        z.derive({ x: -3.0, y: 2.5 })
    with raises(DomainException):
        z.derive({ x: -3.0, y: 0.0 })
    with raises(DomainException):
        z.derive({ x: -3.0, y: -2.5 })

def testPowerWithConstantBaseOne():
    y = Variable()
    z = Power(Constant(1), y)
    result = z.derive({ y: 3 })
    assert result.value == approx(1.0)
    assert result.partialWithRespectTo(y) == approx(0.0)
    result = z.derive({ y: 0 })
    assert result.value == approx(1.0)
    assert result.partialWithRespectTo(y) == approx(0.0)
    assert result.value == approx(1.0)
    result = z.derive({ y: -5 })
    assert result.partialWithRespectTo(y) == approx(0.0)

def testPowerWithConstantBaseZero():
    y = Variable()
    z = Power(Constant(0), y)
    with raises(DomainException):
        z.derive({ y: 3 })
    with raises(DomainException):
        z.derive({ y: 0 })
    with raises(DomainException):
        z.derive({ y: -5 })

def testPowerWithConstantBaseNegativeOne():
    y = Variable()
    z = Power(Constant(-1), y)
    with raises(DomainException):
        z.derive({ y: 3 })
    with raises(DomainException):
        z.derive({ y: 0 })
    with raises(DomainException):
        z.derive({ y: -5 })

def testPowerWithConstantExponentTwo():
    x = Variable()
    z = Power(x, Constant(2))
    result = z.derive({ x: 3 })
    assert result.value == approx(9.0)
    assert result.partialWithRespectTo(x) == approx(6.0)
    result = z.derive({ x: 0 })
    assert result.value == approx(0.0)
    assert result.partialWithRespectTo(x) == approx(0.0)
    result = z.derive({ x: -5 })
    assert result.value == approx(25.0)
    assert result.partialWithRespectTo(x) == approx(-10.0)

def testPowerWithConstantExponentOne():
    x = Variable()
    z = Power(x, Constant(1))
    result = z.derive({ x: 3 })
    assert result.value == approx(3.0)
    assert result.partialWithRespectTo(x) == approx(1.0)
    result = z.derive({ x: 0 })
    assert result.value == approx(0.0)
    assert result.partialWithRespectTo(x) == approx(1.0)
    result = z.derive({ x: -5 })
    assert result.value == approx(-5.0)
    assert result.partialWithRespectTo(x) == approx(1.0)

def testPowerWithConstantExponentZero():
    x = Variable()
    z = Power(x, Constant(0))
    result = z.derive({ x: 3 })
    assert result.value == approx(1.0)
    assert result.partialWithRespectTo(x) == approx(0.0)
    result = z.derive({ x: 0 })
    assert result.value == approx(1.0)
    assert result.partialWithRespectTo(x) == approx(0.0)
    result = z.derive({ x: -5 })
    assert result.value == approx(1.0)
    assert result.partialWithRespectTo(x) == approx(0.0)

def testPowerWithConstantExponentNegativeOne():
    x = Variable()
    z = Power(x, Constant(-1))
    result = z.derive({ x: 2 })
    assert result.value == approx(0.5)
    assert result.partialWithRespectTo(x) == approx(-0.25)
    with raises(DomainException):
        z.derive({ x: 0 })
    result = z.derive({ x: -5 })
    assert result.value == approx(-0.2)
    assert result.partialWithRespectTo(x) == approx(-0.04)

def testPowerWithConstantExponentNegativeTwo():
    x = Variable()
    z = Power(x, Constant(-2))
    result = z.derive({ x: 2 })
    assert result.value == approx(0.25)
    assert result.partialWithRespectTo(x) == approx(-0.25)
    with raises(DomainException):
        z.derive({ x: 0 })
    result = z.derive({ x: -5 })
    assert result.value == approx(0.04)
    assert result.partialWithRespectTo(x) == approx(0.016)

def testPowerWithExponentMadeFromAddingConstants():
    x = Variable()
    z = Power(x, Constant(1) + Constant(1))
    result = z.derive({ x: 3 })
    assert result.value == approx(9.0)
    assert result.partialWithRespectTo(x) == approx(6.0)
    result = z.derive({ x: 0 })
    assert result.value == approx(0.0)
    assert result.partialWithRespectTo(x) == approx(0.0)
    result = z.derive({ x: -5 })
    assert result.value == approx(25.0)
    assert result.partialWithRespectTo(x) == approx(-10.0)

### Polynomials

def testPolynomialOfOneVariable():
    x = Variable()
    z = x * x - Constant(6) * x + Constant(4)
    result = z.derive({ x: 2 })
    assert result.value == -4
    assert result.partialWithRespectTo(x) == -2

def testPolynomialOfTwoVariables():
    x = Variable()
    y = Variable()
    z = x * (x + y) - Constant(5) * y * y
    result = z.derive({ x: 2, y: 3 })
    assert result.value == -35
    assert result.partialWithRespectTo(x) == 7
    assert result.partialWithRespectTo(y) == -28

def testPolynomialOfThreeVariables():
    w = Variable()
    x = Variable()
    y = Variable()
    z = w * w + Constant(5) * w * x * x - w * x * y
    result = z.derive({ w: 2, x: 3, y: 4 })
    assert result.value == 70
    assert result.partialWithRespectTo(w) == 37
    assert result.partialWithRespectTo(x) == 52
    assert result.partialWithRespectTo(y) == -6

### Other

def testCompositeFunction():
    x = Variable()
    z = NaturalExponential(x ** Constant(2))
    result = z.derive({ x: 2 })
    assert result.value == approx(54.598150033)
    assert result.partialWithRespectTo(x) == approx(218.392600132)

def testIndeterminateForm():
    t = Variable()
    z = (Constant(2) * t) / t
    with raises(DomainException):
        z.derive({ t: 0 })

def testExpressionReuse():
    x = Variable()
    w = x ** Constant(2)
    z = (w + Constant(1)) / w
    result = z.derive({ x: 2 })
    assert result.value == approx(1.25)
    assert result.partialWithRespectTo(x) == approx(-0.25)
