from abc import ABC, abstractmethod, abstractproperty

class ComplexSystem(ABC):
    """Class: ComplexSystem
    A System that runs an operation over a collection of entities.
    Complex system is abstract. This allows other systems to be embedded
    into the concrete system.
    """

    def __init__(self, parentECS):
        """Function: Init
        Set the entitySignature, run function, and parent ECS.

        Parameters:
            parentECS - ECS system to pull entities from.
        """
        self._parent = parentECS
        self._entityList = list()

        self.enabled = True

    @abstractproperty
    def getEntitySignature(self):
        """Function: GetEntitySignature
        Return this system's entity signature.

        Returns:
            An entity signature (see: Entity Signatures)
        """
        pass

    def run(self):
        """Function: Run
        Run the system through a complete iteration of the entity list.
        """
        for entity in self._entityList:
            self._runFunc(entity)

    @abstractmethod
    def _runFunc(self, entity):
        """Function: RunFunction
        Execute logic over an entity that satsfies this system's entity
        signature.

        Parameters:
            entity - The entity to operate over.
        """
        pass

    def getEntities(self):
        """Function: GetEntities
        Refresh the entity list for this system from the parent ECS.
        """
        if self._entityList:
            del self._entityList
        self._entityList = self._parent.getEntities(self.getEntitySignature())

"""About: Entity Signatures
A system's entity signature is a list of strings made up of ident.proto name
field values. It is used by the ECS framework class to pull a list of entities
using the framework's getEntities() function.
"""

"""About: Run Function Signatures
All run functions are required to have the following signature:
function(e) where 'e' is an entity that satisfies the system's entity signature.
"""
