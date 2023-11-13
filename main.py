from smoothmath.variable_values import VariableValues
from smoothmath.expressions.variable import Variable
from smoothmath.expressions.constant import Constant

# Example: Finding the partials of z = x * (x + y) + 5 * y ** 2 at (x, y) = (2, 3)
x = Variable("x")
y = Variable("y")
z = x * (x + y) + Constant(5) * y ** Constant(2)
variable_values = VariableValues({ x: 2, y: 3 })
zValue = z.evaluate(variable_values)
print("### evaluation ###")
print(f"z = {zValue}")       # Output: z = 55
print("### forward accumulation ###")
xPartial = z.partial_at(variable_values, x)
yPartial = z.partial_at(variable_values, y)
print(f"∂z/∂x = {xPartial}") # Output: ∂z/∂x = 7
print(f"∂z/∂y = {yPartial}") # Output: ∂z/∂y = 32
print("### reverse accumulation ###")
all_partials = z.all_partials_at(variable_values)
print(f"∂z/∂x = {all_partials.partial_with_respect_to(x)}") # Output: ∂z/∂x = 7
print(f"∂z/∂y = {all_partials.partial_with_respect_to(y)}") # Output: ∂z/∂y = 32
