from pytest import approx, raises
import math
from src.reverse_accumulation.custom_exceptions import ArithmeticException
from src.reverse_accumulation.expression import *

### Constant

def testConstantEvaluation():
    c = Constant(7)
    assert c.evaluate() == 7

def testConstantDerivation():
    c = Constant(7)
    computedPartials = c.derive()
    x = Variable(2)
    assert computedPartials.partialWithRespectTo(x) == 0

### Variable

def testVariableEvaluation():
    x = Variable(2)
    assert x.evaluate() == 2

def testVariableDerivation():
    x = Variable(2)
    computedPartials = x.derive()
    assert computedPartials.partialWithRespectTo(x) == 1
    y = Variable(3)
    assert computedPartials.partialWithRespectTo(y) == 0

### Negation

def testNegationEvaluation():
    x = Variable(2)
    z = Negation(x)
    assert z.evaluate() == -2

def testNegationDerivation():
    x = Variable(2)
    z = Negation(x)
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(x) == -1

# ### Reciprocal

def testReciprocalEvalutaion():
    x = Variable(2)
    z = Reciprocal(x)
    assert z.evaluate() == approx(0.5)

def testReciprocalDerivation():
    x = Variable(2)
    z = Reciprocal(x)
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(x) == approx(-0.25)

def testReciprocalEvaluationAtZero():
    x = Variable(0)
    z = Reciprocal(x)
    with raises(ArithmeticException):
        z.evaluate()

def testReciprocalDerivationAtZero():
    x = Variable(0)
    z = Reciprocal(x)
    with raises(ArithmeticException):
        z.derive()

### Natural Exponential

def testNaturalExponentialEvaluationAtZero():
    x = Variable(0)
    z = NaturalExponential(x)
    assert z.evaluate() == approx(1.0)

def testNaturalExponentialDerivationAtZero():
    x = Variable(0)
    z = NaturalExponential(x)
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(x) == approx(1.0)

def testNaturalExponentialEvaluationAtOne():
    x = Variable(1)
    z = NaturalExponential(x)
    assert z.evaluate() == approx(math.e)

def testNaturalExponentialDerivationAtOne():
    x = Variable(1)
    z = NaturalExponential(x)
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(x) == approx(math.e)

### Natural Logarithm

def testNaturalLogarithmEvaluationAtOne():
    x = Variable(1)
    z = NaturalLogarithm(x)
    assert z.evaluate() == approx(0.0)

def testNaturalLogarithmDerivationAtOne():
    x = Variable(1)
    z = NaturalLogarithm(x)
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(x) == approx(1.0)

def testNaturalLogarithmEvaluationAtE():
    x = Variable(math.e)
    z = NaturalLogarithm(x)
    assert z.evaluate() == approx(1.0)

def testNaturalLogarithmDerivationAtE():
    x = Variable(math.e)
    z = NaturalLogarithm(x)
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(x) == approx(1.0 / math.e)

def testNaturalLogarithmEvaluationAtZero():
    x = Variable(0.0)
    z = NaturalLogarithm(x)
    with raises(ArithmeticException):
        z.evaluate()

def testNaturalLogarithmDerivationAtZero():
    x = Variable(0.0)
    z = NaturalLogarithm(x)
    with raises(ArithmeticException):
        z.derive()

def testNaturalLogarithmEvaluationAtNegative():
    x = Variable(-3.0)
    z = NaturalLogarithm(x)
    with raises(ArithmeticException):
        z.evaluate()

def testNaturalLogarithmDerivationAtNegative():
    x = Variable(-3.0)
    z = NaturalLogarithm(x)
    with raises(ArithmeticException):
        z.derive()

### Sine

def testSineEvaluationAtZero():
    theta = Variable(0.0)
    z = Sine(theta)
    assert z.evaluate() == approx(0.0)

def testSineDerivationAtZero():
    theta = Variable(0.0)
    z = Sine(theta)
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(theta) == approx(1.0)

def testSineEvaluationAtOneQuarterTurn():
    theta = Variable(math.pi / 2)
    z = Sine(theta)
    assert z.evaluate() == approx(1.0)

def testSineDerivationAtOneQuarterTurn():
    theta = Variable(math.pi / 2)
    z = Sine(theta)
    assert z.evaluate() == approx(1.0)

### Cosine

def testCosineEvaluationAtZero():
    theta = Variable(0.0)
    z = Cosine(theta)
    assert z.evaluate() == approx(1.0)

def testCosineDerivationAtZero():
    theta = Variable(0.0)
    z = Cosine(theta)
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(theta) == approx(0.0)

def testCosineEvaluationAtOneQuarterTurn():
    theta = Variable(math.pi / 2)
    z = Cosine(theta)
    assert z.evaluate() == approx(0.0)

def testCosineDerivationAtOneQuarterTurn():
    theta = Variable(math.pi / 2)
    z = Cosine(theta)
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(theta) == approx(-1.0)

### Plus

def testPlusEvaluation():
    x = Variable(2)
    y = Variable(3)
    z = Plus(x, y)
    assert z.evaluate() == approx(5.0)

def testPlusDerivation():
    x = Variable(2)
    y = Variable(3)
    z = Plus(x, y)
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(x) == approx(1.0)
    assert computedPartials.partialWithRespectTo(y) == approx(1.0)

### Minus

def testMinusEvaluation():
    x = Variable(2)
    y = Variable(3)
    z = Minus(x, y)
    assert z.evaluate() == approx(-1.0)

def testMinusDerivation():
    x = Variable(2)
    y = Variable(3)
    z = Minus(x, y)
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(x) == approx(1.0)
    assert computedPartials.partialWithRespectTo(y) == approx(-1.0)

### Multiply

def testMultiplyEvaluation():
    x = Variable(2)
    y = Variable(3)
    z = Multiply(x, y)
    assert z.evaluate() == approx(6.0)

def testMultiplyDerivation():
    x = Variable(2)
    y = Variable(3)
    z = Multiply(x, y)
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(x) == approx(3.0)
    assert computedPartials.partialWithRespectTo(y) == approx(2.0)

### Divide

def testDivideEvaluation():
    x = Variable(5)
    y = Variable(2)
    z = Divide(x, y)
    assert z.evaluate() == approx(2.5)

def testDivideDerivation():
    x = Variable(5)
    y = Variable(2)
    z = Divide(x, y)
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(x) == approx(0.5)
    assert computedPartials.partialWithRespectTo(y) == approx(-1.25)

def testDivideEvaluationAtZero():
    x = Variable(5)
    y = Variable(0)
    z = Divide(x, y)
    with raises(ArithmeticException):
        z.evaluate()

def testDivideDerivationAtZero():
    x = Variable(5)
    y = Variable(0)
    z = Divide(x, y)
    with raises(ArithmeticException):
        z.derive()

### PowerWithIntegralExponent

def testPowerWithIntegralExponentEvaluation():
    x = Variable(3)
    c = Constant(2)
    z = PowerWithIntegralExponent(x, c)
    assert z.evaluate() == approx(9.0)

def testPowerWithIntegralExponentDerivation():
    x = Variable(3)
    c = Constant(2)
    z = PowerWithIntegralExponent(x, c)
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(x) == approx(6.0)

def testPowerWithIntegralExponentAndNegativeBaseEvaluation():
    x = Variable(-5)
    c = Constant(2)
    z = PowerWithIntegralExponent(x, c)
    assert z.evaluate() == approx(25.0)

def testPowerWithIntegralExponentAndNegativeBaseDerivation():
    x = Variable(-5)
    c = Constant(2)
    z = PowerWithIntegralExponent(x, c)
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(x) == approx(-10.0)

def testPowerWithIntegralExponentAndZeroBaseEvaluation():
    x = Variable(0)
    c = Constant(2)
    z = PowerWithIntegralExponent(x, c)
    assert z.evaluate() == approx(0.0)

def testPowerWithIntegralExponentAndZeroBaseDerivation():
    x = Variable(0)
    c = Constant(2)
    z = PowerWithIntegralExponent(x, c)
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(x) == approx(0.0)

def testPowerWithNegativeIntegralExponentEvaluation():
    x = Variable(2)
    c = Constant(-2)
    z = PowerWithIntegralExponent(x, c)
    assert z.evaluate() == approx(0.25)

def testPowerWithNegativeIntegralExponentDerivation():
    x = Variable(2)
    c = Constant(-2)
    z = PowerWithIntegralExponent(x, c)
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(x) == approx(-0.25)

def testPowerWithNegativeIntegralExponentAndNegativeBaseEvaluation():
    x = Variable(-2)
    c = Constant(-2)
    z = PowerWithIntegralExponent(x, c)
    assert z.evaluate() == approx(0.25)

def testPowerWithNegativeIntegralExponentAndNegativeBaseDerivation():
    x = Variable(-2)
    c = Constant(-2)
    z = PowerWithIntegralExponent(x, c)
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(x) == approx(0.25)

def testPowerWithNegativeIntegralExponentAndZeroBaseEvaluation():
    x = Variable(0)
    c = Constant(-2)
    z = PowerWithIntegralExponent(x, c)
    with raises(ArithmeticException):
        z.evaluate()

def testPowerWithNegativeIntegralExponentAndZeroBaseDerivation():
    x = Variable(0)
    c = Constant(-2)
    z = PowerWithIntegralExponent(x, c)
    with raises(ArithmeticException):
        z.derive()

def testIllFormedPowerWithIntegralExponentEvaluation():
    x = Variable(-2)
    c = Constant(3.5) # we're only supposed to put integers in the exponent
    z = PowerWithIntegralExponent(x, c)
    with raises(Exception):
        z.evaluate()

def testIllFormedPowerWithIntegralExponentDeriation():
    x = Variable(-2)
    c = Constant(3.5) # we're only supposed to put integers in the exponent
    z = PowerWithIntegralExponent(x, c)
    with raises(Exception):
        z.evaluate()

### Power

def testPowerEvaluation():
    x = Variable(3.0)
    y = Variable(2.5)
    z = Power(x, y)
    assert z.evaluate() == approx(15.588457268)

def testPowerDerivation():
    x = Variable(3.0)
    y = Variable(2.5)
    z = Power(x, y)
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(x) == approx(12.990381056)
    assert computedPartials.partialWithRespectTo(y) == approx(17.125670716)

def testPowerWithNegativeBaseEvaluation():
    x = Variable(-3.0)
    y = Variable(2.5)
    z = Power(x, y)
    with raises(ArithmeticException):
        z.evaluate()

def testPowerWithNegativeBaseDerivation():
    x = Variable(-3.0)
    y = Variable(2.5)
    z = Power(x, y)
    with raises(ArithmeticException):
        z.derive()

def testPowerWithZeroBaseEvaluation():
    x = Variable(0.0)
    y = Variable(2.5)
    z = Power(x, y)
    with raises(ArithmeticException):
        z.evaluate()

def testPowerWithZeroBaseDerivation():
    x = Variable(0.0)
    y = Variable(2.5)
    z = Power(x, y)
    with raises(ArithmeticException):
        z.derive()

def testPowerWithNegativeExponentEvaluation():
    x = Variable(3.0)
    y = Variable(-2.5)
    z = Power(x, y)
    assert z.evaluate() == approx(0.0641500299)

def testPowerWithNegativeExponentDerivation():
    x = Variable(3.0)
    y = Variable(-2.5)
    z = Power(x, y)
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(x) == approx(-0.0534583582)
    assert computedPartials.partialWithRespectTo(y) == approx(0.0704760111)

def testPowerWithZeroExponentEvaluation():
    x = Variable(3.0)
    y = Variable(0.0)
    z = Power(x, y)
    assert z.evaluate() == approx(1.0)

def testPowerWithZeroExponentDerivation():
    x = Variable(3.0)
    y = Variable(0.0)
    z = Power(x, y)
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(x) == approx(0.0)
    assert computedPartials.partialWithRespectTo(y) == approx(1.0986122886)

def testPowerWithZeroBaseAndZeroExponentEvaluation():
    x = Variable(0.0)
    y = Variable(0.0)
    z = Power(x, y)
    with raises(ArithmeticException):
        z.evaluate()

def testPowerWithZeroBaseAndZeroExponentDerivation():
    x = Variable(0.0)
    y = Variable(0.0)
    z = Power(x, y)
    with raises(ArithmeticException):
        z.derive()

### Polynomials

def testPolynomialOfOneVariable():
    x = Variable(2)
    z = x * x - Constant(6) * x + Constant(4)
    assert z.evaluate() == -4
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(x) == -2

def testPolynomialOfTwoVariables():
    x = Variable(2)
    y = Variable(3)
    z = x * (x + y) - Constant(5) * y * y
    assert z.evaluate() == -35
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(x) == 7
    assert computedPartials.partialWithRespectTo(y) == -28

def testPolynomialOfThreeVariables():
    w = Variable(2)
    x = Variable(3)
    y = Variable(4)
    z = w * w + Constant(5) * w * x * x - w * x * y
    assert z.evaluate() == 70
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(w) == 37
    assert computedPartials.partialWithRespectTo(x) == 52
    assert computedPartials.partialWithRespectTo(y) == -6

### Other

def testCompositeFunctionEvaluation():
    x = Variable(2)
    z = NaturalExponential(x ** Constant(2))
    assert z.evaluate() == approx(54.598150033)

def testCompositeFunctionDerivation():
    x = Variable(2)
    z = NaturalExponential(x ** Constant(2))
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(x) == approx(218.392600132)

def testExpressionReuseEvaluation():
    x = Variable(2)
    w = x ** Constant(2)
    z = (w + Constant(1)) / w
    assert z.evaluate() == approx(1.25)

def testExpressionReuseDerivation():
    x = Variable(2)
    w = x ** Constant(2)
    z = (w + Constant(1)) / w
    computedPartials = z.derive()
    assert computedPartials.partialWithRespectTo(x) == approx(-0.25)
