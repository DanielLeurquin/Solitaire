import pygame
from Carte import Carte
from Place import Place

class Zone(Place):
    def __init__(self, color : tuple, pos : list, width , height):
        self.color = color
        self.pos = pos

        self.children = None
        self.parent = None
        self.rect = pygame.Rect(pos[0],pos[1], width, height)

        self.parent_pos = pos.copy()

    def setChildren(self, carte : Carte):
        """Permet de définir un enfant à la zone"""

        #pour commentaire voir setChildren de Carte.Carte
        if carte !=  None:
            if self.children == None:
                carte.pos = self.pos.copy()
                carte.place = self.pos.copy()
                self.children = carte
                if carte.parent != None:
                    carte.parent.children = None
                    if isinstance(carte.parent, Carte):
                        carte.parent.updateRect()
                carte.parent = self
                carte.updateRect()
                carte.updateParent_pos()

        else:
            self.children = None

    def setParent(self):
        #les zones n'ont pas de parents
        pass

    def getBottomChildren(self):
        """Permet d'obtenir le dernier enfant de la zone"""
        children = self.children
        save = self.children
        while children != None:
            save = children
            children = children.children


        return save

    def getBottomParent(self):
        """Permet de recupere le dernier parent de la zone (toujour None car les zones n'ont pas de parents)"""
        parent = self.parent
        save = self.parent
        while parent != None:
            save = parent
            parent = parent.parent

        return save
