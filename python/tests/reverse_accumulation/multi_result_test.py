from src.reverse_accumulation.multi_result import MultiResult, InternalMultiResult
from src.reverse_accumulation.variable import Variable

def testMultiResult():
    x = Variable("x")
    multiResult = MultiResult(3, { x: 5 })
    assert multiResult.value == 3
    assert multiResult.partialWithRespectTo(x) == 5
    y = Variable("y")
    assert multiResult.partialWithRespectTo(y) == 0

def testMultiResultWithNoDictionary():
    x = Variable("x")
    multiResult = MultiResult(3)
    assert multiResult.value == 3
    assert multiResult.partialWithRespectTo(x) == 0
    y = Variable("y")
    assert multiResult.partialWithRespectTo(y) == 0

def testInternalMultiResult():
    w = Variable("w")
    x = Variable("x")
    y = Variable("y")
    internalMultiResult = InternalMultiResult(1)
    internalMultiResult.addSeed(x, 3)
    internalMultiResult.addSeed(y, 4)
    internalMultiResult.addSeed(y, 2)
    assert internalMultiResult.value == 1
    assert internalMultiResult.partialWithRespectTo(w) == 0
    assert internalMultiResult.partialWithRespectTo(x) == 3
    assert internalMultiResult.partialWithRespectTo(y) == 6
    multiResult = internalMultiResult.toMultiResult()
    assert multiResult.value == 1
    assert multiResult.partialWithRespectTo(w) == 0
    assert multiResult.partialWithRespectTo(x) == 3
    assert multiResult.partialWithRespectTo(y) == 6
