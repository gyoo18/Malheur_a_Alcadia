from typing_extensions import Self
import sys
from Maths.Vec2 import Vec2
from Carte.class_carte import Carte

# État de l'IA
class ÉtatIA:
    RECHERCHE = "recherche" # Recherche une entitée ennemie
    COMBAT = "combat"       # Est en combat avec une entitée ennemie
    DÉPLACEMENT = "déplacement" # Se déplace vers une entitée ennemie
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

# Décrit une attaque et ses composantes
class Attaque:

    dégats : float # Dégats infligés à l'ennemi

    def __init__(self):
        self.dégats = 0

# Classe abstraite de base d'une entitée
class Entité:
    estVivant : bool = True
    vie : float     # Points de vies restants

    état : ÉtatIA = ÉtatIA()    # État de l'IA
    étatCombat : ÉtatCombat = ÉtatCombat()  # État de combat
    ennemi : Self = None    # Entitée ennemie avec laquelle on est en combat
    pos : Vec2 = Vec2(0)    # Position actuelle
    destination : Vec2 = Vec2(0)    # Destination vers laquelle on se dirige

    TEMP_CHARGEMENT : int   # Temps nécessaire pour charger une attaque puissante
    chargement : int = 0    # Temps passé à charger l'attque puissante jusqu'à présent
    attaque_chargée : float # Dégats associés à l'attaque chargée

    dégats_défense : float  # Pourcentage de réduction des dégats en mode défense
    dégats_libre : float    # Pourcentage de réduction des dégats en mode libre
    dégats_charger : float  # Pourcentage de réduction des dégats en mode charger

    chemin : list[int] = [] # Liste des tuiles sur le chemin précalculé      # TODO implémenter Tuiles

    carte : Carte   # Référence à la carte jouée en ce moment

    def __init__(self, carte : Carte):
        self.dégats_défense = 0.5
        self.dégats_libre = 1.0
        self.dégats_charger = 1.5
        self.vie = 100.0
        self.TEMP_CHARGEMENT = 3
        self.attaque_chargée = 2.0
        self.carte = carte
        pass

    # Mise à jour de l'IA de base
    def MiseÀJourIA(self):

        # Obtenir une liste des ressources du jeu
        from Ressources import Ressources
        res = Ressources.avoirRessources()

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
        if self.état.v == ÉtatIA.RECHERCHE:
            ennemiPlusPrès = None
            distanceMinimale = sys.float_info.max
            for ennemi in res.entités:
                if Vec2.distance(ennemi.pos,self.pos) < distanceMinimale:
                    ennemiPlusPrès = ennemi
                    distanceMinimale = Vec2.distance(ennemi.pos,self.pos)
            if ennemiPlusPrès != None:
                self.état.v = ÉtatIA.DÉPLACEMENT
                self.destination = ennemi.pos
        
        if self.état.v == ÉtatIA.DÉPLACEMENT:
            faire_pathfinding = True
            if len(self.chemin) > 0:
                if self.carte.peutAller(self.chemin[0].pos):
                    self.pos = self.chemin[0].pos.copie()
                    faire_pathfinding = False

                    for ennemi in res.entités:
                        if Vec2.distance(ennemi.pos, self.pos) <= 1:
                            self.état.v = ÉtatIA.COMBAT
                            self.ennemi = ennemi
                            break
                    if self.ennemi == None and self.pos == self.destination:
                        self.état.v = ÉtatIA.RECHERCHE
                else:
                    self.chemin = []
                    faire_pathfinding = True

            if faire_pathfinding:
                self.chemin = self.A_étoile(self.carte, self.pos, self.destination)
        
        if self.état.v == ÉtatIA.COMBAT:
            if self.ennemi.estVivant and distance(self.ennemi, self) <= 1:
                self.AttaquerEnnemi()
            else:
                self.état.v = ÉtatIA.RECHERCHE
    
    # Attaque l'ennemi qui est enregistré dans Entité.ennemi
    def AttaquerEnnemi(self):
        attaque = Attaque()
        attaque.dégats = 1.0
        self.ennemi.Attaquer(attaque)

    # Fonction pour recevoir une attaque
    def Attaquer(self, attaque : Attaque):
        attaque = self.Défense(attaque)
        self.vie -= attaque.dégats
        if self.vie <= 0.0:
            self.vie = 0.0
            self.estVivant = False

    # Fonction pour traiter le niveau de défense qui bloque l'attaque.
    def Défense(self, attaque : Attaque):
        match self.état.v:
            case ÉtatCombat.DÉFENSE:
                attaque.dégats *= self.dégats_défense
            case ÉtatCombat.LIBRE:
                attaque.dégats *= self.dégats_libre
            case ÉtatCombat.CHARGER:
                attaque.dégats *= self.dégats_charger
            case _:
                raise ValueError("Éntité.Défense() L'état de combat " + self.étatCombat.v + " n'est pas un état valide.")

        return attaque

    # Trouve le chemin le plus court entre le point A et B en utilisant A* et renvoie une liste des cases à prendre pour suivre le chemin
    def A_étoile(self, carte : Carte, départ : Vec2, arrivé : Vec2):
        return []   # TODO implémenter Entitié.A_étoile()