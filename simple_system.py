from complex_system import ComplexSystem

class SimpleSystem(ComplexSystem):
    """Class: SimpleSystem
    A System that runs an operation over a collection of entities.
    Changes are made to entities in-place as external access is difficult.
    If external system access is required, use ComplexSystem.
    """

    def __init__(self, parentECS):
        """Function: Init
        Set the entitySignature, run function, and parent ECS.

        Parameters:
            parentECS - ECS system to pull entities from.
        """
        super().__init__(parentECS)
        self.entitySignature = list()

    def setRunFunc(self, runFunc, entitySignature):
        """Function: Set Run Function

        Parameters:
            runFunc - The function to run over entities.
            entitySignature - The runFunc's component requirement.
        """
        self._runFunc = runFunc
        self.entitySignature = entitySignature
        return self

    def _runFunc(self, entity):
        raise Exception('_runFunc is undefined. Call setRunFunc before execution.')

    def getEntitySignature(self):
        if not self.entitySignature:
            raise Exception('entitySignature is undefined. Call setRunFunc before execution.')
        return self.entitySignature
