import pygame
from pygame.locals import *
from Carte import Carte
from Zone import Zone
import random
from ZonePile import ZonePile

pygame.init()

fenetre = pygame.display.set_mode((1536, 780))


def boucle(fenetre):
    continuer = 1

    #nombre de carte que l'on pioche a chaque fois
    nb_pioche = 3

    #contien les cartes sur le plateau (pas celles de la pile)
    plateau = []


    couleurs = ["c", "d", "h", "s"]
    chiffres = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "D", "J", "Q", "K"]

    #tailles des cartes en pixel
    card_width = 69
    card_height = 94

    #generation de la zone de pile
    zpile = ZonePile((225, 155, 0), [200, 40], card_width, card_height)

    #generation des 52 cartes que l'on stocke dans zpile.cartes
    for c in couleurs:
        for num in chiffres:
            zpile.cartes.append(Carte(num + c, [zpile.pos[0], zpile.pos[1]]))

    #on melange le paquet de carte
    random.shuffle(zpile.cartes)

    #zones  = les zones ou les cartes sont placées eu début
    zones = []

    #zones_as sont les zones du dessus ou les as peuvent etre places
    zones_as = []

    #variable perettant de place corectement les zones
    startx = 346
    ofsetx = 60

    starty = 200
    ofsety = 30

    #generation des zone et remplissage de zones
    for i in range(7):
        zones.append(Zone((155, 155, 155), [startx + (ofsetx + 69) * i, starty], card_width, card_height))

    #generation des zones d'as et remplissage de zones_as
    for i in range(4):
        zones_as.append(Zone((155, 155, 155), [991 + (ofsetx + 69) * i, 40], card_width, card_height))



    #distribue les cartes sur les zones et stocke ces cartes distribués dans plateau
    #les cartes de plateau sont retirées de zpile.cartes
    plateau = debutPartie(zpile.cartes, zones)
    clock = pygame.time.Clock()


    #boucle de jeu
    while continuer:
        dt = clock.tick()
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = 0

            #gere les event de clic de carte
            dragCards(plateau,event,zones,zones_as,zpile,nb_pioche)
            clickPile(event,zpile,nb_pioche)

            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    continuer = 0
                    boucle(fenetre)
                    pygame.quit()
                    return
                if event.key == K_SPACE:
                    if nb_pioche == 1:
                        nb_pioche = 3
                    else:
                        nb_pioche = 1



        if dt%10 == 0:

            fenetre.fill((51,102,0))
            #dessin de la zone de pile en jaune ou les cartes sont pioches
            pygame.draw.rect(fenetre,zpile.color,zpile.rect,0,5)

            #affichage des cartes de la pile (retournee)
            for c in zpile.cartes:
                fenetre.blit(c.image,c.pos)





            #affiche les zones
            for z in zones:
                pygame.draw.rect(fenetre,z.color,z.rect,0,5)
                b = z.getBottomChildren()
                #revele la carte du bout de la pile si elle est cachee
                if b != None:
                    if b.hide:
                        z.getBottomChildren().reveal()

            #actualise le rect de la carte du dessus de zones_as
            for z in zones_as:
                c = z.getBottomChildren()
                if c != None:
                    c.updateRect()
                #affichage de zones_as
                pygame.draw.rect(fenetre,z.color,z.rect,0,5)

            for c in plateau:
                #affiche les cartes du plateau
                fenetre.blit(c.image,c.pos)
                #si la carte est lachee hors d'un amplacement on la fais revenir a sa place
                if c.norm != 0:
                    c.goBack()
                    c.updateRect()


            #la carte du haut de la pile est ramenee a sa place si lachee
            if len(zpile.pile) > 0:
                if zpile.pile[-1].norm != 0:
                    c = zpile.pile[-1]
                    c.goBack()
                    c.updateRect()

            #affiche les cartes de la pile (devoilees)
            for c in zpile.pile:
                fenetre.blit(c.image,c.pos)



        pygame.display.flip()



    pygame.quit()






def dragCards(plateau,event,zones,zones_as,zpile,nb = 3):
    """Fonction qui s'occupe du deplacage de carte lors d'un drag"""

    if event.type == MOUSEBUTTONDOWN:
        #si clique gauche sur une carte devoilee
        if event.button == 1:
            for c in plateau:
                if c.rect.collidepoint(event.pos):
                    if not c.hide:
                        #on initie sa variable drag a True, calcul du drag offset
                        c.drag = True
                        c.drag_offset = (c.pos[0]-event.pos[0], c.pos[1]-event.pos[1])
                        #place la carte au premier plan dans l'affichage
                        plateau.remove(c)
                        plateau.append(c)
                        L = c.getChildrenList()
                        #Place les enfants succesif de la carte au premier plan de l'affichage
                        for elem in L:
                            plateau.remove(elem)
                            plateau.append(elem)
                        break

            if len(zpile.pile) > 0:
                if zpile.pile[-1].rect.collidepoint(event.pos):
                    #initie le drag a True pour la carte du haut de la pile
                    c = zpile.pile[-1]
                    c.drag = True
                    c.drag_offset = (c.pos[0] - event.pos[0], c.pos[1] - event.pos[1])





    if event.type == MOUSEMOTION:
        if event.buttons[0] == 1:
            for c in plateau:
                if c.drag:
                    c.pos[0] = event.pos[0] + c.drag_offset[0]
                    c.pos[1] = event.pos[1] + c.drag_offset[1]
                    c.updateRect()
                    for elem in c.getChildrenList():
                        elem.pos = elem.parent.parent_pos.copy()
                        elem.parent_pos[0] = elem.pos[0]
                        elem.parent_pos[1] = elem.pos[1]+30

            if len(zpile.pile) > 0:
                if zpile.pile[-1].drag:
                    c = zpile.pile[-1]
                    c.pos[0] = event.pos[0] + c.drag_offset[0]
                    c.pos[1] = event.pos[1] + c.drag_offset[1]
                    c.updateRect()


    if event.type == MOUSEBUTTONUP:
        for c in plateau:
           if c.drag:
                moveCarte(c,zpile,zones,zones_as,plateau,nb)

        if len(zpile.pile) > 0:
            c = zpile.pile[-1]
            moveCarte(c,zpile,zones,zones_as,plateau,nb)



def moveCarte(c : Carte,zpile,zones,zones_as,plateau,nb):
    """Permet de déplacer une carte vers une nouvelle position que cette carte soit sur la plateau ou sur le dessus de la
     pile"""

    if c.drag:
        for z in zones:
            #verifie si la carte est bien sur une zone
            if z.rect.colliderect(c.move_rect):
                #si c'est un roi
                if c.nom[0] == 'K':
                    #on place l carte sur la zone
                    z.setChildren(c)
                    if c in zpile.pile:
                        zpile.pile.remove(c)
                        plateau.append(c)
                        zpile.actualise(nb)


        for z in zones_as:
            if c.children == None:
                # verifie si la carte est bien sur une zone_as
                if z.rect.colliderect(c.move_rect):
                    #si c'est un as
                    if c.nom[0] == '1':
                        #on place la carte sur l'emplacement
                        z.setChildren(c)
                        if c in zpile.pile:
                            zpile.pile.remove(c)
                            plateau.append(c)
                            zpile.actualise(nb)


        for ca in plateau:
            if ca != c:
                if c.move_rect.colliderect(ca.rect):
                    #si la carte est sur une autre carte, et qu'elle peut etre posée la, on la pose
                    if critereBouge(c,ca,zones,zones_as)[0]:
                        ca.setChildren(c,critereBouge(c,ca,zones,zones_as)[1])
                        if c in zpile.pile:
                            zpile.pile.remove(c)
                            plateau.append(c)
                            zpile.actualise(nb)

        c.drag = False
        c.findVector()



def clickPile(event, zpile : ZonePile, nb = 3):
    """Fonction qui gere l'evenement de click sur la pile pour piocher de nouvelles cartes"""
    if event.type == MOUSEBUTTONDOWN:
        if event.button == 1:
            #si clic gauche sur la zone de pile
            if zpile.rect.collidepoint(event.pos):
                #si la pile n'est pas vide, on pioche
                if len(zpile.cartes) > 0:
                    zpile.piocher(nb)
                #sinon on retourne la pile
                else:
                    zpile.retourner()




def debutPartie(paquet : list,zones):
    """Fonction permettant de distribuer les cartes sur les zone. Les cartes ajoutée sont stockées dans une variable
     plateau (retournee a la fin) et sont retires de zpile.cartes (ici paquet en argument) afin qu'elles ne puissent pas
     etre tires dans la pile"""
    plateau = []
    #on parcourt les zones
    for i in range(7):
        #distribution des cartes
        for j in range(i+1):
            c = paquet[0]
            paquet.remove(c)
            plateau.append(c)
            #placage des cartes dans les zones ou sur la derniere carte de la zone
            place = zones[j].getBottomChildren()

            #dans la zone
            if place == None:
                zones[j].setChildren(c)
            #sur la derniere carte de la zone
            else:
                place.setChildren(c)

    #on revele les dernieres cartes de chaque zone
    for z in zones:
        z.getBottomChildren().reveal()

    return plateau



def critereBouge(carte : Carte, parentTest : Carte, zones : list, zones_as : list):
    """Vérfie si la premiere carte passee en argument peut etre palcé sur la seconde"""


    chiffres = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "D", "J", "Q", "K"]
    zone = "norm" #correspond aux 7 septs zones classiques et non les zones d'as

    #stocke la couleur de la premier carte dans ca et celle de la deuxieme dans c2
    if carte.nom[1] == "c" or carte.nom[1] == "s": #carte noire
        c1 = "n"
    else:
        c1 = "r"

    if parentTest.nom[1] == "c" or parentTest.nom[1] == "s":
        c2 = "n"
    else:
        c2 = "r"

    #on verifie si le parent potentiel se trouve sur une zone ou une zones d'as
    if parentTest.getBottomParent() in zones:
        #on veut des couleurs differentes
        if c1 == c2:
            return False, zone
        #on veut que le parent potentiel n'est pas de carte deja attachee a lui
        if parentTest.children != None:
            return False,zone

        #on verifie si les deux cartes se suivent dans leur chiffres tel que Carte < Parent_potentiel
        c_p = parentTest.nom[0]
        i_p = chiffres.index(c_p)
        #rien sur l'as


        if i_p != 0:
            if chiffres[i_p-1] != carte.nom[0]:
                return False,zone

    #si le parent potentiel est dans la zone d'as
    elif parentTest.getBottomParent() in zones_as:
        zone = "as"
        #on veut des couleurs identiques
        if carte.nom[1] != parentTest.nom[1]:
            return False, zone
        #le parent potentiel ne doit pas avoir d'enfant
        if carte.children != None:
            return False,zone
        #il faut que les chiffre se suivent tel que Carte > Parent_potentiel
        c_p = parentTest.nom[0]
        i_p = chiffres.index(c_p)
        #rien sur le roi
        if i_p != 12:
            if chiffres[i_p+1] != carte.nom[0]:
                return False,zone

    return True,zone


boucle(fenetre)

