from entity import Entity
from entity import EntityFactory
from speedComponent_pb2 import Speed
from location_pb2 import Location
from facing_pb2 import Facing
from state_pb2 import State

from truth.truth import AssertThat

def speedFactory():
    s = Speed(mph=5)
    s.ident.name = "speed"
    s.ident.version = 1
    return s

def locationFactory():
    l = Location(xLoc=6, yLoc=7, zLoc=8)
    l.ident.name = "location"
    l.ident.version = 1
    return l

def facingFactory():
    f = Facing(orientation=9, magnitude=10)
    f.ident.name = "facing"
    f.ident.version = 1
    return f

def movementStateFactory():
    m = State(state="ground")
    m.ident.name = "movement_state"
    m.ident.version = 1
    return m

movableBuilderList = [speedFactory, locationFactory, facingFactory, movementStateFactory]

movableFactory = EntityFactory(movableBuilderList)

def test_newReturnsObject():
    e = movableFactory.new()

    AssertThat(e).IsNotNone()

def test_newReturnsEntity():
    e = movableFactory.new()

    AssertThat(e).IsInstanceOf(Entity)

def test_newReturns4Components():
    e = movableFactory.new()

    AssertThat(e.components).HasSize(4)

def test_newContainsSpeed():
    e = movableFactory.new()

    AssertThat(e.components).Contains("speed")

def test_newContainsLocation():
    e = movableFactory.new()

    AssertThat(e.components).Contains("location")

def test_newContainsFacing():
    e = movableFactory.new()

    AssertThat(e.components).Contains("facing")

def test_newContainsMovementState():
    e = movableFactory.new()

    AssertThat(e.components).Contains("movement_state")

def test_newInitState_speedMph():
    e = movableFactory.new()

    AssertThat(e.components["speed"].mph).IsEqualTo(5)

def test_newInitState_locationXLoc():
    e = movableFactory.new()

    AssertThat(e.components["location"].xLoc).IsEqualTo(6)

def test_newInitState_locationYLoc():
    e = movableFactory.new()

    AssertThat(e.components["location"].yLoc).IsEqualTo(7)

def test_newInitState_locationZLoc():
    e = movableFactory.new()

    AssertThat(e.components["location"].zLoc).IsEqualTo(8)

def test_newInitState_facingOrientation():
    e = movableFactory.new()

    AssertThat(e.components["facing"].orientation).IsEqualTo(9)

def test_newInitState_facingMagnitude():
    e = movableFactory.new()

    AssertThat(e.components["facing"].magnitude).IsEqualTo(10)

def test_newInitState_movementState():
    e = movableFactory.new()

    AssertThat(e.components["movement_state"].state).IsEqualTo("ground")
