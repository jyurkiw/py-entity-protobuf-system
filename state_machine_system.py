from complex_system import ComplexSystem

class StateMachineSystem(ComplexSystem):
    """Class: State Machine System
    A system that implements the basics of a state machine.
    Is intended to be extended unless all states alter in-place.
    """

    def __init__(self, parentECS, entitySignature, stateComponentName):
        """Function: Init
        Sets the class's parentECS, the entity signature, and the
        state attribute name.

        Parameters:
            parentECS - ECS to pull entities from.
            entitySignature - The system's entity signature.
            stateComponentName - The name of the state component this machine
                looks at.
        """
        super().__init__(parentECS)
        self._entitySignature = entitySignature
        self.stateHandlers = dict()
        self.stateComponentName = stateComponentName

    def getEntitySignature(self):
        """Function: Get Entity Signature
        Return the machine's entity signature.
        """
        return self._entitySignature

    def addStateHandler(self, state, handler):
        """Function: Add State Handler
        Add a state handler to this machine.

        Parameters:
            state - string The name of the state.
            handler - func The handler function for this state.
        """
        self.stateHandlers[state] = handler

    def _runFunc(self, entity):
        state = entity[self.stateComponentName].state

        if state not in self.stateHandlers:
            raise Exception('{1} component-owning entity has invalid state: {2}.'
            .format(entity.ident.name, state))

        self.stateHandlers[state](entity)
