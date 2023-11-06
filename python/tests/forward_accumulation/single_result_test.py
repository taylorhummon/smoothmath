from src.forward_accumulation.single_result import SingleResult, InternalSingleResult

def testSingleResult():
    singleResult = SingleResult(3, 4)
    assert singleResult.value == 3
    assert singleResult.partial == 4
    value, partial = singleResult.toPair()
    assert value == 3
    assert partial == 4

def testInternalSingleResult():
    internalResult = InternalSingleResult(True, 1, 2)
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
    singleResult = internalResult.toSingleResult()
    assert singleResult.value == 1
    assert singleResult.partial == 2
