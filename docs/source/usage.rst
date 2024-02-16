Usage
=====

Expressions with one variable
-----------------------------

It's easy to both evaluate and take the derivative of an expression that has one variable!
Let's start with an example where we evaluate.

>>> from smoothmath.expression import Variable, Constant
>>> x = Variable("x")
>>> z = x ** Constant(2) + Constant(3) * x
>>> z
Add(Power(Variable("x"), Constant(2)), Multiply(Constant(3), Variable("x")))
>>> z.at(1)
4

A few things to note:
* It's important to wrap our numbers 2 and 3 in ``Constant()`` classes so that they are considered ``Expression``s.
* smoothmath doesn't simplify expressions automatically.
* It wasn't important that we named our variable "x" - it could have been "theta" or "speed" or ...
* smoothmath was able to guess that we wanted to evaluate by setting ``x`` to one because there was only one variable.

It's easy to take the derivative of an expression. Notice that smoothmath treats derivatives as opaque:
it doesn't reduce the derivative to an expression automatically. If we want to see the derivative as an
expression, we call the ``as_expression()`` method.

>>> from smoothmath import Derivative
>>> from smoothmath.expression import Variable, Constant
>>> x = Variable("x")
>>> z = x ** Constant(2) + Constant(3) * x
>>> derivative = Derivative(z)
>>> derivative.at(5)
13
>>> derivative
Derivative(Add(Power(Variable("x"), Constant(2)), Multiply(Constant(3), Variable("x"))))
>>> derivative.as_expression()
Add(Multiply(Constant(2), Variable("x")), Constant(3))


Expressions with several variables
----------------------------------

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
