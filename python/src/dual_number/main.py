from src.dual_number.dual_number import *
# !!! stop importing *

# Example: Finding the partials of z = x * (x + y) + y ** 2 at (x, y) = (2, 3)
def f(
    x: DualNumber,
    y: DualNumber
) -> DualNumber:
    return x * (x + y) + power1D(y, 2)
x = DualNumber.fromReal(2)
y = DualNumber.fromReal(3)
epsilon = DualNumber.epsilon()
a = f(x + epsilon, y)
b = f(x, y + epsilon)
print(f"z = {a.realPart}")              # Output: z = 19
print(f"∂z/∂x = {a.infinitesimalPart}") # Output: ∂z/∂x = 7
print(f"∂z/∂y = {b.infinitesimalPart}") # Output: ∂z/∂y = 8
