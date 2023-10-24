from expression import *

def testPolynomialOfTwoVariables():
    x = Variable(2)
    y = Variable(3)
    c = Constant(5)
    z = x * (x + y) + c * y * y
    xPartial = z.evaluateAndDerive(x).partial
    yPartial = z.evaluateAndDerive(y).partial
    assert xPartial == 7
    assert yPartial == 32
