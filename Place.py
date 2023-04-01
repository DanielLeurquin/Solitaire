from abc import ABC, abstractmethod

class Place(ABC):
    """classe abstraite qui definis un endroit ou un carte peut etre placee. Toutes les objets Place peuvent avoir un
    enfant et parfois un parent. Les objets Carte et Zone héritent de place"""
    def __init__(self):
        self.children = None
        self.parent = None
        self.parent_pos = []

    @abstractmethod
    def setChildren(self):
        pass

    @abstractmethod
    def setParent(self):
        pass

    @abstractmethod
    def getBottomChildren(self):
        pass

    @abstractmethod
    def getBottomParent(self):
        pass
