Usage
=====

Derivatives
-----------

>>> from smoothmath import Derivative
>>> from smoothmath.expression import Variable, Constant
>>> x = Variable("x")
>>> z = x ** Constant(2) + Constant(3)
>>> z.at(1)
4
>>> derivative = Derivative(z)
>>> derivative.at(5)
10
>>> derivative.as_expression()
Multiply(Constant(2), Variable("x"))


Partials
--------

>>> from smoothmath import Point, Partial
>>> from smoothmath.expression import Variable, Constant
>>> x = Variable("x")
>>> z = x ** 2 + Constant(3)
>>> z.at(Point(x=1))
4
>>> partial = Partial(z, x)
>>> partial.at(Point(x=1))
2


>>> from smoothmath import Point, Partial
>>> from smoothmath.expression import Variable, Constant
>>> x = Variable("x")
>>> z = x ** 2 + Constant(3)
>>> partial = Partial(z, x, compute_eagerly=True)
>>> partial.at(Point(x=1))
2
>>> partial.at(Point(x=2))
4
>>> partial.as_expression()
Multiply(Constant(2), Variable("x"))


Differentials
-------------
