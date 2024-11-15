from typing_extensions import Self
import sys
from Maths.Vec2 import Vec2
from class_carte import Carte

class État:
    RECHERCHE = "recherche"
    COMBAT = "combat"
    DÉPLACEMENT = "déplacement"
    IMMOBILE = "immobile"

    v : str

    def __init__(self, valeur = RECHERCHE):
        self.v = valeur

class ÉtatCombat:
    LIBRE = "libre"
    DÉFENSE = "défense"
    CHARGER = "charger"

    v : str

    def __init__(self, valeur = LIBRE):
        self.v = valeur

class Attaque:

    dégats : float

    def __init__(self):
        self.dégats = 0

class Entité:

    estVivant : bool
    vie : float

    état : État
    étatCombat : ÉtatCombat
    ennemi : Self
    pos : Vec2
    destination : Vec2

    dégats_défense : float
    dégats_libre : float
    dégats_charger : float

    chemin : list[Tuile] # TODO implémenter Tuiles

    def __init__(self):
        self.estVivant = True
        self.état = État()
        self.étatCombat = ÉtatCombat()
        self.ennemi = None
        self.pos = Vec2(0,0)
        self.destination = Vec2(0,0)
        self.dégats_défense = 0.5
        self.dégats_libre = 1.0
        self.dégats_charger = 1.5
        self.vie = 100.0
        pass

    def MiseÀJourIA(self):
        carte = Carte()
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
        attaque = Attaque()
        attaque.dégats = 1.0
        self.ennemi.Attaquer(attaque)

    def Attaquer(self, attaque : Attaque):
        attaque = self.Défense(attaque)
        self.vie -= attaque.dégats
        if self.vie <= 0.0:
            self.vie = 0.0
            self.estVivant = False

    def Défense(self, attaque : Attaque):
        match self.état.v:
            case ÉtatCombat.DÉFENSE:
                attaque.dégats *= self.dégats_défense
            case ÉtatCombat.LIBRE:
                attaque.dégats *= self.dégats_libre
            case ÉtatCombat.CHARGER:
                attaque.dégats *= self.dégats_charger
            case _:
                raise ValueError("[Éntité.Défense()] L'état de combat " + self.étatCombat.v + " n'est pas un état valide.")

        return attaque

    def A_étoile(self, carte : Carte, départ : Vec2, arrivé : Vec2):
        pass    # TODO implémenter Entitié.A_étoile()