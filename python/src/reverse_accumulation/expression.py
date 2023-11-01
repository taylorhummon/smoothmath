from __future__ import annotations
from abc import ABC, abstractmethod
import math
from src.reverse_accumulation.custom_types import numeric, VariableValues
from src.reverse_accumulation.custom_exceptions import DomainException
from src.reverse_accumulation.result import Result, InternalResult

class Expression(ABC):
    def __init__(
        self: Expression,
        lacksVariables: bool
    ) -> None:
        self.lacksVariables : bool
        self.lacksVariables = lacksVariables
        self._value : numeric | None
        self._value = None

    ## Evaluation ##

    def evaluate(
        self: Expression,
        variableValues: VariableValues
    ) -> numeric:
        try:
            return self._evaluateUsingCache(variableValues)
        finally:
            self._resetEvaluationCache()

    def _evaluateUsingCache(
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
            result = InternalResult()
            self._derive(result, variableValues, 1)
            return result.toResult()
        finally:
            self._resetEvaluationCache()

    @abstractmethod
    def _derive(
        self: Expression,
        result: InternalResult,
        variableValues: VariableValues,
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
        result: InternalResult,
        variableValues: VariableValues,
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
            raise Exception("variableValues is missing a value for a variable")
        return value

    def _derive(
        self: Variable,
        result: InternalResult,
        variableValues: VariableValues,
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
        aValue = self.a._evaluateUsingCache(variableValues)
        return - aValue

    def _derive(
        self: Negation,
        result: InternalResult,
        variableValues: VariableValues,
        seed: numeric
    ) -> None:
        # d(-a) = -da
        self.a._derive(result, variableValues, -seed)

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
        aValue = self.a._evaluateUsingCache(variableValues)
        self._ensureValueIsInDomain(aValue)
        return 1 / aValue

    def _derive(
        self: Reciprocal,
        result: InternalResult,
        variableValues: VariableValues,
        seed: numeric
    ) -> None:
        aValue = self.a._evaluateUsingCache(variableValues)
        self._ensureValueIsInDomain(aValue)
        selfValue = self._evaluateUsingCache(variableValues)
        # d(1 / a) = - (1 / a ** 2) * da
        self.a._derive(result, variableValues, - seed * (selfValue ** 2))

    def _ensureValueIsInDomain(
        self: Reciprocal,
        aValue: numeric
    ) -> None:
        if aValue == 0:
            raise DomainException("1 / x blows up around x = 0")

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
        aValue = self.a._evaluateUsingCache(variableValues)
        self._ensureValueIsInDomain(aValue)
        return math.sqrt(aValue)

    def _derive(
        self: SquareRoot,
        result: InternalResult,
        variableValues: VariableValues,
        seed: numeric
    ) -> None:
        aValue = self.a._evaluateUsingCache(variableValues)
        self._ensureValueIsInDomain(aValue)
        selfValue = self._evaluateUsingCache(variableValues)
        # d(sqrt(a)) = (1 / (2 sqrt(a))) * da
        self.a._derive(result, variableValues, seed / (2 * selfValue))

    def _ensureValueIsInDomain(
        self: SquareRoot,
        aValue: numeric
    ) -> None:
        if aValue == 0:
            raise DomainException("sqrt(x) is not smooth around x = 0")
        elif aValue < 0:
            raise DomainException("sqrt(x) is undefined for x < 0")

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
        aValue = self.a._evaluateUsingCache(variableValues)
        return math.e ** aValue

    def _derive(
        self: NaturalExponential,
        result: InternalResult,
        variableValues: VariableValues,
        seed: numeric
    ) -> None:
        selfValue = self._evaluateUsingCache(variableValues)
        # d(e ** a) = e ** a * da
        self.a._derive(result, variableValues, seed * selfValue)

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
        aValue = self.a._evaluateUsingCache(variableValues)
        self._ensureValueIsInDomain(aValue)
        return math.log(aValue)

    def _derive(
        self: NaturalLogarithm,
        result: InternalResult,
        variableValues: VariableValues,
        seed: numeric
    ) -> None:
        aValue = self.a._evaluateUsingCache(variableValues)
        self._ensureValueIsInDomain(aValue)
        # d(ln(a)) = (1 / a) * da
        self.a._derive(result, variableValues, seed / aValue)

    def _ensureValueIsInDomain(
        self: NaturalLogarithm,
        aValue: numeric
    ) -> None:
        if aValue == 0:
            raise DomainException("ln(x) blows up around x = 0")
        elif aValue < 0:
            raise DomainException("ln(x) is undefined for x < 0")

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
        aValue = self.a._evaluateUsingCache(variableValues)
        return math.sin(aValue)

    def _derive(
        self: Sine,
        result: InternalResult,
        variableValues: VariableValues,
        seed: numeric
    ) -> None:
        aValue = self.a._evaluateUsingCache(variableValues)
        # d(sin(a)) = cos(a) * da
        self.a._derive(result, variableValues, seed * math.cos(aValue))

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
        aValue = self.a._evaluateUsingCache(variableValues)
        return math.cos(aValue)

    def _derive(
        self: Cosine,
        result: InternalResult,
        variableValues: VariableValues,
        seed: numeric
    ) -> None:
        aValue = self.a._evaluateUsingCache(variableValues)
        # d(cos(a)) = - sin(a) * da
        self.a._derive(result, variableValues, - seed * math.sin(aValue))

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
        aValue = self.a._evaluateUsingCache(variableValues)
        bValue = self.b._evaluateUsingCache(variableValues)
        return aValue + bValue

    def _derive(
        self: Plus,
        result: InternalResult,
        variableValues: VariableValues,
        seed: numeric
    ) -> None:
        # d(a + b) = da + db
        self.a._derive(result, variableValues, seed)
        self.b._derive(result, variableValues, seed)

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
        aValue = self.a._evaluateUsingCache(variableValues)
        bValue = self.b._evaluateUsingCache(variableValues)
        return aValue - bValue

    def _derive(
        self: Minus,
        result: InternalResult,
        variableValues: VariableValues,
        seed: numeric
    ) -> None:
        # d(a - b) = da - db
        self.a._derive(result, variableValues, seed)
        self.b._derive(result, variableValues, - seed)

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
        aValue = self.a._evaluateUsingCache(variableValues)
        bValue = self.b._evaluateUsingCache(variableValues)
        return aValue * bValue

    def _derive(
        self: Multiply,
        result: InternalResult,
        variableValues: VariableValues,
        seed: numeric
    ) -> None:
        aValue = self.a._evaluateUsingCache(variableValues)
        bValue = self.b._evaluateUsingCache(variableValues)
        # d(a * b) = b * da + a * db
        self.a._derive(result, variableValues, seed * bValue)
        self.b._derive(result, variableValues, seed * aValue)

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
        aValue = self.a._evaluateUsingCache(variableValues)
        bValue = self.b._evaluateUsingCache(variableValues)
        # Note: 0 / b is smooth at b = 0 despite a / b not being smooth at (0, 0)
        if self.a.lacksVariables and aValue == 0:
            return 0
        else:
            self._ensureValueIsInDomain(aValue, bValue)
            return aValue / bValue

    def _derive(
        self: Divide,
        result: InternalResult,
        variableValues: VariableValues,
        seed: numeric
    ) -> None:
        aValue = self.a._evaluateUsingCache(variableValues)
        bValue = self.b._evaluateUsingCache(variableValues)
        # Note: 0 / b is smooth at b = 0 despite a / b not being smooth at (0, 0)
        if self.a.lacksVariables and aValue == 0:
            self.b._derive(result, variableValues, 0)
        else:
            self._ensureValueIsInDomain(aValue, bValue)
            # d(a / b) = (1 / b) * da - (a / b ** 2) * dv
            self.a._derive(result, variableValues, seed / bValue)
            self.b._derive(result, variableValues, - seed * aValue / (bValue ** 2))

    def _ensureValueIsInDomain(
        self: Divide,
        aValue: numeric,
        bValue: numeric
    ) -> None:
        if bValue == 0:
            if aValue == 0:
                raise DomainException("x / y is not smooth around (x = 0, y = 0)")
            else: # aValue != 0
                raise DomainException("x / y blows up around x != 0 and y = 0")

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
    # In case (I), we allow negative bases. In case (II), we only allow positive bases.

    def _evaluate(
        self: Power,
        variableValues: VariableValues
    ) -> numeric:
        aValue = self.a._evaluateUsingCache(variableValues)
        bValue = self.b._evaluateUsingCache(variableValues)
        if self.b.lacksVariables and bValue.is_integer():
            if bValue >= 1:
                return aValue ** bValue
            elif bValue == 0:
                # Note: x ** 0 is smooth at x = 0 despite x ** y not being smooth at (0, 0)
                return 1
            else: # bValue <= -1
                self._ensureValueIsInDomainCaseI(aValue, bValue)
                return aValue ** bValue
        else: # bValue is not an integer
            self._ensureValueIsInDomainCaseII(aValue, bValue)
            return aValue ** bValue

    def _derive(
        self: Power,
        result: InternalResult,
        variableValues: VariableValues,
        seed: numeric
    ) -> None:
        aValue = self.a._evaluateUsingCache(variableValues)
        bValue = self.b._evaluateUsingCache(variableValues)
        if self.b.lacksVariables and bValue.is_integer():
            if bValue >= 2:
                # d(a ** C) = C * a ** (C - 1) * da
                self.a._derive(result, variableValues, seed * bValue * (aValue ** (bValue - 1)))
            elif bValue == 1:
                # d(a ** 1) = da
                self.a._derive(result, variableValues, seed)
            elif bValue == 0:
                # Note: a ** 0 is smooth at a = 0 despite a ** b not being smooth at (0, 0)
                # d(a ** 0) = 0 * da
                self.a._derive(result, variableValues, 0)
            else: # bValue <= -1
                self._ensureValueIsInDomainCaseI(aValue, bValue)
                # d(a ** C) = C * a ** (C - 1) * da
                self.a._derive(result, variableValues, seed * bValue * (aValue ** (bValue - 1)))
        else: # bValue is not an integer
            self._ensureValueIsInDomainCaseII(aValue, bValue)
            selfValue = self._evaluateUsingCache(variableValues)
            # d(a ** b) = b * a ** (b - 1) * da + ln(a) * a ** b * db
            self.a._derive(result, variableValues, seed * bValue * selfValue / aValue)
            self.b._derive(result, variableValues, seed * math.log(aValue) * selfValue)

    def _ensureValueIsInDomainCaseI(
        self: Power,
        aValue: numeric,
        bValue: numeric
    ) -> None:
        if bValue <= -1 and aValue == 0:
            raise DomainException("x ** C blows up around x = 0 when C is a negative integer")

    def _ensureValueIsInDomainCaseII(
        self: Power,
        aValue: numeric,
        bValue: numeric
    ) -> None:
        if aValue == 0:
            if bValue > 0:
                raise DomainException("x ** y is not smooth around x = 0 for y > 0")
            elif bValue == 0:
                raise DomainException("x ** y is not smooth around (x = 0, y = 0)")
            else: # bValue < 0
                raise DomainException("x ** y blows up around x = 0 for y < 0")
        elif aValue < 0:
            raise DomainException("x ** y is undefined for x < 0")
