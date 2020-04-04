# py-entity-protobuf-system
A basic entity-component-system implemented with google protobufs as components.

## The EPS contains the following:

* An EntityFactory class for quick creation of default-state entities.
* An abstract ComplexSystem class for inheritance.
* A SimpleSystem class for systems that edit entities in-place.
* A StateMachineSystem class for systems that drive logic based on entity state.
* A Framework class to keep track of systems and factories, and to manage
entities based on system requirements.

# What is an ECS?

An Entity-Component-System is a compositional programming pattern.

**Entities** are simple bags that hold **Components**.
**Components** are simple objects that hold *data*.
**Systems** operate on **Entities** filtered by their **Component** composition
such that they only receive Entities that contain the components the system
needs to operate.

# What are "Protobufs"?

https://developers.google.com/protocol-buffers

Google Protocol Buffers are a language neutral, platform-neutral solution
for serializing structured data. A Protocol Buffer (or "protobuf" for short)
can be compiled into any supported language via the *protoc* compiler.

Since components are supposed to be plain old dumb objects (with all logic
being defined in systems. If your components operate on data, you're doing it
wrong) .proto files compiled into python objects through protoc
are perfect for our needs. And we additionally get a bunch of serialization
functionality for free. Thanks, Google!

# Code Examples

### A note about the *ident* protobuf

The ident.proto message is a required dependency for all components. It contains
name and version values that are important for both entities as well as systems.
The name value is a string used by entities to allow access to the component,
and the version entry can be used to handle serialized components across
multiple versions of a program.

ident must be included in a component as an ident message named ident.
See the test components in the proto folder for examples.

## Creating and Using an EntityFactory

The speed protobuf is defined as a message with an integer named "mph".
The direction protobuf is defined as a message with a float named "facing".
The position protobuf is defined as a message with two ints named "x" and "y".

    def speedBuilder():
      s = Speed(mph=0)
      s.ident.name = "speed"
      return s

    def directionBuilder():
      d = Direction(facing=0.0)
      d.ident.name = "direction"
      return d

    def positionBuilder():
      p = Position(x=0, y=0)
      p.ident.name = "position"
      return p

    movableEntityFactory = EntityFactory([speedBuilder, directionBuilder, positionBuilder])

    movableEntity = movableEntityFactory.new()
    movableEntity['position'].x = 12
    movableEntity['position'].y = 55
    movableEntity['speed'].mph = 88
    movableEntity['direction'].facing = 270.0

The factory will instantiate an entity containing a speed, direction, and
position component, with all components populated with default data.

## Adding a new component to an existing Entity

    movableEntity = movableEntityFactory.new()
    attackComponent = Attack(damage=4, accuracy=0.75)
    attackComponent.ident.name = 'attack'
    attackComponent.ident.version = 4

    movableEntity.addComponent(attackComponent)

## Creating a simple system to heal entities on a primative timer

    # e is an entity passed to the system
    def healEveryTenTicks(e):
      if e.tick.value % 10 == 0:
        e.health.hp += e.health.naturalHealingValue

    # we have a framework named 'f'
    healingSystem = SimpleSystem(f)
    healingSystem.setRunFunc(healEveryTenTicks, ['tick', 'health'])

    # run the system
    healingSystem.getEntities()
    healingSystem.run()

## Creating a state machine system to move based on terrain

    # e is an entity passed to the system
    def moveOverRoad(e):
      # vehicles move very fast over road
      if e['unitType'].type == 'vehicle':
        moveBasedOnDirection(e['direction'], e['speed'].mph * 2)
      # so do infantry, but they take a defense penalty if possible
      elif e['unitType'].type == 'infantry':
        moveBasedOnDirection(e['direction'], e['speed'].mph * 1.1)
        if e.hasComponent('defense'):
          e['defense'].currentPenalty += 0.2

    def moveOverWater(e):
      # vehicles move over water slowly
      if e['unitType'].type == 'vehicle':
        # if they don't float, they sink and are destroyed
        if ...
        # if they do float, they move at speed unless they are taking on water
        elif ...
      elif e['unitType'].type == 'infancty':
        # move slowly
        ...
        # decrement stamina
        ... # depleted stamina deals damage in a different system.

    # We have a framework named 'f'
    movementSystem = StateMachineSystem(f, ['unitType', 'direction', 'speed', 'terrainState'], 'terrainState')
    movementSystem.addStateHandler('road', moveOverRoad)
    movementSystem.addStateHandler('water', moveOverWater)

## Creating a framework

    # A framework manages entities according to the requirements of systems
    # and stores your entity factories for you.
    f = Framework()

    someSystem = ... create a system and set the runFunc
    someOtherSystem = ... create a second system

    f.registerSystem(someSystem)
    f.registerSystem(someOtherSystem)

    ef = ... make a new entity factory

    initialEntities = list()
    for e in range(1, 1000):
      ... create a thousand entities and add them to initialEntities
    f.registerEntities(initialEntities)

    f.runSystems()
