import math
import smoothmath as sm
from smoothmath._private.utilities import is_even


### Unary Functions ###


def negation(
    x: sm.real_number
) -> sm.real_number:
    return - x


def reciprocal(
    x: sm.real_number
) -> sm.real_number:
    if x == 0:
        raise sm.DomainError("reciprocal(x) blows up around x = 0")
    else:
        return 1 / x


def cosine(
    x: sm.real_number
) -> sm.real_number:
    return math.cos(x)


def sine(
    x: sm.real_number
) -> sm.real_number:
    return math.sin(x)


### Parameterized Unary Functions ###


def nth_power(
    x: sm.real_number,
    n: int
) -> sm.real_number:
    if n <= 0:
        raise sm.DomainError(f"nth_power(x, n) is not defined for n = {n}")
    else:
        return x ** n


def nth_root(
    x: sm.real_number,
    n: int
) -> sm.real_number:
    if n <= 0:
        raise sm.DomainError(f"nth_root(x, n) is not defined for n = {n}")
    elif n == 1:
        return x
    elif n == 2:
        if x > 0:
            return math.sqrt(x)
        elif x == 0:
            raise sm.DomainError(f"nth_root(x, n) is not defined at x = 0 for n = 2")
        else: # x < 0
            raise sm.DomainError(f"nth_root(x, n) is not defined for negative x for n = 2")
    elif n == 3:
        if x > 0:
            return math.cbrt(x)
        elif x == 0:
            raise sm.DomainError(f"nth_root(x, n) is not defined at x = 0 for n = 3")
        else: # x < 0
            # CAREFUL: math.cbrt can return imaginary values for negative inputs
            return - math.cbrt(- x)
    else: # n >= 4
        if is_even(n):
            if x > 0:
                return x ** (1 / n)
            elif x == 0:
                raise sm.DomainError(f"nth_root(x, n) is not defined at x = 0 for n = {n}")
            else: # x < 0
                raise sm.DomainError(f"nth_root(x, n) is not defined for negative x for n = {n}")
        else: # n is odd
            if x > 0:
                return x ** (1 / n)
            elif x == 0:
                raise sm.DomainError(f"nth_root(x, n) is not defined at x = 0 for n = {n}")
            else: # x < 0
                return - ((- x) ** (1 / n))


def exponential(
    x: sm.real_number,
    base: sm.real_number = math.e
) -> sm.real_number:
    if base <= 0:
        raise sm.DomainError(f"exponential(x) must have a positive base, found: {base}")
    else:
        return base ** x


def logarithm(
    x: sm.real_number,
    base: sm.real_number = math.e
) -> sm.real_number:
    if base <= 0:
        raise sm.DomainError("logarithm(x) must have a positive base")
    elif base == 1:
        raise sm.DomainError("logarithm(x) cannot have base = 1")
    return math.log(x, base)


### Binary Functions ###


def minus(
    x: sm.real_number,
    y: sm.real_number
) -> sm.real_number:
    return x - y


def divide(
    x: sm.real_number,
    y: sm.real_number
) -> sm.real_number:
    if y == 0:
        if x == 0:
            raise sm.DomainError("divide(x, y) is not smooth around (x = 0, y = 0)")
        else: # x != 0
            raise sm.DomainError("divide(x, y) blows up around x != 0 and y = 0")
    else:
        return x / y


def power(
    x: sm.real_number,
    y: sm.real_number
) -> sm.real_number:
    if x == 0:
        if y > 0:
            raise sm.DomainError("power(x, y) is not smooth around x = 0 for y > 0")
        elif y == 0:
            raise sm.DomainError("power(x, y) is not smooth around (x = 0, y = 0)")
        else: # y < 0
            raise sm.DomainError("power(x, y) blows up around x = 0 for y < 0")
    elif x < 0:
        raise sm.DomainError("power(x, y) is undefined for x < 0")
    else: # x > 0
        return x ** y


### n-Ary Functions ###


def add(
    *args: sm.real_number
) -> sm.real_number:
    return sum(args)


def multiply(
    *args: sm.real_number
) -> sm.real_number:
    product = 1
    for arg in args:
        if arg == 0:
            return 0
        product *= arg
    return product