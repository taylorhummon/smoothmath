from src.reverse_accumulation.result import Result, InternalResult
from src.reverse_accumulation.variable import Variable

def testResult():
    x = Variable("x")
    result = Result(3, { x: 5 })
    assert result.value == 3
    assert result.partialWithRespectTo(x) == 5
    y = Variable("y")
    assert result.partialWithRespectTo(y) == 0

def testResultWithNoDictionary():
    x = Variable("x")
    result = Result(3)
    assert result.value == 3
    assert result.partialWithRespectTo(x) == 0
    y = Variable("y")
    assert result.partialWithRespectTo(y) == 0

def testInternalResult():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    internalResult = InternalResult(1)
    internalResult.addSeed(x, 3)
    internalResult.addSeed(y, 4)
    internalResult.addSeed(y, 2)
    assert internalResult.value == 1
    assert internalResult.partialWithRespectTo(w) == 0
    assert internalResult.partialWithRespectTo(x) == 3
    assert internalResult.partialWithRespectTo(y) == 6
    result = internalResult.toResult()
    assert result.value == 1
    assert result.partialWithRespectTo(w) == 0
    assert result.partialWithRespectTo(x) == 3
    assert result.partialWithRespectTo(y) == 6
