from src.smooth_expression.variable_values import VariableValues
from src.smooth_expression.variable import Variable
from src.smooth_expression.constant import Constant

# Example: Finding the partials of z = x * (x + y) + 5 * y ** 2 at (x, y) = (2, 3)
x = Variable("x")
y = Variable("y")
z = x * (x + y) + Constant(5) * y ** Constant(2)
variableValues = VariableValues({ x: 2, y: 3 })
zValue = z.evaluate(variableValues)
print("### evaluation ###")
print(f"z = {zValue}")       # Output: z = 55
print("### forward accumulation ###")
xPartial = z.partialAt(variableValues, x)
yPartial = z.partialAt(variableValues, y)
print(f"∂z/∂x = {xPartial}") # Output: ∂z/∂x = 7
print(f"∂z/∂y = {yPartial}") # Output: ∂z/∂y = 32
print("### reverse accumulation ###")
allPartials = z.allPartialsAt(variableValues)
print(f"∂z/∂x = {allPartials.partialWithRespectTo(x)}") # Output: ∂z/∂x = 7
print(f"∂z/∂y = {allPartials.partialWithRespectTo(y)}") # Output: ∂z/∂y = 32
