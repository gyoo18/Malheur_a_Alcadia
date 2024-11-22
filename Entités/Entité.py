from typing_extensions import Self
import sys
from Maths.Vec2 import *
from Carte.class_carte import Carte
from Entités.Attaque import Attaque

# État de l'IA
class ÉtatIA:
    RECHERCHE = "recherche" # Recherche une entitée ennemie
    COMBAT = "combat"       # Est en combat avec une entitée ennemie
    DÉPLACEMENT = "déplacement" # Se déplace vers une entitée ennemie
    DÉPLACEMENT_IMMOBILE = "déplacement_commande"
    IMMOBILE = "immobile"   # Est immobile en attente d'instructions

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
    vie : float     # Points de vies restants

    état : ÉtatIA = ÉtatIA()    # État de l'IA
    étatCombat : ÉtatCombat = ÉtatCombat()  # État de combat
    ennemi : Self = None    # Entitée ennemie avec laquelle on est en combat
    estAttaqué : bool = False
    pos : Vec2 = Vec2(0)    # Position actuelle
    destination : Vec2 = Vec2(0)    # Destination vers laquelle on se dirige

    TEMP_CHARGEMENT : int   # Temps nécessaire pour charger une attaque puissante
    chargement : int = 0    # Temps passé à charger l'attque puissante jusqu'à présent
    attaque_chargée : float # Dégats associés à l'attaque chargée

    dégats_défense : float  # Pourcentage de réduction des dégats en mode défense
    dégats_libre : float    # Pourcentage de réduction des dégats en mode libre
    dégats_charger : float  # Pourcentage de réduction des dégats en mode charger

    attaque_normale_dégats : int

    chemin : list[int] = [] # Liste des tuiles sur le chemin précalculé      # TODO implémenter Tuiles

    carte : Carte   # Référence à la carte jouée en ce moment

    def __init__(self, carte : Carte):
        self.dégats_défense = 0.5
        self.dégats_libre = 1.0
        self.dégats_charger = 1.5
        self.vie = 100.0
        self.TEMP_CHARGEMENT = 3
        self.attaque_chargée = 2.0
        self.attaque_normale_dégats = 1
        self.carte = carte
        pass

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
        #        |                  |       +--------------+ Oui    |  |           |            |
        #        |                  |       |Ennemi à porté|--+     |  |          Oui           |
        #        |                  |       |  d'attaque?  |---Non-----+           |            |
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
                self._modeDéplacementImmobile()
            case ÉtatIA.COMBAT:
                self._modeCombat()
            case ÉtatIA.IMMOBILE:
                self._modeImmobile()
    
    def _modeRecherche(self):
        # Obtenir une liste des ressources du jeu
        from Ressources import Ressources
        res = Ressources.avoirRessources()

        ennemiPlusPrès = None
        distanceMinimale = sys.float_info.max
        for ennemi in res.entités:
            if distance(ennemi.pos,self.pos) < distanceMinimale:
                ennemiPlusPrès = ennemi
                distanceMinimale = distance(ennemi.pos,self.pos)
        if ennemiPlusPrès != None:
            self.état.v = ÉtatIA.DÉPLACEMENT
            self.destination = ennemi.pos
    def _modeDéplacement(self):
        faire_pathfinding = True
        if len(self.chemin) > 0:
            if self.carte.peutAller(self.chemin[0].pos):
                self.pos = self.chemin[0].pos.copie()
                faire_pathfinding = False

                for ennemi in res.entités:
                    if distance(ennemi.pos, self.pos) <= 1:
                        self.état.v = ÉtatIA.COMBAT
                        self.ennemi = ennemi
                        break
                if self.ennemi == None and self.pos == self.destination:
                    self.état.v = ÉtatIA.RECHERCHE
            else:
                self.chemin = []
                faire_pathfinding = True

        if faire_pathfinding:
            self.chemin = self._A_étoile(self.carte, self.pos, self.destination)
    def _modeDéplacementImmobile(self):
        faire_pathfinding = True
        if len(self.chemin) > 0:
            if self.carte.peutAller(self.chemin[0].pos):
                self.pos = self.chemin[0].pos.copie()
                faire_pathfinding = False

                for ennemi in res.entités:
                    if distance(ennemi.pos, self.pos) <= 1:
                        self.état.v = ÉtatIA.COMBAT
                        self.ennemi = ennemi
                        break
                if self.ennemi == None and self.pos == self.destination:
                    self.état.v = ÉtatIA.IMMOBILE
            else:
                self.chemin = []
                faire_pathfinding = True

        if faire_pathfinding:
            self.chemin = self._A_étoile(self.carte, self.pos, self.destination)
    def _modeCombat(self):
        if self.ennemi.estVivant and distance(self.ennemi.pos, self.pos) <= 1:
            self._AttaquerEnnemi()
        else:
            self.état.v = ÉtatIA.RECHERCHE
            self.estAttaqué = False
    def _modeImmobile(self):
        if self.estAttaqué:
            self.état.v = ÉtatIA.COMBAT

    # Attaque l'ennemi qui est enregistré dans Entité.ennemi
    def _AttaquerEnnemi(self):
        attaque = Attaque(self)
        attaque.dégats = self.attaque_normale_dégats
        self.ennemi.Attaquer(attaque)

    # Fonction pour recevoir une attaque
    def Attaquer(self, attaque : Attaque):
        if not self.estAttaqué:
            self.estAttaqué = True
            self.ennemi = attaque.provenance
        
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