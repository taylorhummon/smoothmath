from __future__ import annotations
from abc import ABC, abstractmethod
import math
from src.reverse_accumulation.custom_types import numeric, VariableValues
from src.reverse_accumulation.custom_exceptions import MathException
from src.reverse_accumulation.result import Result

# !!! update exception messages

class Expression(ABC):
    def __init__(
        self: Expression,
        lacksVariables: bool
    ) -> None:
        self._value : numeric | None
        self._value = None
        self.lacksVariables : bool
        self.lacksVariables = lacksVariables

    ## Evaluation ##

    def evaluate(
        self: Expression,
        variableValues: VariableValues
    ) -> numeric:
        try:
            return self._evaluateWithCache(variableValues)
        finally:
            self._resetEvaluationCache()

    def _evaluateWithCache(
        self: Expression,
        variableValues: VariableValues
    ) -> numeric:
        if self._value is None:
            self._value = self._evaluate(variableValues)
        return self._value

    @abstractmethod
    def _evaluate(
        self: Expression,
        variableValues: VariableValues
    ) -> numeric:
        raise Exception("concrete classes derived from Expression must implement _evaluate()")

    @abstractmethod
    def _resetEvaluationCache(
        self: Expression
    ) -> None:
        raise Exception("concrete classes derived from Expression must implement _resetEvaluationCache()")

    ## Derivation ##

    def derive(
        self: Expression,
        variableValues: VariableValues
    ) -> Result:
        try:
            result = Result()
            self._derive(variableValues, result, 1)
            return result
        finally:
            self._resetEvaluationCache()

    @abstractmethod
    def _derive(
        self: Expression,
        variableValues: VariableValues,
        result: Result,
        seed: numeric
    ) -> None:
        raise Exception("concrete classes derived from Expression must implement _derive()")

    ## Operations ##

    def __neg__(
        self: Expression
    ) -> Negation:
        return Negation(self)

    def __add__(
        self: Expression,
        other: Expression
    ) -> Plus:
        return Plus(self, other)

    def __sub__(
        self: Expression,
        other: Expression
    ) -> Minus:
        return Minus(self, other)

    def __mul__(
        self: Expression,
        other: Expression
    ) -> Multiply:
        return Multiply(self, other)

    def __truediv__(
        self: Expression,
        other: Expression
    ) -> Divide:
        return Divide(self, other)

    def __pow__(
        self: Expression,
        other: Expression
    ) -> Power:
        return Power(self, other)

### Nullary Expressions ###

class NullaryExpression(Expression):
    def __init__(
        self: NullaryExpression,
        lacksVariables: bool
    ) -> None:
        super().__init__(lacksVariables)

    def _resetEvaluationCache(
        self: NullaryExpression
    ) -> None:
        self._value = None

class Constant(NullaryExpression):
    def __init__(
        self: Constant,
        value: numeric
    ) -> None:
        super().__init__(lacksVariables = True)
        self._valueFromInit = value

    def _evaluate(
        self: Constant,
        variableValues: VariableValues
    ) -> numeric:
        return self._valueFromInit

    def _derive(
        self: Constant,
        variableValues: VariableValues,
        result: Result,
        seed: numeric
    ) -> None:
        pass

class Variable(NullaryExpression):
    def __init__(
        self: Variable
    ) -> None:
        super().__init__(lacksVariables = False)

    def _evaluate(
        self: Variable,
        variableValues: VariableValues
    ) -> numeric:
        value = variableValues.get(self, None)
        if value is None:
            raise Exception("variableValues missing a value for a variable")
        return value

    def _derive(
        self: Variable,
        variableValues: VariableValues,
        result: Result,
        seed: numeric
    ) -> None:
        result.addSeed(self, seed)

### Unary Expressions ###

class UnaryExpression(Expression):
    def __init__(
        self: UnaryExpression,
        a: Expression
    ) -> None:
        super().__init__(lacksVariables = a.lacksVariables)
        self.a = a

    def _resetEvaluationCache(
        self: UnaryExpression
    ) -> None:
        self._value = None
        self.a._resetEvaluationCache()

class Negation(UnaryExpression):
    def __init__(
        self: Negation,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Negation,
        variableValues: VariableValues
    ) -> numeric:
        aValue = self.a._evaluateWithCache(variableValues)
        return - aValue

    def _derive(
        self: Negation,
        variableValues: VariableValues,
        result: Result,
        seed: numeric
    ) -> None:
        # d(-u) = -du
        self.a._derive(variableValues, result, -seed)

class Reciprocal(UnaryExpression):
    def __init__(
        self: Reciprocal,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Reciprocal,
        variableValues: VariableValues
    ) -> numeric:
        aValue = self.a._evaluateWithCache(variableValues)
        if aValue == 0:
            raise MathException("1 / x at x = 0")
        return 1 / aValue

    def _derive(
        self: Reciprocal,
        variableValues: VariableValues,
        result: Result,
        seed: numeric
    ) -> None:
        selfValue = self._evaluateWithCache(variableValues)
        # d(1 / u) = (-1 / u ** 2) * du
        self.a._derive(variableValues, result, - seed * (selfValue ** 2))

class SquareRoot(UnaryExpression):
    def __init__(
        self: SquareRoot,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: SquareRoot,
        variableValues: VariableValues
    ) -> numeric:
        aValue = self.a._evaluateWithCache(variableValues)
        if aValue == 0:
            raise MathException("sqrt(x) at x = 0")
        elif aValue < 0:
            raise MathException("sqrt(x) for x < 0")
        return math.sqrt(aValue)

    def _derive(
        self: SquareRoot,
        variableValues: VariableValues,
        result: Result,
        seed: numeric
    ) -> None:
        selfValue = self._evaluateWithCache(variableValues)
        # d(sqrt(v)) = (1 / (2 sqrt(v))) * dv
        self.a._derive(variableValues, result, (1 / (2 * selfValue)) * seed)

class NaturalExponential(UnaryExpression):
    def __init__(
        self: NaturalExponential,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: NaturalExponential,
        variableValues: VariableValues
    ) -> numeric:
        aValue = self.a._evaluateWithCache(variableValues)
        return math.e ** aValue

    def _derive(
        self: NaturalExponential,
        variableValues: VariableValues,
        result: Result,
        seed: numeric
    ) -> None:
        selfValue = self._evaluateWithCache(variableValues)
        # d(e ** v) = e ** v * dv
        self.a._derive(variableValues, result, seed * selfValue)

class NaturalLogarithm(UnaryExpression):
    def __init__(
        self: NaturalLogarithm,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: NaturalLogarithm,
        variableValues: VariableValues
    ) -> numeric:
        aValue = self.a._evaluateWithCache(variableValues)
        if aValue == 0: #!!! consider DRYing
            raise MathException("ln(x) at x = 0")
        elif aValue < 0:
            raise MathException("ln(x) for x < 0")
        return math.log(aValue)

    def _derive(
        self: NaturalLogarithm,
        variableValues: VariableValues,
        result: Result,
        seed: numeric
    ) -> None:
        aValue = self.a._evaluateWithCache(variableValues)
        if aValue == 0:
            raise MathException("ln(x) at x = 0")
        elif aValue < 0:
            raise MathException("ln(x) for x < 0")
        # d(ln(u)) = (1 / u) * du
        self.a._derive(variableValues, result, seed / aValue)

class Sine(UnaryExpression):
    def __init__(
        self: Sine,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Sine,
        variableValues: VariableValues
    ) -> numeric:
        aValue = self.a._evaluateWithCache(variableValues)
        return math.sin(aValue)

    def _derive(
        self: Sine,
        variableValues: VariableValues,
        result: Result,
        seed: numeric
    ) -> None:
        aValue = self.a._evaluateWithCache(variableValues)
        # d(sin(u)) = cos(u) * du
        self.a._derive(variableValues, result, math.cos(aValue) * seed)

class Cosine(UnaryExpression):
    def __init__(
        self: Cosine,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _evaluate(
        self: Cosine,
        variableValues: VariableValues
    ) -> numeric:
        aValue = self.a._evaluateWithCache(variableValues)
        return math.cos(aValue)

    def _derive(
        self: Cosine,
        variableValues: VariableValues,
        result: Result,
        seed: numeric
    ) -> None:
        aValue = self.a._evaluateWithCache(variableValues)
        # d(cos(u)) = - sin(u) * du
        self.a._derive(variableValues, result, - math.sin(aValue) * seed)

### Binary Expressions ###

class BinaryExpression(Expression):
    def __init__(
        self: BinaryExpression,
        a: Expression,
        b: Expression,
    ) -> None:
        super().__init__(lacksVariables = a.lacksVariables and b.lacksVariables)
        self.a = a
        self.b = b

    def _resetEvaluationCache(
        self: BinaryExpression
    ) -> None:
        self._value = None
        self.a._resetEvaluationCache()
        self.b._resetEvaluationCache()

class Plus(BinaryExpression):
    def __init__(
        self: Plus,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Plus,
        variableValues: VariableValues
    ) -> numeric:
        aValue = self.a._evaluateWithCache(variableValues)
        bValue = self.b._evaluateWithCache(variableValues)
        return aValue + bValue

    def _derive(
        self: Plus,
        variableValues: VariableValues,
        result: Result,
        seed: numeric
    ) -> None:
        # d(u + v) = du + dv
        self.a._derive(variableValues, result, seed)
        self.b._derive(variableValues, result, seed)

class Minus(BinaryExpression):
    def __init__(
        self: Minus,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Minus,
        variableValues: VariableValues
    ) -> numeric:
        aValue = self.a._evaluateWithCache(variableValues)
        bValue = self.b._evaluateWithCache(variableValues)
        return aValue - bValue

    def _derive(
        self: Minus,
        variableValues: VariableValues,
        result: Result,
        seed: numeric
    ) -> None:
        # d(u - v) = du - dv
        self.a._derive(variableValues, result, seed)
        self.b._derive(variableValues, result, - seed)

class Multiply(BinaryExpression):
    def __init__(
        self: Multiply,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Multiply,
        variableValues: VariableValues
    ) -> numeric:
        aValue = self.a._evaluateWithCache(variableValues)
        bValue = self.b._evaluateWithCache(variableValues)
        return aValue * bValue

    def _derive(
        self: Multiply,
        variableValues: VariableValues,
        result: Result,
        seed: numeric
    ) -> None:
        aValue = self.a._evaluateWithCache(variableValues)
        bValue = self.b._evaluateWithCache(variableValues)
        # d(u * v) = v * du + u * dv
        self.a._derive(variableValues, result, bValue * seed)
        self.b._derive(variableValues, result, aValue * seed)

class Divide(BinaryExpression):
    def __init__(
        self: Divide,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _evaluate(
        self: Divide,
        variableValues: VariableValues
    ) -> numeric:
        aValue = self.a._evaluateWithCache(variableValues)
        bValue = self.b._evaluateWithCache(variableValues)
        if bValue == 0: # !!! consider DRYing
            if aValue == 0:
                raise MathException("x / y at (x, y) = (0, 0)")
            else:
                raise MathException("x / y with x != 0 and y = 0")
        return aValue / bValue

    def _derive(
        self: Divide,
        variableValues: VariableValues,
        result: Result,
        seed: numeric
    ) -> None:
        aValue = self.a._evaluateWithCache(variableValues)
        bValue = self.b._evaluateWithCache(variableValues)
        if bValue == 0:
            if aValue == 0:
                raise MathException("x / y at (x, y) = (0, 0)")
            else:
                raise MathException("x / y with x != 0 and y = 0")
        # d(u / v) = (1 / v) * du - (u / v ^ 2) * dv
        self.a._derive(variableValues, result, seed / bValue)
        self.b._derive(variableValues, result, - seed * aValue / (bValue ** 2))

class Power(BinaryExpression):
    def __init__(
        self: Power,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    # For a power a ** b, there are two over-arching cases we work with:
    # (I) the exponent, b, can be determined to be a constant integer
    #     e.g. a ** 2, a ** 3, or a ** (-1)
    # (II) otherwise
    #     e.g. e ** b, or 3 ** b, a ** b,
    # In case (I), we support negative bases. In case (II), we only support positive bases.

    def _evaluate(
        self: Power,
        variableValues: VariableValues
    ) -> numeric:
        aValue = self.a._evaluateWithCache(variableValues)
        bValue = self.b._evaluateWithCache(variableValues)
        if bValue.is_integer():
            if aValue == 0 and bValue <= 0:
                raise MathException("cannot have a base of zero unless the exponent is positive")
            return aValue ** bValue
        else: # bValue is not an integer
            if aValue <= 0:
                raise MathException("must have a positive base for non-integral exponents")
            return aValue ** bValue

    def _derive(
        self: Power,
        variableValues: VariableValues,
        result: Result,
        seed: numeric
    ) -> None:
        aValue = self.a._evaluateWithCache(variableValues)
        bValue = self.b._evaluateWithCache(variableValues)
        selfValue = self._evaluateWithCache(variableValues)
        if self.b.lacksVariables and bValue.is_integer():
            if aValue == 0 and bValue <= 0:
                raise MathException("cannot have a base of zero unless the exponent is positive")
            # d(u ** c) = c * u ** (c - 1) * du
            self.a._derive(variableValues, result, seed * bValue * (aValue ** (bValue - 1)))
        else: # bValue is not an integer
            # d(u ** v) = v * u ** (v - 1) * du + ln(u) * u ** v * dv
            self.a._derive(variableValues, result, seed * bValue * (aValue ** (bValue - 1)))
            self.b._derive(variableValues, result, seed * math.log(aValue) * selfValue)
