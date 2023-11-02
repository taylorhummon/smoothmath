from __future__ import annotations
from abc import ABC, abstractmethod
import math
from src.forward_accumulation.custom_types import numeric, VariableValues
from src.forward_accumulation.custom_exceptions import DomainException
from src.forward_accumulation.result import Result, InternalResult

class Expression(ABC):
    def derive(
        self: Expression,
        variableValues: VariableValues,
        withRespectTo: Variable,
    ) -> Result:
        return self._derive(variableValues, withRespectTo).toResult()

    @abstractmethod
    def _derive(
        self: Expression,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
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

class Constant(Expression):
    def __init__(
        self: Constant,
        value: numeric
    ) -> None:
        self.value = value

    def _derive(
        self: Constant,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
        return InternalResult(
            lacksVariables = True,
            value = self.value,
            partial = 0
        )

class Variable(Expression):
    def __init__(
        self: Variable
    ) -> None:
        pass

    def _derive(
        self: Variable,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
        value = variableValues.get(self, None)
        if value is None:
            raise Exception("variableValues is missing a value for a variable")
        return InternalResult(
            lacksVariables = False,
            value = value,
            partial = 1 if self == withRespectTo else 0
        )

### Unary Expressions ###

class UnaryExpression(Expression):
    def __init__(
        self: UnaryExpression,
        a: Expression
    ) -> None:
        if not isinstance(a, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {a}")
        self.a = a

class Negation(UnaryExpression):
    def __init__(
        self: Negation,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _derive(
        self: Negation,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
        aLacksVariables, aValue, aPartial = self.a._derive(variableValues, withRespectTo).toTriple()
        # d(-a) = -da
        return InternalResult(
            lacksVariables = aLacksVariables,
            value = -aValue,
            partial = -aPartial
        )

class Reciprocal(UnaryExpression):
    def __init__(
        self: Reciprocal,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _derive(
        self: Reciprocal,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
        aLacksVariables, aValue, aPartial = self.a._derive(variableValues, withRespectTo).toTriple()
        if aValue == 0:
            raise DomainException("1 / x blows up around x = 0")
        resultValue = 1 / aValue
        # d(1 / a) = - (1 / a ** 2) * da
        return InternalResult(
            lacksVariables = aLacksVariables,
            value = resultValue,
            partial = - (resultValue ** 2) * aPartial
        )

class SquareRoot(UnaryExpression):
    def __init__(
        self: SquareRoot,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _derive(
        self: SquareRoot,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
        aLacksVariables, aValue, aPartial = self.a._derive(variableValues, withRespectTo).toTriple()
        if aValue == 0:
            raise DomainException("sqrt(x) is not smooth around x = 0")
        elif aValue < 0:
            raise DomainException("sqrt(x) is undefined for x < 0")
        resultValue = math.sqrt(aValue)
        # d(sqrt(a)) = (1 / (2 sqrt(a))) * da
        return InternalResult(
            lacksVariables = aLacksVariables,
            value = resultValue,
            partial = (1 / (2 * resultValue)) * aPartial
        )

class NaturalExponential(UnaryExpression):
    def __init__(
        self: NaturalExponential,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _derive(
        self: NaturalExponential,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
        aLacksVariables, aValue, aPartial = self.a._derive(variableValues, withRespectTo).toTriple()
        resultValue = math.e ** aValue
        # d(e ** a) = e ** a * da
        return InternalResult(
            lacksVariables = aLacksVariables,
            value = resultValue,
            partial = resultValue * aPartial
        )

class NaturalLogarithm(UnaryExpression):
    def __init__(
        self: NaturalLogarithm,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _derive(
        self: NaturalLogarithm,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
        aLacksVariables, aValue, aPartial = self.a._derive(variableValues, withRespectTo).toTriple()
        if aValue == 0:
            raise DomainException("ln(x) blows up around x = 0")
        elif aValue < 0:
            raise DomainException("ln(x) is undefined for x < 0")
        # d(ln(a)) = (1 / a) * da
        return InternalResult(
            lacksVariables = aLacksVariables,
            value = math.log(aValue),
            partial = aPartial / aValue
        )

class Sine(UnaryExpression):
    def __init__(
        self: Sine,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _derive(
        self: Sine,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
        aLacksVariables, aValue, aPartial = self.a._derive(variableValues, withRespectTo).toTriple()
        # d(sin(a)) = cos(a) * da
        return InternalResult(
            lacksVariables = aLacksVariables,
            value = math.sin(aValue),
            partial = math.cos(aValue) * aPartial
        )

class Cosine(UnaryExpression):
    def __init__(
        self: Cosine,
        a: Expression
    ) -> None:
        super().__init__(a)

    def _derive(
        self: Cosine,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
        aLacksVariables, aValue, aPartial = self.a._derive(variableValues, withRespectTo).toTriple()
        # d(cos(a)) = - sin(a) * da
        return InternalResult(
            lacksVariables = aLacksVariables,
            value = math.cos(aValue),
            partial = - math.sin(aValue) * aPartial
        )

### Binary Expressions ###

class BinaryExpression(Expression):
    def __init__(
        self: UnaryExpression,
        a: Expression,
        b: Expression
    ) -> None:
        if not isinstance(a, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {a}")
        if not isinstance(b, Expression):
            raise Exception(f"Expressions must be composed of Expressions, found {b}")
        self.a = a
        self.b = b

class Plus(BinaryExpression):
    def __init__(
        self: Plus,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _derive(
        self: Plus,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
        aLacksVariables, aValue, aPartial = self.a._derive(variableValues, withRespectTo).toTriple()
        bLacksVariables, bValue, bPartial = self.b._derive(variableValues, withRespectTo).toTriple()
        # d(a + b) = da + db
        return InternalResult(
            lacksVariables = aLacksVariables and bLacksVariables,
            value = aValue + bValue,
            partial = aPartial + bPartial
        )

class Minus(BinaryExpression):
    def __init__(
        self: Minus,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _derive(
        self: Minus,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
        aLacksVariables, aValue, aPartial = self.a._derive(variableValues, withRespectTo).toTriple()
        bLacksVariables, bValue, bPartial = self.b._derive(variableValues, withRespectTo).toTriple()
        # d(a - b) = da - db
        return InternalResult(
            lacksVariables = aLacksVariables and bLacksVariables,
            value = aValue - bValue,
            partial = aPartial - bPartial
        )

class Multiply(BinaryExpression):
    def __init__(
        self: Multiply,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _derive(
        self: Multiply,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
        aLacksVariables, aValue, aPartial = self.a._derive(variableValues, withRespectTo).toTriple()
        bLacksVariables, bValue, bPartial = self.b._derive(variableValues, withRespectTo).toTriple()
        # d(a * b) = b * da + a * db
        return InternalResult(
            lacksVariables = aLacksVariables and bLacksVariables,
            value = aValue * bValue,
            partial = bValue * aPartial + aValue * bPartial
        )

class Divide(BinaryExpression):
    def __init__(
        self: Divide,
        a: Expression,
        b: Expression
    ) -> None:
        super().__init__(a, b)

    def _derive(
        self: Divide,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
        aLacksVariables, aValue, aPartial = self.a._derive(variableValues, withRespectTo).toTriple()
        bLacksVariables, bValue, bPartial = self.b._derive(variableValues, withRespectTo).toTriple()
        # Note: 0 / y is smooth at y = 0 despite x / y not being smooth at (0, 0)
        if aLacksVariables and aValue == 0:
            return InternalResult(0, 0, bLacksVariables)
        if bValue == 0:
            if aValue == 0:
                raise DomainException("x / y is not smooth around (x = 0, y = 0)")
            else: # aValue != 0
                raise DomainException("x / y blows up around x != 0 and y = 0")
        # d(a / b) = (1 / b) * da - (a / b ** 2) * db
        return InternalResult(
            lacksVariables = aLacksVariables and bLacksVariables,
            value = aValue / bValue,
            partial = (bValue * aPartial - aValue * bPartial) / bValue ** 2
        )

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

    def _derive(
        self: Power,
        variableValues: VariableValues,
        withRespectTo: Variable
    ) -> InternalResult:
        aLacksVariables, aValue, aPartial = self.a._derive(variableValues, withRespectTo).toTriple()
        bLacksVariables, bValue, bPartial = self.b._derive(variableValues, withRespectTo).toTriple()
        lacksVariables = aLacksVariables and bLacksVariables
        if bLacksVariables and bValue.is_integer(): # CASE I: has constant integer exponent
            if bValue >= 2:
                resultValue = aValue ** bValue
                # d(a ** C) = C * a ** (C - 1) * da
                resultPartial = bValue * (aValue ** (bValue - 1)) * aPartial
                return InternalResult(lacksVariables, resultValue, resultPartial)
            elif bValue == 1:
                resultValue = aValue
                # d(a ** 1) = 1 * da
                resultPartial = aPartial
                return InternalResult(lacksVariables, resultValue, resultPartial)
            elif bValue == 0:
                # Note: x ** 0 is smooth at x = 0 despite x ** y not being smooth at (0, 0)
                resultValue = 1
                # d(a ** 0) = 0 * da
                resultPartial = 0
                return InternalResult(lacksVariables, resultValue, resultPartial)
            else: # bValue <= -1:
                if aValue == 0:
                    raise DomainException("x ** C blows up around x = 0 when C is a negative integer")
                resultValue = aValue ** bValue
                # d(a ** C) = C * a ** (C - 1) * da
                resultPartial = (bValue * resultValue / aValue) * aPartial
                return InternalResult(lacksVariables, resultValue, resultPartial)
        else: # CASE II: does not have a constant integer exponent
            if aValue > 0:
                resultValue = aValue ** bValue
                # d(a ** b) = b * a ** (b - 1) * da + ln(a) * a ** b * db
                resultPartial = (
                    (bValue * resultValue / aValue) * aPartial +
                    math.log(aValue) * resultValue * bPartial
                )
                return InternalResult(lacksVariables, resultValue, resultPartial)
            elif aValue == 0:
                if bValue > 0:
                    raise DomainException("x ** y is not smooth around x = 0 for y > 0")
                elif bValue == 0:
                    raise DomainException("x ** y is not smooth around (x = 0, y = 0)")
                else: # bValue < 0
                    raise DomainException("x ** y blows up around x = 0 for y < 0")
            else: # aValue < 0
                raise DomainException("x ** y is undefined for x < 0")
