import math
from abc import ABC, abstractmethod
from src.forward_accumulation.value_and_partial import ValueAndPartial

# !!! should I be worried about expressions like y / (x - x) ?
# !!! do i want to add type annotations?
# !!! how do I want to handle compound constant expressions?
# !!! how hard would this be to change from calculating partials to calculating the differential?
# !!! can we do this work iteratively instead of recursively?

class Expression(ABC):
    def evaluateAndDerive(self, variable):
        if isinstance(variable, Variable):
            return self._evaluateAndDerive(variable)
        else:
            raise Exception("can only differentiate with respect to a Variable")

    @abstractmethod
    def _evaluateAndDerive(self, variable):
        raise Exception("concrete classes derived from Expression must implement _evaluateAndDerive()")

    def __neg__(self):
        return Negation(self)

    def __add__(self, other):
        return Plus(self, other)

    def __sub__(self, other):
        return Minus(self, other)

    def __mul__(self, other):
        return Multiply(self, other)

    def __truediv__(self, other):
        return Divide(self, other)

    def __pow__(self, other):
        # !!! what if other isnt a Constant but evaluates to a constant?
        if isinstance(other, Constant) and isinstance(other.value, int):
            return PowerWithIntegralExponent(self, other)
        else:
            return Power(self, other)

class Constant(Expression):
    def __init__(self, value):
        self.value = value

    def _evaluateAndDerive(self, variable):
        return ValueAndPartial(self.value, 0)

class Variable(Expression):
    def __init__(self, value):
        self.value = value

    def _evaluateAndDerive(self, variable):
        partial = 1 if self == variable else 0
        return ValueAndPartial(self.value, partial)

class Negation(Expression):
    def __init__(self, expressionA):
        self.expressionA = expressionA

    def _evaluateAndDerive(self, variable):
        valueA, partialA = self.expressionA._evaluateAndDerive(variable).toList()
        # d(-u) = -du
        return ValueAndPartial(-valueA, -partialA)

class Reciprocal(Expression):
    def __init__(self, expressionA):
        self.expressionA = expressionA

    def _evaluateAndDerive(self, variable):
        valueA, partialA = self.expressionA._evaluateAndDerive(variable).toList()
        if valueA == 0:
            raise Exception("cannot divide by zero")
        value = 1 / valueA
        # d(1 / u) = (-1 / u ** 2) * du
        partial = - partialA * (value ** 2)
        return ValueAndPartial(value, partial)

class NaturalExponential(Expression):
    def __init__(self, expressionA):
        self.expressionA = expressionA

    def _evaluateAndDerive(self, variable):
        valueA, partialA = self.expressionA._evaluateAndDerive(variable).toList()
        value = math.e ** valueA
        # d(e ** v) = e ** v * dv
        partial = value * partialA
        return ValueAndPartial(value, partial)

class NaturalLogarithm(Expression):
    def __init__(self, expressionA):
        self.expressionA = expressionA

    def _evaluateAndDerive(self, variable):
        valueA, partialA = self.expressionA._evaluateAndDerive(variable).toList()
        if valueA <= 0:
            raise Exception("can only take the log of a positive number")
        # d(ln(u)) = (1 / u) * du
        return ValueAndPartial(
            math.log(valueA),
            partialA / valueA
        )

class Sine(Expression):
    def __init__(self, expressionA):
        self.expressionA = expressionA

    def _evaluateAndDerive(self, variable):
        valueA, partialA = self.expressionA._evaluateAndDerive(variable).toList()
        # d(sin(u)) = cos(u) * du
        return ValueAndPartial(
            math.sin(valueA),
            math.cos(valueA) * partialA
        )

class Cosine(Expression):
    def __init__(self, expressionA):
        self.expressionA = expressionA

    def _evaluateAndDerive(self, variable):
        valueA, partialA = self.expressionA._evaluateAndDerive(variable).toList()
        # d(cos(u)) = - sin(u) * du
        return ValueAndPartial(
            math.cos(valueA),
            - math.sin(valueA) * partialA
        )

class Plus(Expression):
    def __init__(self, expressionA, expressionB):
        self.expressionA = expressionA
        self.expressionB = expressionB

    def _evaluateAndDerive(self, variable):
        valueA, partialA = self.expressionA._evaluateAndDerive(variable).toList()
        valueB, partialB = self.expressionB._evaluateAndDerive(variable).toList()
        # d(u + v) = du + dv
        return ValueAndPartial(
            valueA + valueB,
            partialA + partialB
        )

class Minus(Expression):
    def __init__(self, expressionA, expressionB):
        self.expressionA = expressionA
        self.expressionB = expressionB

    def _evaluateAndDerive(self, variable):
        valueA, partialA = self.expressionA._evaluateAndDerive(variable).toList()
        valueB, partialB = self.expressionB._evaluateAndDerive(variable).toList()
        # d(u - v) = du - dv
        return ValueAndPartial(
            valueA - valueB,
            partialA - partialB
        )

class Multiply(Expression):
    def __init__(self, expressionA, expressionB):
        self.expressionA = expressionA
        self.expressionB = expressionB

    def _evaluateAndDerive(self, variable):
        valueA, partialA = self.expressionA._evaluateAndDerive(variable).toList()
        valueB, partialB = self.expressionB._evaluateAndDerive(variable).toList()
        value = valueA * valueB
        # d(u * v) = v * du + u * dv
        partial = valueB * partialA + valueA * partialB
        return ValueAndPartial(value, partial)

class Divide(Expression):
    def __init__(self, expressionA, expressionB):
        self.expressionA = expressionA
        self.expressionB = expressionB

    def _evaluateAndDerive(self, variable):
        valueA, partialA = self.expressionA._evaluateAndDerive(variable).toList()
        valueB, partialB = self.expressionB._evaluateAndDerive(variable).toList()
        if valueB == 0:
            raise Exception("cannot divide by zero")
        value = valueA / valueB
        # d(u / v) = (1 / v) * du - (u / v ** 2) * dv
        partial = (valueB * partialA - valueA * partialB) / valueB ** 2
        return ValueAndPartial(value, partial)

# When we have an integer in the exponent, we can support negative bases
class PowerWithIntegralExponent(Expression):
    def __init__(self, expressionA, expressionB):
        # !!! we expect expressionB to be a integral Constant
        self.expressionA = expressionA
        self.expressionB = expressionB

    def _evaluateAndDerive(self, variable):
        valueA, partialA = self.expressionA._evaluateAndDerive(variable).toList()
        valueB = self.expressionB.value
        if valueA == 0 and valueB <= 0:
            raise Exception("cannot have a base of zero unless the exponent is positive")
        value = valueA ** valueB
        # d(u ** c) = c * u ** (c - 1) * du
        partial = (valueB * valueA ** (valueB - 1)) * partialA
        return ValueAndPartial(value, partial)

class Power(Expression):
    def __init__(self, expressionA, expressionB):
        self.expressionA = expressionA
        self.expressionB = expressionB

    def _evaluateAndDerive(self, variable):
        valueA, partialA = self.expressionA._evaluateAndDerive(variable).toList()
        valueB, partialB = self.expressionB._evaluateAndDerive(variable).toList()
        if valueA <= 0:
            raise Exception("must have a positive base for non-integral exponents")
        value = valueA ** valueB
        # d(u ** v) = v * u ** (v - 1) * du + ln(u) * u ** v * dv
        partial = (
            (valueB * (valueA ** (valueB - 1))) * partialA +
            math.log(valueA) * (valueA ** valueB) * partialB
        )
        return ValueAndPartial(value, partial)
