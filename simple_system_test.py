from simple_system import SimpleSystem
from entity import EntityFactory

from state_pb2 import State

from truth.truth import AssertThat
from unittest import TestCase

def setIdent(c, name, version):
    c.ident.name = name
    c.ident.version = version
    return c

def aState(): return setIdent(State(state='a'), 'aState', 4)
def bState(): return setIdent(State(state='b'), 'bState', 6)

class Parent (object):
    def __init__(self):
        self.aEntityFactory = EntityFactory([aState])
        self.abEntityFactory = EntityFactory([aState, bState])

    def registerSystem(self, s):
        self.system = s

    def getEntities(self, signature):
        entities = [
            self.aEntityFactory.new(),
            self.aEntityFactory.new(),
            self.abEntityFactory.new()
        ]
        return entities

class TestSimpleSystem_setRunFunc(TestCase):
    def setUp(self):
        self.testSystem = SimpleSystem(Parent())

    def tRunFunc(self, e):
        pass

    def testSetRunFunc_entitySignatureSet(self):
        self.testSystem.setRunFunc(self.tRunFunc, ['aState'])

        AssertThat(self.testSystem.entitySignature).Contains('aState')

class TestSimpleSystemRun(TestCase):
    def setUp(self):
        self.testSystem = SimpleSystem(Parent())
        self.testSystem.setRunFunc(self.tRunFunc, ['aState'])

        self.runs = 0

    def tRunFunc(self, e):
        self.runs += 1

    def test_systemHasARunFunc(self):
        AssertThat(self.testSystem._runFunc).IsEqualTo(self.tRunFunc)

    def test_runsOncePerEntityReturned(self):
        self.testSystem.getEntities()
        self.testSystem.run()
        AssertThat(self.runs).IsEqualTo(3)
