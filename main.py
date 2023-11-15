from smoothmath.expressions import Constant, Variable
from smoothmath.variable_values import VariableValues


x = Variable("x")
y = Variable("y")
seven = Constant(7)

z = x + x + y + seven
p = z.synthetic_partial(x)
print(p.evaluate(VariableValues({x: 5, y: 3})))
