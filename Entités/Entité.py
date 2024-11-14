from typing_extensions import Self
import sys
from Maths.Vec2 import Vec2

class État:
    RECHERCHE = "recherche"
    COMBAT = "combat"
    DÉPLACEMENT = "déplacement"
    IMMOBILE = "immobile"

    v : str

    def __init__(self, valeur = Self.RECHERCHE):
        self.v = valeur

class ÉtatCombat:
    LIBRE = "libre"
    DÉFENSE = "défense"
    CHARGER = "charger"

    v : str

    def __init__(self, valeur = Self.LIBRE):
        self.v = valeur

class Attaque:

    def __init__(self):
        pass

class Entité:

    estVivant : bool

    état : État
    étatCombat : ÉtatCombat
    ennemi : Self
    pos : Vec2
    destination : Vec2

    chemin : list[Tuile] # TODO implémenter Tuiles

    def __init__(self):
        self.estVivant = True
        self.état = État()
        self.étatCombat = ÉtatCombat()
        self.ennemi = None
        self.pos = Vec2(0,0)
        self.destination = Vec2(0,0)
        pass

    def MiseÀJourIA(self):
        carte = Carte() # TODO implémenter carte
        if self.état.v == État.RECHERCHE:
            ennemiPlusPrès = None
            distanceMinimale = sys.float_info.max
            for ennemi in carte.ennemis:
                if distance(ennemi,self) < distanceMinimale:    # TODO implémenter distance entre entitées
                    ennemiPlusPrès = ennemi
                    distanceMinimale = distance(ennemi,self)
            if ennemiPlusPrès != None:
                self.état = État.DÉPLACEMENT
                self.destination = ennemi.pos
        
        if self.état.v == État.DÉPLACEMENT:
            faire_pathfinding = True
            if len(self.chemin) > 0:
                if carte.peutAller(self.chemin[0].pos):
                    self.pos = self.chemin[0].pos.copie()
                    faire_pathfinding = False

                    for ennemi in carte.ennemis:
                        if distance(ennemi, self) <= 1:
                            self.état.v = État.COMBAT
                            self.ennemi = ennemi
                            break
                    if self.ennemi == None and self.pos == self.destination:
                        self.état = État.RECHERCHE
                else:
                    self.chemin = []
                    faire_pathfinding = True

            if faire_pathfinding:
                self.chemin = self.A_étoile(carte, self.pos, self.destination)
        
        if self.état.v == État.COMBAT:
            if self.ennemi.estVivant and distance(self.ennemi, self) <= 1:
                self.AttaquerEnnemi()
            else:
                self.état.v = État.RECHERCHE


        pass
    
    def AttaquerEnnemi(self):
        pass    # TODO implémenter Entitié.AttaquerEnnemi()

    def Attaquer(self, attaque : Attaque):
        pass    # TODO implémenter Entitié.Attaquer()

    def Défense(self, attaque : Attaque):
        return attaque  # TODO implémenter Entitié.Défense()

    def A_étoile(self, carte : Carte, départ : Vec2, arrivé : Vec2):
        pass    # TODO implémenter Entitié.A_étoile()