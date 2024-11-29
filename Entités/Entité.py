from __future__ import annotations
from typing_extensions import Self
import random
import sys
from Maths.Vec2 import *
from InclusionsCirculaires.Entité_Attaque import *
from InclusionsCirculaires.Entité_Carte import *

# État de l'IA
class ÉtatIA:
    RECHERCHE = "recherche" # Recherche une entitée ennemie
    COMBAT = "combat"       # Est en combat avec une entitée ennemie
    DÉPLACEMENT = "déplacement" # Se déplace vers une entitée ennemie
    DÉPLACEMENT_IMMOBILE = "déplacement immobile" # Se déplace après en avoir reçus l'ordre. Serat immobile par la suite.
    IMMOBILE = "immobile"   # Est immobile en attente d'instructions
    GUÉRISON = "guérison" # Est en processus de guérir un allié

    v : str

    def __init__(self, valeur = RECHERCHE):
        self.v = valeur

# État de combat
class ÉtatCombat:
    LIBRE = "libre" # N'est ni en défense, ni en train de charger une attaque
    DÉFENSE = "défense" # Est en mode défense, réduit les dégats des attaques, mais ne peut pas attaquer
    CHARGER = "charger" # Est en train de charger une attaque plus puissante, mais est vulnérable aux attaques

    v : str

    def __init__(self, valeur = LIBRE):
        self.v = valeur

# Classe abstraite de base d'une entitée
class Entité:
    estVivant : bool = True
    vieMax : int    # Points de vies maximum
    vie : float     # Points de vies restants

    état : ÉtatIA = ÉtatIA()    # État de l'IA
    étatCombat : ÉtatCombat = ÉtatCombat()  # État de combat
    cible : Self = None    # Entitée ennemie avec laquelle on est en combat ou entité allié que nous guérissons
    estAttaqué : bool = False
    pos : Vec2 = Vec2(0)    # Position actuelle
    destination : Vec2 = Vec2(0)    # Destination vers laquelle on se dirige
    direction : Vec2 = Vec2(0)      # Direction vers laquelle l'entité fait face

    TEMP_CHARGEMENT : int   # Temps nécessaire pour charger une attaque puissante
    chargement : int = 0    # Temps passé à charger l'attque puissante jusqu'à présent
    attaque_chargée : float # Dégats associés à l'attaque chargée

    dégats_défense : float  # Pourcentage de réduction des dégats en mode défense
    dégats_libre : float    # Pourcentage de réduction des dégats en mode libre
    dégats_charger : float  # Pourcentage de réduction des dégats en mode charger

    attaque_normale_dégats : int

    chemin : list[Vec2] = [] # Liste des tuiles sur le chemin précalculé

    carte : Carte = None  # Référence à la carte jouée en ce moment

    camp : str = ""                 # Dans quel camp se trouve cette entité?
    campsEnnemis : list[str] = []   # Liste des camps ennemis à cette entité.

    def __init__(self):
        self.dégats_défense = 0.5*self.dégats_libre
        self.dégats_libre = 1.0
        self.dégats_charger = 1.5*self.dégats_libre
        self.vieMax = 100
        self.vie = 100.0
        self.TEMP_CHARGEMENT = 3
        self.attaque_chargée = 2.0
        self.attaque_normale_dégats = 1

    def Random_Stats(x,y):
        Stats=int(random.choice(range(x,y)))
        return Stats
    
    def nom_aléatoire(liste):
        nom=random.choice(liste)
        return nom
        

    def MiseÀJour(self):
        self._MiseÀJourIA()
        
    # Mise à jour de l'IA de base
    def _MiseÀJourIA(self):
        # L'IA est basée sur une machine d'états
        # Diagramme de la machine :
        #                           |                               |                           |
        #       Mode Recherche      |       Mode Déplacement        |       Mode Combat         |
        #                           |                               |                           |
        #      +------------+   +------------->+---------+          |                           |
        #      |Recherche un|   |   |       +--|A chemin?|--+       |     +------------------+  |
        #      |   ennemi   |   |   |      Oui +---------+ Non      |  +->|Exécuter l'attaque|  |
        #      +------------+   |   |       |               |       |  |  +------------------+  |
        #        ↑   |          |   |       V               V       |  |      |        ↑        |
        #        | ennemi       |   |   +-------+     +-----------+ |  |      |       Non       |
        #        | trouvé       |   |   |Cherche|---->| Effectue  | |  |      V        |        |
        #        |   +----------+   |   |chemin |  +--|déplacement| |  |  +------------------+  |
        #        |                  |   +-------+  |  +-----------+ |  |  |Ennemi mort/parti?|  |
        #        |                  |              V          ↑     |  |  +------------------+  |
        #        |                  |       +--------------+ Non    |  |           |            |
        #        |                  |       |Ennemi à porté|--+     |  |          Oui           |
        #        |                  |       |  d'attaque?  |---Oui-----+           |            |
        #        |                  |       +--------------+        |              |            |
        #        +-----------------------------------------------------------------+            |
        #                           |                               |                           |
        #
        match self.état.v:
            case ÉtatIA.RECHERCHE:
                self._modeRecherche()
            case ÉtatIA.DÉPLACEMENT:
                self._modeDéplacement()
            case ÉtatIA.DÉPLACEMENT_IMMOBILE:
                self._modeDéplacement()
            case ÉtatIA.COMBAT:
                self._modeCombat()
            case ÉtatIA.IMMOBILE:
                self._modeImmobile()
            case ÉtatIA.GUÉRISON:
                self._modeGuérison()
    
    def _estEnnemi(self,ennemi : Self):
        return ennemi.camp in self.campsEnnemis

    def _modeRecherche(self):
        ennemiPlusPrès = None
        distanceMinimale = sys.float_info.max
        for ennemi in self.carte.entités:
            if distance(ennemi.pos,self.pos) < distanceMinimale and self._estEnnemi(ennemi):
                ennemiPlusPrès = ennemi
                distanceMinimale = distance(ennemi.pos,self.pos)
        if ennemiPlusPrès != None:
            self.état.v = ÉtatIA.DÉPLACEMENT
            self.destination = ennemiPlusPrès.pos
    def _modeDéplacement(self):
        faire_pathfinding = True
        if len(self.chemin) > 0:
            if self.carte.peutAller(self.chemin[0].pos):
                self.direction = self.chemin[0].pos - self.pos
                self.pos = self.chemin[0].pos.copie()
                faire_pathfinding = False

                for ennemi in self.carte.entités:
                    if distance(ennemi.pos, self.pos) <= 1 and ennemi.camp in self.campsEnnemis:
                        self.état.v = ÉtatIA.COMBAT
                        self.cible = ennemi
                        break
                if self.cible == None and self.pos == self.destination and self.état.v == ÉtatIA.DÉPLACEMENT:
                    self.état.v = ÉtatIA.RECHERCHE
                elif self.cible == None and self.pos == self.destination and self.état.v == ÉtatIA.DÉPLACEMENT_IMMOBILE:
                    self.état.v = ÉtatIA.IMMOBILE
            else:
                self.chemin = []
                faire_pathfinding = True

        if faire_pathfinding:
            self.chemin = self._A_étoile()
    def _modeCombat(self):
        if self.cible.estVivant and distance(self.cible.pos, self.pos) <= 1:
            self._AttaquerEnnemi()
        else:
            self.état.v = ÉtatIA.RECHERCHE
            self.estAttaqué = False
            self.cible = None
    def _modeImmobile(self):
        if self.estAttaqué:
            self.état.v = ÉtatIA.COMBAT
    def _modeGuérison(self):
        pass

    # Attaque l'ennemi qui est enregistré dans Entité.ennemi
    def _AttaquerEnnemi(self):
        from Entités.Attaque import Attaque
        attaque = Attaque(self)
        attaque.dégats = self.attaque_normale_dégats
        self.cible.Attaquer(attaque)

    # Fonction pour recevoir une attaque
    def Attaquer(self, attaque : Attaque):
        if not self.estAttaqué:
            self.estAttaqué = True
            self.cible = attaque.provenance
        
        attaque = self._Défense(attaque)
        self.vie -= attaque.dégats
        if self.vie <= 0.0:
            self.vie = 0.0
            self.estVivant = False

    # Fonction pour traiter le niveau de défense qui bloque l'attaque.
    def _Défense(self, attaque : Attaque):
        match self.état.v:
            case ÉtatCombat.DÉFENSE:
                attaque.dégats -= attaque.dégats*(self.dégats_défense/100)
            case ÉtatCombat.LIBRE:
                attaque.dégats *= attaque.dégats*(self.dégats_libre/100)
            case ÉtatCombat.CHARGER:
                attaque.dégats *= attaque.dégats*(self.dégats_défense/100)
            case _:
                raise ValueError("Éntité.Défense() L'état de combat " + self.étatCombat.v + " n'est pas un état valide.")

        return attaque

    def naviguerVers(self, destination : Vec2):
        self.destination = destination
        self.chemin = self._A_étoile()

    # Trouve le chemin le plus court entre le point A et B en utilisant A* et renvoie une liste des cases à prendre pour suivre le chemin
    def _A_étoile(self):
        return []   # TODO implémenter Entitié.A_étoile()