from src.smooth_expression.variable import Variable
from src.smooth_expression.constant import Constant

# Example: Finding the partials of z = x * (x + y) + 5 * y * y at (x, y) = (2, 3)
x = Variable("x")
y = Variable("y")
z = x * (x + y) + Constant(5) * y ** Constant(2)
variableValues = { x: 2, y: 3 }
singleResultWithXPartial = z.deriveSingle(variableValues, x)
singleResultWithYPartial = z.deriveSingle(variableValues, y)
print(f"z = {singleResultWithXPartial.value}")       # Output: z = 55
print(f"∂z/∂x = {singleResultWithXPartial.partial}") # Output: ∂z/∂x = 7
print(f"∂z/∂y = {singleResultWithYPartial.partial}") # Output: ∂z/∂y = 32
