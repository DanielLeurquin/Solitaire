import pygame
import numpy as np
from Place import Place


path = "ressources/cartes/"

def resize(surface : pygame.Surface, factor):

    reso = (int(surface.get_width() * factor), int(surface.get_height() * factor))
    return pygame.transform.scale(surface, reso)


class Carte(Place):

    def __init__(self, nom : str, pos: list):
        self.nom = nom          #nom de la carte
        self.image = pygame.image.load(path + "back"+".png")    #image pygame
        self.pos = pos          #position sur l'écran en temps reel
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height()) #zone de cliquage de la carte
        self.place = pos.copy()     #emplacement de la carte (endroit ou elle revient si elle est lachée)
        self.hide = True            #defini si la carte est face visible True indique face cachée
        self.drag = False           #defini si la carte est entrain d'etre deplacee
        self.drag_offset = (0,0)    #offset pour que le dag se fasse depuis le coin ou on a cliqié sur la carte


        self.vector = np.array([0,0])  #vecteur de deplacement retour en cas de lache de carte
        self.norm = np.linalg.norm(self.vector)     #norme du vecteur
        self.speed = 5                              #vitesse de retour des cartes

        #rect qui permet de verifier si une carte est bien en collision avec une zone ou une autre carte
        #ce rect est plus petit que le premier afin de verifier que les colision sont intentionnelles
        self.move_rect = pygame.Rect(self.pos[0]+10, self.pos[1]+10, self.image.get_width()-20, self.image.get_height()-20)

        self.parent = None  #place sur laquelle la carte actuelle est placee
        self.children = None  #carte potentiellement attachee a cette carte

        # place a laquelle l'enfant devra etre place afin de ne pas cacher completement son parent
        self.parent_pos = [self.pos[0], self.pos[1] + 30]

    def reveal(self):
        """Retourne une carte face visible"""
        self.image = pygame.image.load(path + self.nom + ".png")
        self.hide = False
        self.updateRect()

    def unreveal(self):
        """Retourne une carte face cachee"""
        self.image = pygame.image.load(path +"back" + ".png")
        self.hide = True
        self.updateRect()


    def updateRect(self):
        """Met a jour le rect (zone de clic) de la carte"""

        #si la carte n'as pas d'enfant la taille de son rect est celle par defaut avec sa position actuelle
        if self.children == None:
            self.rect = pygame.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())
            self.move_rect = pygame.Rect(self.pos[0] + 10, self.pos[1] + 10, self.image.get_width() - 20,
                                         self.image.get_height() - 20)

        #si la carte a un enfant
        else:
            #son rect est reduit uniquement a la partie visible de la carte, son move_rect devient la meme que son rect
            self.rect = pygame.Rect(self.pos[0], self.pos[1], self.image.get_width(), 30)
            self.move_rect = pygame.Rect(self.pos[0], self.pos[1], self.image.get_width(), 30)

            #si la carte est sur une zone d'as, mais n'est pas au dessus de la pile, alors son rect est placé hors de la fenetre
            #afin que le carte ne puisse pas etre deplacee
            if self.children.nom[1] == self.nom[1]:
                self.rect = pygame.Rect(-10000, -10000, self.image.get_width(), 30)
                self.move_rect = pygame.Rect(-10000, -10000, self.image.get_width(), 30)

        self.parent_pos = [self.pos[0], self.pos[1] + 30]

    def updateParent_pos(self):
        """actualise la position des cartes filles d'une pile pour que lors d'un drag les cartes se deplacent d'un seul bloc"""
        self.parent_pos = [self.pos[0], self.pos[1] + 30]
        #recupere toutes les cartes filles depuis la carte courrante
        L = self.getChildrenList()
        for elem in L:
            #verifie si la carte est sur une zone classique (pas zone d'as)
            if elem.nom[1] != elem.parent.nom[1]:
                #actualise les position de l'element courant en fonct du parent_pos de son parent, et redefinis sont parent_pos
                #pour les cartes filles suivantes, actualise aussi les rects pour la position
                elem.pos = elem.parent.parent_pos
                elem.place = elem.pos.copy()
                elem.parent_pos = [elem.pos[0], elem.pos[1] + 30]
                elem.updateRect()
            else:
                #si la carte est sur une zone d'as le parent_pos ne doit pas contenir de decalage
                elem.pos = elem.parent.pos
                elem.place = elem.pos.copy()
                elem.parent_pos = elem.pos.copy()
                elem.updateRect()

    def findVector(self):
        """Trouve le vecteur de retour de la carte en fonction de sa place et de l'endroit dont la carte à ete lachee"""

        #trouve la direction du vecteur
        self.vector = np.array([float(self.place[0]-self.pos[0]), float(self.place[1]-self.pos[1])])
        self.norm = np.linalg.norm(self.vector)
        #si vecteur non nul
        if self.norm != 0:
            #normalise le vecteur et le multiplie par la vitesse de deplacement
            self.vector[0] = (self.vector[0]/self.norm)*self.speed
            self.vector[1] = (self.vector[1]/self.norm)*self.speed

    def setParent(self, parent :Place):
        """Permet de definir la parent d'un carte. (Pas utilisee, la fonction set Children a ete systematiquement
        utilisee car est disponible egalement pour les zones) ---USAGE DECONSEILLE !--- """
        if parent.children == None:
            parent.children = self
            self.parent = parent
            self.pos = parent.parent_pos.copy()
            self.place = self.pos.copy()
            self.updateRect()
            self.updateParent_pos()
            if isinstance(parent, Carte):
                parent.updateRect()
                parent.updateParent_pos()



    def setChildren(self, children : Place, zone = "norm"):
        """Permet de definir un enfant pour la carte courante"""

        #verifie si la carte cournte n'as pas deja un enfant
        if self.children == None:
            #verifie si l'enfant potentiel existe
            if children != None:
                #defini l'enfant potentiel comme l'enfant de la carte courrante
                self.children = children
                #si le nouvel enfant a un ancien parent
                if children.parent != None:
                    #le parent perd son enfant
                    children.parent.children = None
                    #si l'ancien parent est une carte, on actualise son rect
                    if isinstance(children.parent, Carte):
                        children.parent.updateRect()

                #on defini le nouveau parent de la carte
                children.parent = self
                #si l'enfant est sur une zones classique (pas zones d'as)
                if zone == "norm":
                    #l'enfant est place sur la parent_pos de son nouveau parent
                    children.pos = self.parent_pos.copy()
                    children.place = self.parent_pos.copy()
                #si l'enfant est sur une zone d'as
                else:
                    #il est placé directement sur la position de son parent
                    children.pos = self.pos.copy()
                    children.place = self.pos.copy()

                #on actualise le rect du nouveau parent (carte courrante) et de l'enfant
                children.updateRect()
                children.updateParent_pos()
                self.updateRect()
            else:
                self.children = None
                self.updateRect()



    def getBottomChildren(self):
        """Recupere le derier enfant d'une Place, renvoie None si la place courrante ne possede pas d'enfant"""
        children = self.children
        save = self.children
        while children != None:
            save = children
            children = children.children

        return save

    def getBottomParent(self):
        """Recupere le derier enfant d'une Place, renvoie None si la place courrante ne possede pas de parent"""
        parent = self.parent
        save = self.parent
        while parent != None:
            save = parent
            parent = parent.parent

        return save


    def getChildrenList(self):
        """Renvoie la liste de tous les enfants depuis la carte courante"""
        L = []
        children = self.children
        while children != None:
            L.append(children)
            children = children.children


        return L


    def goBack(self):
        """Fais avancer d'un increment la carte vers sa place dans le cas ou elle a etet lachee hors d'un place"""
        if self.norm > 1:
            self.pos[0] += self.vector[0]
            self.pos[1] += self.vector[1]
            self.norm -= self.speed
            self.updateRect()
            self.updateParent_pos()

        else:
            self.pos = self.place.copy()
            self.vector = np.array([0, 0])
            self.norm = 0
            self.updateRect()
            self.updateParent_pos()











