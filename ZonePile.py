import pygame
from Carte import Carte

class ZonePile():

    def __init__(self, color : tuple, pos: list, width, height):
        self.color = color
        self.pos = pos
        self.rect = pygame.Rect(self.pos[0], self.pos[1],width,height)
        self.cartes = []
        self.pile = []

    def piocher(self, nb = 3):
        """Methode qui permet de piocher nb cartes de la pile. Par defaut nb = 3"""

        pioche = [] #variable dans laquelle sont stockes les cartes piochees

        #retabli la position des cartes tires sur l'emplacement la plus a gauche
        for c in self.pile:
            c.pos = [300, 40]
            c.place = c.pos.copy()

        #si la le nombre de carte a piocher est inferieur au nombre de carte qu l'on peut piocher
        if len(self.cartes) >= nb:
            #la pile recupere les nb derniere carte la pioche
            for i in range(nb):
                self.pile.append(self.cartes[-(i+1)])
                pioche.append(self.cartes[-(i+1)])

        else:
            #sinon on pioche le reste des cartes
            for i in range(len(self.cartes)):
                c = self.cartes[-(i+1)]
                self.pile.append(c)
                pioche.append(c)
                c.pos = [300,40]
                c.place = c.pos.copy()

        #on retire les cartes piochees de la pioche et on les affiche
        for c in pioche:
            self.cartes.remove(c)
            c.reveal()

        #on actualise l'affichage de la pile
        self.actualise(nb)



    def actualise(self,nb):
        """Methode qui permet d'actualiserl'affichage de la pile"""

        #si il y a plus d'element dans la pile que que nombre de carte piochable
        if len(self.pile) >= nb:
            comp = 0
            #on place les nb dernieres carte de la piles de sortes a ce qu'elles soient superposée et que seule la derinere soit completement visible
            for i in range(len(self.pile) - nb, len(self.pile)):
                self.pile[i].pos[0] = 300 + (comp) * 13
                self.pile[i].place = self.pile[i].pos.copy()
                comp += 1
            #on actualise le rect de la carte du dessus la pile de sorte qu'elle puisse etre deplacee
            self.pile[-1].updateRect()
        else:
            #si il y a moisn d'element dans la pile ue de carte piochables
            if len(self.pile) != 0:
                #on place toutes les cates de la pile dans l'affichage
                for i in range(len(self.pile)):
                    self.pile[i].pos[0] = 300 + (i) * 13
                    self.pile[i].place = self.pile[i].pos.copy()
                self.pile[-1].updateRect()


    def retourner(self):
        """Methode appelee quand l'entierte des cartes de la pioche ont ete pioches. Les crtes de la pile sont alors
        remises dans la pioche dans le meme ordre que celle ou elle ont ete tires"""

        #on inverse la pile pour que la premire carte de la pile soit la premiere de la pioche
        self.pile.reverse()

        self.cartes = self.pile.copy()
        self.pile = []
        #on rempli la pioche de nouveau e on cache les carte de la pioche
        for c in self.cartes:
            c.pos = self.pos.copy()
            c.place = self.pos.copy()
            c.unreveal()


