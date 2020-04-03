from framework import Framework
from state_pb2 import State
from entity import EntityFactory
from simple_system import SimpleSystem

from truth.truth import AssertThat
from unittest import TestCase
from unittest import SkipTest

def basicStateComponentBuilderFactory(stateName, defaultState, defaultVersion):
    def builder():
        s = State(state=defaultState)
        s.ident.name = stateName
        s.ident.version = defaultVersion
        return s
    return builder

class TestFramework_registerEntity(TestCase):
    testSignature = ['c1']

    def setUp(self):
        f = Framework()
        c1sys = SimpleSystem(f)
        c1sys.setRunFunc(lambda e: None, TestFramework_registerEntity.testSignature)

        f.registerSystem(c1sys)

        self.ckey = f.registerEntityFactory([
            basicStateComponentBuilderFactory('c1', 'clear', 1)
            ])
        self.dkey = f.registerEntityFactory([
            basicStateComponentBuilderFactory('d1', 'foo', 3)
            ])


        self.framework = f

    def test_registerEntity_addOneEntity(self):
        ef = self.framework.getEntityFactory(self.ckey)

        self.framework.registerEntity(ef.new())

        AssertThat(self.framework.entities).HasSize(1)

    def test_registerEntities_addThreeEntities(self):
        ef = self.framework.getEntityFactory(self.ckey)

        self.framework.registerEntities([
            ef.new(),
            ef.new(),
            ef.new()
        ])

        AssertThat(self.framework.entities).HasSize(3)

    def test_registerEntity_addC1ToBreakdown(self):
        ef = self.framework.getEntityFactory(self.ckey)

        self.framework.registerEntity(ef.new())

        AssertThat(self.framework.componentSystemBreakdown).Contains('c1')

    def test_registerEntity_addEntityToC1Breakdown(self):
        ef = self.framework.getEntityFactory(self.ckey)

        e = ef.new()
        self.framework.registerEntity(e)

        AssertThat(self.framework.componentSystemBreakdown['c1']).Contains(e)

    def test_registerEntities_addThreeC1EntitiesToBreakdown(self):
        ef = self.framework.getEntityFactory(self.ckey)

        e = ef.new()
        f = ef.new()
        g = ef.new()
        self.framework.registerEntities([e, f, g])

        AssertThat(self.framework.componentSystemBreakdown['c1']).HasSize(3)

    def test_registerEntity_addOneEntity_noValidKey(self):
        df = self.framework.getEntityFactory(self.dkey)

        d = df.new()
        self.framework.registerEntity(d)

        AssertThat(self.framework.entities).HasSize(1)

class TestFramework_getEntities (TestCase):
    c1testSignature = ['c1']
    d1testSignature = ['d1']

    def setUp(self):
        f = Framework()
        c1sys = SimpleSystem(f)
        c1sys.setRunFunc(lambda e: None, TestFramework_getEntities.c1testSignature)

        f.registerSystem(c1sys)

        self.ckey = f.registerEntityFactory([
            basicStateComponentBuilderFactory('c1', 'clear', 1)
            ])
        ef = f.getEntityFactory(self.ckey)

        f.registerEntities([
            ef.new(),
            ef.new(),
            ef.new()
        ])

        self.d1System = SimpleSystem(f)
        self.d1System.setRunFunc(lambda e: None, TestFramework_getEntities.d1testSignature)
        self.d1Factory = EntityFactory([basicStateComponentBuilderFactory('d1', 'foo', 1)])

        self.framework = f

    def test_getEntities_allEntitiesMatch(self):
        entities = self.framework.getEntities(TestFramework_getEntities.c1testSignature)

        AssertThat(entities).HasSize(3)

    def test_getEntities_oneEntityDoesNotMatch_noD1System(self):
        e = self.d1Factory.new()
        self.framework.registerEntity(e)

        entities = self.framework.getEntities(TestFramework_getEntities.c1testSignature)

        AssertThat(entities).HasSize(3)

    def test_getEntities_oneEntityDoesNotMatch(self):
        self.framework.registerSystem(self.d1System)

        d = self.d1Factory.new()
        self.framework.registerEntity(d)

        entities = self.framework.getEntities(TestFramework_getEntities.c1testSignature)

        AssertThat(entities).HasSize(3)

    def test_getEntities_noEntitiesMatch(self):
        entities = self.framework.getEntities(TestFramework_getEntities.d1testSignature)

        AssertThat(entities).HasSize(0)
