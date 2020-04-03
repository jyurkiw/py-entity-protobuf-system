from state_machine_system import StateMachineSystem
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
        self.dirty = True
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
        entities[1]['aState'].state = 'b'
        self.dirty = False
        return entities

class TestStateMachineSystem(TestCase):
    def setUp(self):
        self.testSystem = StateMachineSystem(Parent(), ['aState'], 'aState')
        self.testSystem.addStateHandler('a', self.aRunFunc)
        self.testSystem.addStateHandler('b', self.bRunFunc)

        self.aCount = 0
        self.bCount = 0

    def aRunFunc(self, e):
        self.aCount += 1

    def bRunFunc(self, e):
        self.bCount += 1

    def test_runsOverAll3Entities(self):
        self.testSystem.getEntities()
        self.testSystem.run()

        AssertThat(self.aCount).IsEqualTo(2)
        AssertThat(self.bCount).IsEqualTo(1)
