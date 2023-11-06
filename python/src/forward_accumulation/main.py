from src.forward_accumulation.variable import Variable
from src.forward_accumulation.constant import Constant

print("Forward Accumulation Method")

# Example: Finding the partials of z = x * (x + y) + 5 * y * y at (x, y) = (2, 3)
x = Variable("x")
y = Variable("y")
z = x * (x + y) + Constant(5) * y ** Constant(2)
variableValues = { x: 2, y: 3 }
resultWithXPartial = z.derive(variableValues, x)
resultWithYPartial = z.derive(variableValues, y)
print(f"z = {resultWithXPartial.value}")       # Output: z = 55
print(f"∂z/∂x = {resultWithXPartial.partial}") # Output: ∂z/∂x = 7
print(f"∂z/∂y = {resultWithYPartial.partial}") # Output: ∂z/∂y = 32
