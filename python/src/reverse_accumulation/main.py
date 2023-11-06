from src.reverse_accumulation.constant import Constant
from src.reverse_accumulation.variable import Variable

print("Reverse Accumulation Method")

# Example: Finding the partials of z = x * (x + y) + 5 * y * y at (x, y) = (2, 3)
x = Variable("x")
y = Variable("y")
z = x * (x + y) + Constant(5) * y ** Constant(2)
multiResult = z.derive({ x: 2, y: 3 })
print(f"z = {multiResult.value}")                       # Output: z = 55
print(f"∂z/∂x = {multiResult.partialWithRespectTo(x)}") # Output: ∂z/∂x = 7
print(f"∂z/∂y = {multiResult.partialWithRespectTo(y)}") # Output: ∂z/∂y = 32
