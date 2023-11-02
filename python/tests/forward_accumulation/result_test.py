from src.forward_accumulation.result import Result, InternalResult

def testResult():
    result = Result(3, 4)
    assert result.value == 3
    assert result.partial == 4
    value, partial = result.toPair()
    assert value == 3
    assert partial == 4

def testInternalResult():
    internalResult = InternalResult(True, 1, 2)
    assert internalResult.lacksVariables == True
    assert internalResult.value == 1
    assert internalResult.partial == 2
    lacksVariables, value, partial = internalResult.toTriple()
    assert lacksVariables == True
    assert value == 1
    assert partial == 2
    value, partial = internalResult.toPair()
    assert value == 1
    assert partial == 2
    result = internalResult.toResult()
    assert result.value == 1
    assert result.partial == 2
