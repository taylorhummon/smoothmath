Usage
=====

In this section we'll take a quick tour of smoothmath. We'll see how to write
smoothmath expressions, how to evaluate them, and how to differentiate them.


Basics of smoothmath expressions
--------------------------------

We use smoothmath expressions to represent numbers and mathematical functions.
Let's start with something easy: adding two numbers. We can use the
:class:`~smoothmath.expression.Constant` class to represent a number as an
expression, and we represent addition using the
:class:`~smoothmath.expression.Add` class.

>>> from smoothmath.expression import Constant, Add
>>> Add(Constant(2), Constant(3))
Add(Constant(2), Constant(3))

Notice that python just echoed back the expression we entered! Unlike the usual
math operations built in to python, smoothmath expressions don't automatically
reduce to numbers during program evaluation. It would get tiring to write
``Add()`` as a function on the left all of the time, so smoothmath supports using
the standard infix operators like the plus symbol. Under the hood, however,
smoothmath always works with operators written on the left.

>>> from smoothmath.expression import Constant
>>> Constant(2) + Constant(3)
Add(Constant(2), Constant(3))
>>> Constant(7) - Constant(1)
Minus(Constant(7), Constant(1))
>>> Constant(4) * Constant(5)
Multiply(Constant(4), Constant(5))
>>> Constant(2) ** Constant(5)
Power(Constant(2), Constant(5))

Because smoothmath doesn't try to reduce expressions automatically, we can write
expressions that have variables representing unknown values. Notice how
differently this works from using the stardard python math operators.

>>> x + 4  # python gets upset because it doesn't have a value for x
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'x' is not defined
>>> from smoothmath.expression import Variable, Constant
>>> Variable("x") + Constant(4)  # OK, these are smoothmath expressions!
Add(Variable("x"), Constant(4))

You can get a full list of building blocks for making expressions from the
:mod:`smoothmath.expression` module. But what can we do once the have an
expression? The simplest thing we can do is evaluate it using the
:meth:`~smoothmath.Expression.at` method!

>>> from smoothmath.expression import Variable, Constant
>>> z = Constant(2) * Variable("x") + Constant(4)
>>> z.at(3)
10.0
>>> z.at(-2)
0.0


Taking the derivative of an expression with one variable
--------------------------------------------------------

We can take the derivative of a smoothmath expression. Here's how:

>>> from smoothmath import Derivative
>>> from smoothmath.expression import Variable, Constant
>>> z = Variable("x") ** Constant(2) - Constant(1)
>>> d = Derivative(z)
>>> d
Derivative(Minus(Power(Variable("x"), Constant(2)), Constant(1)))
>>> d.as_expression()
Multiply(Constant(2), Variable("x"))
>>> d.at(1)
2.0
>>> d.at(3)
6.0

Just as before, smoothmath doesn't reduce by default. Instead, to reduce the
derivative, we call the :meth:`~smoothmath.Derivative.as_expression` method.
And we can call the :meth:`~smoothmath.Derivative.at` method to evaulate the
derivative for different x values.

Curiously, smoothmath does not actually need to compute the derivative as an
expression in order to evaluate the derivative at x values. So we have a
choice to make:

>>> from smoothmath import Derivative
>>> from smoothmath.expression import Variable, Constant
>>> z = Variable("x") ** Constant(2) - Constant(1)
>>> d_late = Derivative(z, compute_early=False)
>>> d_early = Derivative(z, compute_early=True)

The "late derivative" ``d_late`` and the "early derivative" ``d_early`` behave
identically: they give all the same answers when calling their methods. But
they have different performance characteristics. If you only need to evaluate
your derivative at a few x values, ``d_late`` will be fast. But if you need
to evaluate your derivative at many x values, ``d_early`` can give a
performance boost by internally calculating the derivative as an expression.


Taking the differential of an expression with several variables
---------------------------------------------------------------

Up until now, our expressions have only used a single variable,
``Variable("x")``. This makes things simple: we can evaluate and differentiate
without needing to specify which variable we have in mind. To work with
expressions with multiple variables, we'll need to be a little more careful,
and we'll need to work with points.

>>> from smoothmath import Point
>>> Point(x=7, y=-2)
Point(x=7, y=-2)

When specifying a point, we use keyword arguments that name our variables. The
order of the arguments does not matter, but the variable names do!

>>> from smoothmath import Point
>>> Point(x=7, y=-2) == Point(x=7, y=-2)
True
>>> Point(x=7, y=-2) == Point(y=-2, x=7)
True
>>> Point(x=7, y=-2) == Point(v=7, w=-2)
False

Let's use a point to evaluate an expression that has two variables.

>>> from smoothmath import Point
>>> from smoothmath.expression import Variable
>>> x = Variable("x")
>>> y = Variable("y")
>>> z = x ** 2 + x * y - y ** 2
>>> z.at(Point(x=3, y=2))
11.0

Great! While we can only take the derivative when an expression has a single
variable, we can take the :class:`~smoothmath.Differential` of an expression that
has multiple variables. The differential has several *components*, one for each
variable. Each component of the differential is referred to as a *partial*.

>>> from smoothmath import Differential, Point
>>> from smoothmath.expression import Variable
>>> x = Variable("x")
>>> y = Variable("y")
>>> z = x ** 2 + x * y - y ** 2
>>> differential = Differential(z)
>>> x_partial = differential.component(x)
>>> x_partial.as_expression()
Add(Multiply(Constant(2), Variable("x")), Variable("y"))
>>> x_partial.at(Point(x=1, y=2))
4.0
>>> y_partial = differential.component(y)
>>> y_partial.as_expression()
Minus(Variable("x"), Multiply(Constant(2), Variable("y")))
>>> y_partial.at(Point(x=1, y=2))
-3.0

If we only need the differential at a single point, we can use a
:class:`~smoothmath.LocatedDifferential`.

>>> from smoothmath import Differential, Point
>>> from smoothmath.expression import Variable
>>> x = Variable("x")
>>> y = Variable("y")
>>> z = x ** 2 + x * y - y ** 2
>>> differential = Differential(z)
>>> located_differential = differential.at(Point(x=1, y=2))
>>> located_differential.component(x)
4.0
>>> located_differential.component(y)
-3.0

Taking a located differential is a fast way to compute partials for every variable all in one go.
