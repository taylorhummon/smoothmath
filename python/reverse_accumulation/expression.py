import math

class ComputedPartials:
    def __init__(self):
        self._dict = {}

    def partialWithRespectTo(self, variable):
        return self._dict.get(variable, 0)

    def addSeed(self, variable, seed):
        self._dict[variable] = seed + self._dict.get(variable, 0)

class Expression:
    def __init__(self, value):
        self.value = value

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
        return Power(self, other)

    def evaluate(self):
        if self.value is None:
            self._evaluate()

    def derive(self):
        self.evaluate()
        computedPartials = ComputedPartials()
        self._derive(computedPartials, 1)
        return computedPartials

    # the _evaluate method should compute the value for an expression and set it as self.value
    def _evaluate(self):
        raise Exception("the evaluate() method should be overridden")

    def _derive(self, computedPartials, seed):
        raise Exception("the _derive() method should be overridden")

class NullaryExpression(Expression):
    def __init__(self, value):
        super().__init__(value)

class UnaryExpression(Expression):
    def __init__(self, expressionA):
        super().__init__(None)
        self.expressionA = expressionA

class BinaryExpression(Expression):
    def __init__(self, expressionA, expressionB):
        super().__init__(None)
        self.expressionA = expressionA
        self.expressionB = expressionB

class Constant(NullaryExpression):
    def __init__(self, value):
        super().__init__(value)

    def _evaluate(self):
        pass

    def _derive(self, computedPartials, seed):
        pass

class Variable(NullaryExpression):
    def __init__(self, value):
        super().__init__(value)

    def _evaluate(self):
        pass

    def _derive(self, computedPartials, seed):
        computedPartials.addSeed(self, seed)

class Negation(UnaryExpression):
    def __init__(self, expressionA):
        super().__init__(expressionA)

    def _evaluate(self):
        self.expressionA.evaluate()
        self.value = - self.expressionA.value

    def _derive(self, computedPartials, seed):
        # d(-u) = -du
        self.expressionA._derive(computedPartials, -seed)

class Reciprocal(UnaryExpression):
    def __init__(self, expressionA):
        super().__init__(expressionA)

    def _evaluate(self):
        self.expressionA.evaluate()
        if self.expressionA.value == 0:
            raise Exception("cannot divide by zero")
        self.value = 1 / self.expressionA.value

    def _derive(self, computedPartials, seed):
        # d(1 / u) = (-1 / u ** 2) * du
        self.expressionA._derive(computedPartials, - seed * (self.value ** 2))
        pass

class NaturalExp(UnaryExpression):
    def __init__(self, expressionA):
        super().__init__(expressionA)

    def _evaluate(self):
        self.expressionA.evaluate()
        self.value = math.e ** self.expressionA.value

    def _derive(self, computedPartials, seed):
        # d(e ** v) = e ** v * dv
        self.expressionA._derive(computedPartials, seed * self.value)

class NaturalLog(UnaryExpression):
    def __init__(self, expressionA):
        super().__init__(expressionA)

    def _evaluate(self):
        self.expressionA.evaluate()
        if self.expressionA.value <= 0:
            raise Exception("can only take the log of a positive number")
        self.value = math.log(self.expressionA.value)

    def _derive(self, computedPartials, seed):
        # d(ln(u)) = (1 / u) * du
        self.expressionA._derive(computedPartials, seed / self.expressionA.value)

class Sine(UnaryExpression):
    def __init__(self, expressionA):
        super().__init__(expressionA)

    def _evaluate(self):
        self.expressionA.evaluate()
        self.value = math.sin(self.expressionA.value)

    def _derive(self, computedPartials, seed):
        # d(sin(u)) = cos(u) * du
        self.expressionA._derive(computedPartials, math.cos(self.expressionA.value) * seed)

class Cosine(UnaryExpression):
    def __init__(self, expressionA):
        super().__init__(expressionA)

    def _evaluate(self):
        self.expressionA.evaluate()
        self.value = math.cos(self.expressionA.value)

    def _derive(self, computedPartials, seed):
        # d(cos(u)) = - sin(u) * du
        self.expressionA._derive(computedPartials, - math.sin(self.expressionA.value) * seed)

class Plus(BinaryExpression):
    def __init__(self, expressionA, expressionB):
        super().__init__(expressionA, expressionB)

    def _evaluate(self):
        self.expressionA.evaluate()
        self.expressionB.evaluate()
        self.value = self.expressionA.value + self.expressionB.value

    def _derive(self, computedPartials, seed):
        # d(u + v) = du + dv
        self.expressionA._derive(computedPartials, seed)
        self.expressionB._derive(computedPartials, seed)

class Minus(BinaryExpression):
    def __init__(self, expressionA, expressionB):
        super().__init__(expressionA, expressionB)

    def _evaluate(self):
        self.expressionA.evaluate()
        self.expressionB.evaluate()
        self.value = self.expressionA.value - self.expressionB.value

    def _derive(self, computedPartials, seed):
        # d(u - v) = du - dv
        self.expressionA._derive(computedPartials, seed)
        self.expressionB._derive(computedPartials, - seed)

class Multiply(BinaryExpression):
    def __init__(self, expressionA, expressionB):
        super().__init__(expressionA, expressionB)

    def _evaluate(self):
        self.expressionA.evaluate()
        self.expressionB.evaluate()
        self.value = self.expressionA.value * self.expressionB.value

    def _derive(self, computedPartials, seed):
        # d(u * v) = v * du + u * dv
        self.expressionA._derive(computedPartials, self.expressionB.value * seed)
        self.expressionB._derive(computedPartials, self.expressionA.value * seed)

class Divide(BinaryExpression):
    def __init__(self, expressionA, expressionB):
        super().__init__(expressionA, expressionB)

    def _evaluate(self):
        self.expressionA.evaluate()
        self.expressionB.evaluate()
        if self.expressionB.value == 0:
            raise Exception("cannot divide by zero")
        self.value = self.expressionA.value / self.expressionB.value

    def _derive(self, computedPartials, seed):
        # d(u / v) = (1 / v) * du - (u / v ^ 2) * dv
        self.expressionA._derive(
            computedPartials,
            seed / self.expressionB.value
        )
        self.expressionB._derive(
            computedPartials,
            - seed * self.expressionA.value / (self.expressionB.value ** 2)
        )

# When we have an integer in the exponent, we can support negative bases
class PowerWithIntegralExponent(BinaryExpression):
    def __init__(self, expressionA, expressionB):
        super().__init__(expressionA, expressionB)

    def _evaluate(self):
        self.expressionA.evaluate()
        self.expressionB.evaluate()
        if self.expressionA.value == 0 and self.expressionB.value <= 0:
            raise Exception("cannot have a base of zero unless the exponent is positive")
        self.value = self.expressionA.value ** self.expressionB.value

    def _derive(self, computedPartials, seed):
        # d(u ** c) = c * u ** (c - 1) * du
        self.expressionA._derive(
            computedPartials,
            seed * self.expressionB.value * (self.expressionA.value ** (self.expressionB.value - 1))
        )

class Power(BinaryExpression):
    def __init__(self, expressionA, expressionB):
        super().__init__(expressionA, expressionB)

    def _evaluate(self):
        self.expressionA.evaluate()
        self.expressionB.evaluate()
        if self.expressionA.value <= 0:
            raise Exception("must have a positive base for non-integral exponents")
        self.value = self.expressionA.value ** self.expressionB.value

    def _derive(self, computedPartials, seed):
        # d(u ** v) = v * u ** (v - 1) * du + ln(u) * u ** v * dv
        self.expressionA._derive(
            computedPartials,
            seed * self.expressionB.value * (self.expressionA.value ** (self.expressionB.value - 1))
        )
        self.expressionB._derive(
            computedPartials,
            seed * math.log(self.expressionA.value) * (self.expressionA.value ** self.expressionB.value)
        )

# Example: Finding the partials of z = x * (x + y) + 5 *  y * y at (x, y) = (2, 3)
x = Variable(2)
y = Variable(3)
c = Constant(5)
z = x * (x + y) + c * y * y
computedPartials = z.derive()
print("z =", z.value)                            # Output: z = 55
print("∂z/∂x =", computedPartials.partialWithRespectTo(x)) # Output: ∂z/∂x = 7
print("∂z/∂y =", computedPartials.partialWithRespectTo(y)) # Output: ∂z/∂y = 32
