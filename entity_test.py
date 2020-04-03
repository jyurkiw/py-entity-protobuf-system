from .entity import Entity
from speedComponent_pb2 import Speed
from state_pb2 import State
from truth.truth import AssertThat

TEST_COMPONENT = 'testComponent'

class testIdent(object):
    def __init__(self):
        self.name = TEST_COMPONENT

class testComponent(object):
    def __init__(self):
        self.ident = testIdent()

def protoComponentBuilder():
    c = Speed()
    c.ident.name = TEST_COMPONENT
    c.ident.version = 1
    return c

def test_init_componentsIsEmpty():
    c = Entity()
    AssertThat(c.components).IsEmpty()

def test_init_signatureIsEmpty():
    c = Entity()
    AssertThat(c.signature).IsEmpty()

def test_addComponent_componentsIsNotEmpty():
    c = Entity()
    c.addComponent(testComponent())

    AssertThat(c.components).IsNotEmpty()

def test_addComponent_componentsContainsKey():
    c = Entity()
    c.addComponent(testComponent())

    AssertThat(c.components).ContainsKey(TEST_COMPONENT)

def test_addComponent_signatureIsNotEmpty():
    c = Entity()
    c.addComponent(testComponent())

    AssertThat(c.signature).IsNotEmpty()

def test_addComponent_signatureContains():
    c = Entity()
    c.addComponent(testComponent())

    AssertThat(c.signature).Contains(TEST_COMPONENT)

def test_addComponent_noneComponentException():
    c = Entity()
    with AssertThat(Exception).IsRaised():
        c.addComponent(None)

def test_addComponent_badComponentException():
    c = Entity()
    with AssertThat(Exception).IsRaised():
        c.addComponent(object())

def test_removeComponent_signatureIsEmpty():
    c = Entity()
    c.addComponent(testComponent())
    c.removeComponent(TEST_COMPONENT)

    AssertThat(c.signature).IsEmpty()

def test_removeComponent_componentsIsEmpty():
    c = Entity()
    c.addComponent(testComponent())
    c.removeComponent(TEST_COMPONENT)

    AssertThat(c.components).IsEmpty()

def test_addComponent_protoComp_componentsIsNotEmpty():
    c = Entity()
    c.addComponent(protoComponentBuilder())

    AssertThat(c.components).IsNotEmpty()

def test_addComponent_protoComp_componentsContainsKey():
    c = Entity()
    c.addComponent(protoComponentBuilder())

    AssertThat(c.components).ContainsKey(TEST_COMPONENT)

def test_addComponent_protoComp_signatureIsNotEmpty():
    c = Entity()
    c.addComponent(protoComponentBuilder())

    AssertThat(c.signature).IsNotEmpty()

def test_addComponent_protoComp_signatureContains():
    c = Entity()
    c.addComponent(protoComponentBuilder())

    AssertThat(c.signature).Contains(TEST_COMPONENT)

def test_getComponentSignature_signatureStartsEmpty():
    c = Entity()

    AssertThat(c.getComponentSignature()).IsEmpty()

def test_getSignture_addComponent_signatureIsNotEmpty():
    c = Entity()
    sc1 = State()
    sc1.ident.name = 'state1'
    c.addComponent(sc1)

    AssertThat(c.getComponentSignature()).IsNotEmpty()

def test_getSignture_addComponent_signatureIsState1():
    c = Entity()
    sc1 = State()
    sc1.ident.name = 'state1'
    c.addComponent(sc1)

    AssertThat(c.getComponentSignature()).Contains('state1')
