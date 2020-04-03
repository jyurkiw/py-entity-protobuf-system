IDENT_KEY = "ident"


class Entity(object):
    """Class: Entity
    A collection of components.
    """

    def __init__(self):
        """Function: __init__
        Components is an empt dictionary and signature is an empty set.
        """
        self.components = dict()
        self.signature = set()
        self._sigLen = 0

    def addComponent(self, component):
        """Function: addComponent
        Add a component and manage the signature.

        Parameters:
            component - The component to add.

        Returns:
            This object (enables builder pattern)
        """
        if component == None:
            raise Exception('Component cannot be None.')

        if not hasattr(component, IDENT_KEY):
            raise Exception('Component must have an ident attribute.')

        if component.ident.name not in self.signature:
            self.signature.add(component.ident.name)
        self.components[component.ident.name] = component

        return self

    def removeComponent(self, name):
        """Function: removeComponent
        Remove the named component from this entity.

        Parameters:
            name - string name of the component.
        """
        if name in self.signature:
            self.signature.remove(name)
            return self.components.pop(name)

    def __getitem__(self, componentName):
        """Function: Get Item
        Overloads the bracket operator.
        """
        return self.components[componentName]

    def hasComponent(self, name):
        """Function: Has Component
        Returns true if this entity has a component by the passed name.
        """
        return name in self.signature

    def getComponentSignature(self):
        """Function: Get Component Signature
        Get the signature of this entity.
        """
        return list(self.signature)


class EntityFactory(object):
    """Class: EntityFactory
    Create entities with passed builder objects.
    """

    def __init__(self, defaultBuilderList):
        """Function: __init__

        Parameters:

            defaultBuilderList - List of functions that provide properly
            formatted default components.
        """
        self.defaultBuilderList = defaultBuilderList

    def new(self):
        e = Entity()
        [e.addComponent(b()) for b in self.defaultBuilderList]

        return e


"""About: Component Object Structure
All component objects must have an ident message that contains their name
along with any additional default constant values useful for all components.
"""

"""About: Builder Functions
Builder functions return a default component with ident data properly set.
"""
