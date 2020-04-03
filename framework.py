from entity import Entity
from entity import EntityFactory
from random import randint

_alphanum = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
_rmin = 0
_rmax = len(_alphanum) - 1
_keylen = 7
def _genKey():
    """Function: Gen Key
    Generate a random alphanumeric key.
    """
    return ''.join([_alphanum[randint(_rmin, _rmax)] for i in range(0, _keylen)])

class Framework(object):
    """Class: Framework
    An ECS framework that uses protobufs as components.
    """

    def __init__(self):
        self.entities = list()
        self.systems = list()
        self.factories = dict()
        self.dirty = False

        self.componentSystemBreakdown = dict()

    def getEntities(self, entitySignature):
        """Function: Get Entities
        Get all registered entities that contain the passed signature.

        Parameters:
            entitySignature - list An array of component names, usually from a system.

        Returns:
            All entities regestered to this framework that satisfy the passed
            signature.
        """
        entitySignature = entitySignature.copy() # pop is destructive, so protect the passed reference
        entities = set() | self.componentSystemBreakdown.get(entitySignature.pop(), set())
        for componentName in entitySignature:
            entities &= self.componentSystemBreakdown[componentName]
        return entities

    def registerSystem(self, system):
        """Function: Register System
        Register a system with this framework.
        Adds the system to the systems list and updates the system breakdown
        sets according to the passed system's component signature.
        """
        self.systems.append(system)
        for component in [c for c in system.getEntitySignature() if c not in self.componentSystemBreakdown]:
            self.componentSystemBreakdown[component] = set()

    # kwargs for registerEntity
    RE_PROCESS_SYSTEMS = 'processSystems'

    def registerEntity(self, entity, **kwargs):
        """Function: Register Entity
        Registers a single entity with this framework and either upkeep the
        registered system entity lists by adding the entity to any systems whose
        entity signature it satisfies, or mark the framework as dirty so that
        all system entity lists will be regenerated the next time runSystems
        is called.

        Parameters:
            entity - Entity The entity to register.
            processSystems - Boolean (default True) Flag value. If true systems
                are maintained. If false, the framework is set to dirty.
        """
        for componentName in entity.components:
            if componentName in self.componentSystemBreakdown:
                self.componentSystemBreakdown[componentName].add(entity)
        self.entities.append(entity)

        if kwargs.get(Framework.RE_PROCESS_SYSTEMS, True) and not self.dirty:
            for system in self.systems:
                if set.issubset(set(system.getEntitySignature()), set(entity.getComponentSignature())):
                    system._entityList.append(entity)
        else:
            self.dirty = True

    def registerEntities(self, entityList):
        """Function: Register Entities
        Register multiple entities in a single operation. Sets the Framework
        to dirty.

        Parameters:
            entityList - List<Entity> A list of entities.
        """
        for entity in entityList:
            self.registerEntity(entity, **{Framework.RE_PROCESS_SYSTEMS: False})

    def registerEntityFactory(self, builderList):
        """Function: Register Entity Factory
        Register a new entity factory based on the passed builder list.
        Registered factories can be accessed through the getEntityFactory
        function using the key returned when the factory is registered.

        Parameter:
            builderList - List<function> Builder functions used to create the
                factory.

        Returns:
            An alphanumeric key used to access the factory through the
            getEntityFactory function.
        """
        key = _genKey()
        self.factories[key] = EntityFactory(builderList)
        return key

    def getEntityFactory(self, key):
        """Function: Get Entity Factory
        Access a factory with a passed key.

        Parameters:
            key - String A key returned when the factory was registered.

        Returns:
            The factory regestered to the passed key.
        """
        return self.factories[key]

    def runSystems(self):
        for system in self.systems:
            if self.dirty:
                system.getEntities()
            if system.enabled:
                system.run()
        self.dirty = False
