from __future__ import annotations
from typing_extensions import Self
import random
import sys
from Maths.Vec2 import *
from InclusionsCirculaires.Entité_Attaque import *
from InclusionsCirculaires.Entité_Carte import *
from copy import deepcopy
from TFX import *

# État de l'IA
class ÉtatIA:
    RECHERCHE = "recherche" # Recherche une entitée ennemie
    COMBAT = "combat"       # Est en combat avec une entitée ennemie
    DÉPLACEMENT = "déplacement" # Se déplace vers une entitée ennemie
    DÉPLACEMENT_IMMOBILE = "déplacement immobile" # Se déplace après en avoir reçus l'ordre. Serat immobile par la suite.
    IMMOBILE = "immobile"   # Est immobile en attente d'instructions
    GUÉRISON = "guérison" # Est en processus de guérir un allié

    def __init__(self, valeur = RECHERCHE):
        self.v : str = valeur

# État de combat
class ÉtatCombat:
    LIBRE = "libre" # N'est ni en défense, ni en train de charger une attaque
    DÉFENSE = "défense" # Est en mode défense, réduit les dégats des attaques, mais ne peut pas attaquer
    CHARGER = "charger" # Est en train de charger une attaque plus puissante, mais est vulnérable aux attaques

    def __init__(self, valeur = LIBRE):
        self.v : str = valeur

# Classe abstraite de base d'une entitée
class Entité:

    CAMP_PAYSANS = "Monstres"
    CAMP_GOLEMS = "Golems"
    CAMP_JOUEUR = "Mélios"
    CAMP_PERSONNAGES = "Personnages"

    def __init__(self):
        # Charactérisitques décrivant l'entité
        self.PVMax : int = 100         # Points de vies maximum
        self.PV : float = self.PVMax  # Points de vies restants

        self.TEMP_CHARGEMENT : int = 3      # Temps nécessaire pour charger une attaque puissante
        self.attaque_chargée : float = 30.0 # Dégats associés à l'attaque chargée

        self.dégats_défense : float = 30.0  # Pourcentage de réduction des dégats en mode défense
        self.dégats_libre : float = 10.0    # Pourcentage de réduction des dégats en mode libre
        self.dégats_charger : float = 0.0   # Pourcentage de réduction des dégats en mode charger  

        self.attaque_normale_dégats : int = 10.0

        self.camp : str = ""                 # Dans quel camp se trouve cette entité?
        self.campsEnnemis : list[str] = []   # Liste des camps ennemis à cette entité.

        self.nom : str = "Entité"

        # Variables de fonctionnement 
        self.animID = ""
        self.estVivant : bool = True

        self.état : ÉtatIA = ÉtatIA()    # État de l'IA
        self.étatCombat : ÉtatCombat = ÉtatCombat()  # État de combat
        self.cible : Self = None    # Entitée ennemie avec laquelle on est en combat ou entité allié que nous guérissons
        self.estAttaqué : bool = False
        self.chargement : int = 0    # Temps passé à charger l'attque puissante jusqu'à présent

        self.pos : Vec2 = Vec2(0)   # Position actuelle
        self.destination : Vec2 = Vec2(0)  # Destination vers laquelle on se dirige
        self.direction : Vec2 = Vec2(0)    # Direction vers laquelle l'entité fait face

        self.chemin : list[Vec2] = []  # Liste des tuiles sur le chemin précalculé
        self.carte : Carte = None  # Référence à la carte jouée en ce moment

        noms = ["Jean", "Salom", "Guy", "Pascal", "Eva"]

        # Appel de la fonction avec la liste de noms
        self.nom = Entité.nom_aléatoire(noms)

    def avoirInfoStr(self):
        # TODO #16 implémenter avoirInfoStr() dur toutes les entitées
        return (gras(soul(self.nom.capitalize())) + '\n' +
                gras("PV")+"      : " + str(int(self.PV)) + '\n' +
                gras("PVMax")+"   : " + str(int(self.PVMax)) + '\n' +
                gras("Attaque")+" : " + str(int(self.attaque_normale_dégats)) + '\n' +
                gras("Défense")+" : " + str(int(self.dégats_libre)) + '\n')

    def Random_Stats(self,x,y):
        Stats=int(random.choice(range(x,y)))
        return Stats
    
    def nom_aléatoire(liste):
        if len(liste) == 0:
            print(coul("Aucun nom n'est disponible. Génération aléatoire de nom.",ROUGE))
            cons = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','z']
            voy = ['a','e','i','o','u','y']
            nom = random.choice(cons).upper() + random.choice(voy) + random.choice(cons)
            return nom
        nom=liste.pop(random.randrange(0,len(liste)))
        return nom

    def MiseÀJour(self):
        from Jeu import Jeu,ÉtatJeu
        jeu = Jeu.avoirJeu()
        if jeu.état.v == ÉtatJeu.FIN_TOUR or jeu.état.v == ÉtatJeu.JEU:
            self._MiseÀJourIA()
        elif jeu.état.v in [ÉtatJeu.DÉBUT,ÉtatJeu.SUCCÈS,ÉtatJeu.ÉCHEC,ÉtatJeu.SCÈNE]:
            personnages : list[str] = None
            personnages_positions : list[Vec2] = None
            if self.carte.estScène:
                personnages = self.carte.séquences.plans[jeu.état.scène_étape].personnages[jeu.état.scène_animation_étape]
                personnages_positions = self.carte.séquences.plans[jeu.état.scène_étape].personnages_positions[jeu.état.scène_animation_étape]
            else:
                personnages = self.carte.séquences[jeu.état.v].plans[jeu.état.scène_étape].personnages[jeu.état.scène_animation_étape]
                personnages_positions = self.carte.séquences[jeu.état.v].plans[jeu.état.scène_étape].personnages_positions[jeu.état.scène_animation_étape]

            for i in range(len(personnages)):
                if personnages[i] == self.animID:
                    self.pos = personnages_positions[i]
        
    # Mise à jour de l'IA de base
    def _MiseÀJourIA(self):
        # L'IA est basée sur une machine d'états
        # Diagramme de la machine : TODO #31 Refaire le diagramme de la machine d'état des entités
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
        # L'algorithme fonctionne sur une base de fonctions, pour faciliter la spécialisation dans les classes enfants
        print("\nMise à jour de l'IA de " + gras(self.nom) + ", état : " + gras(self.état.v))
        match self.état.v:
            case ÉtatIA.RECHERCHE:
                print("Mode recherche activé.")
                self._modeRecherche()
            case ÉtatIA.DÉPLACEMENT:
                print("Mode déplacement activé")
                self._modeDéplacement()
            case ÉtatIA.DÉPLACEMENT_IMMOBILE:
                print("Mode déplacement immobile activé")
                self._modeDéplacement()
            case ÉtatIA.COMBAT:
                print("Mode combat activé")
                self._modeCombat()
            case ÉtatIA.IMMOBILE:
                print("Mode immobile activé")
                self._modeImmobile()
            case ÉtatIA.GUÉRISON:
                print("Mode guérison activé")
                self._modeGuérison()
    
    def _estEnnemi(self,ennemi : Self):
        """_estEnnemi Détermine si `ennemi` est un ennemi à `self`

        Est déterminé par le string Entité.camp et la liste Entité.campsEnnemis. 
        Si ennemi.camp se trouve dans self.campsEnnemis, retourne vrai, sinon faux.

        Args:
            ennemi (Self): entité dont on veut évaluer l'allégeance.

        Returns:
            bool: `ennemi` est-il un ennemi à self?
        """
        return ennemi.camp in self.campsEnnemis

    def _modeRecherche(self):
        """_modeRecherche Recherche un ennemi à poursuivre

        Sélectionne l'ennemi le plus proche comme cible et vire à l'état ÉtatIA.DÉPLACEMENT, vers la cible.
        """

        # Passe à travers tout les ennemis, si l'ennemi évalué est plus près que le plus près trouvé jusqu'à présent,
        #   il est l'ennemi le plus près, jusqu'à nouvel ordre

        print("Recherche d'ennemi")
        ennemiPlusPrès = None   # Ennemi le plus près
        distanceMinimale = sys.float_info.max   # Distance à laquelle se trouve l'ennemi trouvé le plus près

        for ennemi in self.carte.entités:
            # S'il est plus près et que c'est un ennemi
            if Vec2.distance(ennemi.pos,self.pos) < distanceMinimale and self._estEnnemi(ennemi):
                # En faire l'ennemi le plus près
                ennemiPlusPrès = ennemi
                distanceMinimale = Vec2.distance(ennemi.pos,self.pos)
        # Si on a trouvé un ennemi le plus près
        if ennemiPlusPrès != None:
            print("Ennemi trouvé : " + gras(ennemiPlusPrès.nom) + " à " + str(ennemiPlusPrès.pos.x) + ":" + str(ennemiPlusPrès.pos.y))
            # Se mettre en mode déplacement vers l'ennemi
            self.état.v = ÉtatIA.DÉPLACEMENT
            self.destination = ennemiPlusPrès.pos
            self.cible = ennemiPlusPrès
    
    def _modeDéplacement(self):
        """ Se déplace vers la cible sélectionnée

        Calcule un chemin vers la cible et s'y déplace. Vire vers le mode combat s'il est attaqué en chemin ou trouve la cible au bout du chemin
        et vire vers le mode recherche si on ne trouve pas la cible au bout du chemin.
        """
        # Si un ennemi se trouve sur une case adjascente, virer en mode combat
        for ennemi in self.carte.entités:
            # Chercher un ennemi à une distance de 1 ou moins de nous (sur une case adjascente)
            if Vec2.distance(ennemi.pos, self.pos) <= 1 and (ennemi.camp in self.campsEnnemis or ennemi == self.cible):
                print("Un ennemi est à proximité! Mode combat activé.")
                self.chemin = []
                self.état.v = ÉtatIA.COMBAT
                self.cible = ennemi
                return
            
        if self.état.v == ÉtatIA.DÉPLACEMENT:
            if self.cible.estVivant :
                print("Recherche d'un chemin vers " + self.cible.nom)
                self.naviguerVers(self.cible.pos,True)
            else:
                print("La cible est morte. À la recherche d'un nouvel ennemi")
                self.état.v = ÉtatIA.RECHERCHE
        elif self.état.v == ÉtatIA.DÉPLACEMENT_IMMOBILE:
            print("Recherche d'un chemin vers " + str(self.destination.x) + ';' + str(self.destination.y))
            self.naviguerVers(self.destination,False)

        # Si on n'a pas atteint le bout du chemin
        if len(self.chemin) > 0:
            print("Un chemin existe, avançons")
            # Avancer sur le chemin
            self.direction = self.chemin[0] - self.pos
            self.pos = self.chemin.pop(0)

            # Si un ennemi se trouve sur une case adjascente, virer en mode combat
            for ennemi in self.carte.entités:
                # Chercher un ennemi à une distance de 1 ou moins de nous (sur une case adjascente)
                if Vec2.distance(ennemi.pos, self.pos) <= 1 and (ennemi.camp in self.campsEnnemis or ennemi == self.cible):
                    print("Un ennemi est à proximité! Mode combat activé.")
                    self.chemin = []
                    self.état.v = ÉtatIA.COMBAT
                    self.cible = ennemi
                    return
            # Si on n'a pas trouvé d'ennemi, mais qu'on est arrivé au bout du chemin,
            if self.pos == self.destination and self.état.v == ÉtatIA.COMBAT:
                print("Arrivé à destination. Aucun ennemi à l'horison, Mode recherche activé.")
                # Chercher un autre ennemi si on est dans la boucle normale,
                # Rester immobile si on se déplace à cause d'une commande
                if self.état.v == ÉtatIA.DÉPLACEMENT:
                    self.état.v = ÉtatIA.RECHERCHE
                elif self.état.v == ÉtatIA.DÉPLACEMENT_IMMOBILE:
                    self.état.v = ÉtatIA.IMMOBILE

    def _modeCombat(self):
        """_modeCombat Exécute le combat

        Vire en mode recherche si l'ennemi est mort ou partis.
        """
        if self.cible.estVivant and Vec2.distance(self.cible.pos, self.pos) <= 1:
            print("Attaque de l'ennemi")
            self._AttaquerCible()
        else:
            print("L'ennemi est soit mort, soit partis. À la recherche d'un nouvel ennemi.")
            self.état.v = ÉtatIA.RECHERCHE
            self.estAttaqué = False
            self.cible = None

    def _modeImmobile(self):
        """_modeImmobile Rest immobile à la suite d'un déplacement dûs à une commande

        Vire en mode combat s'il reçoit une attaque
        """
        if self.estAttaqué:
            print("Je suis attaqué! Mode combat activé.")
            self.état.v = ÉtatIA.COMBAT

    def _modeGuérison(self):
        """ Guérit un allié

        Un allié estune entité dans le même camp (Entité.camp)
        **Non implémenté**
        """
        pass

    def _AttaquerCible(self):
        """_AttaquerEnnemi Attaque la cible enregistré dans Entité.cible

        Appelle self.cible.Attaquer(). Appelé durant le combat.
        """
        from Entités.Attaque import Attaque
        print("Attaque de base.")
        # Attaque de base
        attaque = Attaque(self)
        attaque.dégats = self.attaque_normale_dégats
        self.cible.Attaquer(attaque)

    def Attaquer(self, attaque : Attaque):
        """Attaquer Fonction pour recevoir une attaque

        Prend une Attaque en argument. Active l'indice self.estAttaqué et fait virer au mode combat.

        Args:
            attaque (Attaque): Un objet Attaque qui contient les informations nécessaires pour subir une attaque.
        """
        print(TFX(self.nom,gras=True,Pcoul=ORANGE) + TFX(" reçoit une attaque de ",Pcoul=ORANGE) + TFX(attaque.provenance.nom,gras=True,Pcoul=ORANGE))
        print(gras(self.nom) + " a " + str(self.PV) + " PV, l'attaque fait " + str(attaque.dégats) + " PD")
        # Virer au mode combat, si on n'y est pas déjà
        if not self.estAttaqué:
            print(gras(self.nom) + " passe en mode combat.")
            self.estAttaqué = True
            self.cible = attaque.provenance
    
        attaque = self._Défense(attaque)    # Évaluer la défense
        self.PV -= attaque.dégats          # Retirer les points de vies
        # Évaluer si on est morts
        if self.PV <= 0.0:
            print(TFX(self.nom,gras=True,Pcoul=ROUGE) + TFX(" est mort.",Pcoul=ROUGE))
            self.PV = 0.0
            self.estVivant = False

    def _Défense(self, attaque : Attaque):
        """ Réduit les points d'attaques en fonction des points de défenses.

        Cette fonction est dépendante de trois variables:
         - `dégats_défense` Pourcentage des dégats retirés en mode défense
         - `dégats_libre` Pourcentage des dégats retirés en mode libre
         - `dégats_charger` Pourcentage des dégats retirés en mode charger

        Raises:
            ValueError: Renvoie une erreure si self.étatCombat n'est pas l'un des suivants:
             - DÉFENSE
             - LIBRE
             - CHARGER

        Returns:
            Attaque : Attaque après défense
        """
        match self.étatCombat.v:
            case ÉtatCombat.DÉFENSE:
                print(gras(self.nom) + " bloque " + str(self.dégats_défense) + f"% des dégats.")
                attaque.dégats -= attaque.dégats*(self.dégats_défense/100)
            case ÉtatCombat.LIBRE:
                print(gras(self.nom) + " bloque " + str(self.dégats_libre) + f"% des dégats.")
                attaque.dégats -= attaque.dégats*(self.dégats_libre/100)
            case ÉtatCombat.CHARGER:
                print(gras(self.nom) + " bloque " + str(self.dégats_charger) + f"% des dégats.")
                attaque.dégats -= attaque.dégats*(self.dégats_charger/100)
            case _:
                raise ValueError("Éntité.Défense() L'état de combat " + self.étatCombat.v + " n'est pas un état valide.")
        
        print("L'attaque fait " + str(attaque.dégats) + " PD")

        return attaque

    def naviguerVers(self, destination : Vec2, destination_adjascente = False):
        """naviguerVers fait naviguer l'Entité vers `destination`

        **ATTENTION pour créer une commande `DÉPLACEMENT`, assurez-vous de modifier l'état à `DÉPLACEMENT_IMMOBILE`**
        
        Utilise A* pour calculer le chemin

        Args:
            destination (Vec2): Position de la destination voulue
        """
        print("Navigue vers : (" + str(destination.x) + ';' + str(destination.y) + ')')
        if self.état.v != ÉtatIA.DÉPLACEMENT and self.état.v != ÉtatIA.DÉPLACEMENT_IMMOBILE:
            self.état.v = ÉtatIA.DÉPLACEMENT
        self.destination = destination
        self.chemin = self._A_étoile(self.destination,destination_adjascente)

    # Trouve le chemin le plus court entre le point A et B en utilisant A* et renvoie une liste des cases à prendre pour suivre le chemin
    def _A_étoile(self, destination : Vec2, destination_adjascente : bool):
        """ Algorithme A* pour trouver le chemin le plus court sur la carte

        Utilise `self.carte` et `self.destination` **modifier avant d'appeler**

        Raises:
            RuntimeError: 

        Returns:
            list[Vec2]: liste de positions représentant un chemin à suivre.
        """
        # Si on se trouve déjà à la destination, le chemin est nul
        if self.pos == destination:
            return []
        """
        . Algorithme A* :
        .                       
        . +---+---+---+---+     1. Sélectionner la case avec le noeud le plus petit (il devient alors le curseur)
        . | 9 |10 |11 | D |     2. Vérifier si le curseur est la destination
        . +---+---+---+---+     Oui : 3. Renvoyer le chemin lié au curseur 
        . | # | 8 | # | # |     Non :|3. Ajouter tout les noeuds aux noeuds actifs
        . +---+---+---+---+          |4. Mettre le curseur dans les noeuds passifs
        . | 4 | 5 | 6 | 7 |     
        . +---+---+---+---+     Poid = longueure du chemin + distance avec la destination
        . | P | 1 | 2 | 3 |     
        . +---+---+---+---+     
        . 
        .1. NA = Noeuds Actifs, P = Poids, NP = Noeuds Passifs  |2.                                                     |3.                                                     |
        . +---+---+---+---+     NA : [   P]                     | +---+---+---+---+     NA : [  1,  4]                  | +---+---+---+---+     NA : [  4,  2,  5]              |
        . | 0 | 0 | 0 | 0 |     P  : [5.24]                     | | 0 | 0 | 0 | 0 |     P  : [4.6,4.6]                  | | 0 | 0 | 0 | 0 |     P  : [4.6,5.2,4.8]              |
        . +---+---+---+---+     NP : []                         | +---+---+---+---+     NP : [P]                        | +---+---+---+---+     NP : [P,1]                      |
        . | # | 0 | # | # |     curseur = P                     | | # | 0 | # | # |     curseur = 1                     | | # | 0 | # | # |     curseur = 4                     |
        . +---+---+---+---+                                     | +---+---+---+---+                                     | +---+---+---+---+                                     |
        . |4.6| 0 | 0 | 0 |     NA : [  1,  4]                  | |4.6|4.8| 0 | 0 |     NA : [  4,  2,  5]              | | 4 |4.8| 0 | 0 |     NA : [  2,  5]                  |
        . +---+---+---+---+     P  : [4.6,4.6]                  | +---+---+---+---+     P  : [4.6,5.2,4.8]              | +-|-+---+---+---+     P  : [5.2,4.8]                  |
        . | P |4.6| 0 | 0 |     NP : [P]                        | | P---1 |5.2| 0 |     NP : [P,1]                      | | P | 1 |5.2| 0 |     NP : [P,1,4]                    |
        . +---+---+---+---+                                     | +---+---+---+---+                                     | +---+---+---+---+                                     |
        .=======================================================+=======================================================+=======================================================+
        .4.                                                     |5.                                                     |6.                                                     |
        . +---+---+---+---+     NA : [  2,  5]                  | +---+---+---+---+     NA : [  2,  6,  8]              | +---+---+---+---+     NA : [  6,  8,  3]              |
        . | 0 | 0 | 0 | 0 |     P  : [5.2,4.8]                  | | 0 | 0 | 0 | 0 |     P  : [5.2,5.2,5.2]              | | 0 | 0 | 0 | 0 |     P  : [5.2,5.2,6.0]              |
        . +---+---+---+---+     NP : [P,1,4]                    | +---+---+---+---+     NP : [P,1,4,5]                  | +---+---+---+---+     NP : [P,1,4,5,2]                |
        . | # |5.2| # | # |     curseur = 5                     | | # |5.2| # | # |     curseur = 2                     | | # |5.2| # | # |     curseur = 6                     |
        . +---+---+---+---+                                     | +---+---+---+---+                                     | +---+---+---+---+                                     |
        . | 4 | 5 |5.2| 0 |     NA : [  2,  6,  8]              | | 4 | 5 |5.2| 0 |     NA : [  6,  8,  3]              | | 4 | 5---6 |6.0|     NA : [  8,  3,  7]              |
        . +---+-|-+---+---+     P  : [5.2,5.2,5.2]              | +---+---+---+---+     P  : [5.2,5.2,6.0]              | +---+-|-+---+---+     P  : [5.2,6.0,6.0]              |
        . | P---1 |5.2| 0 |     NP : [P,1,4,5]                  | | P---1---2 |6.0|     NP : [P,1,4,5,2]                | | P---1 | 2 |6.0|     NP : [P,1,4,5,2,6]              |
        . +---+---+---+---+                                     | +---+---+---+---+                                     | +---+---+---+---+                                     |
        .=======================================================+=======================================================+=======================================================+
        .7.                                                     |8.                                                     |9.                                                     |
        . +---+---+---+---+     NA : [  8,  3,  7]              | +---+---+---+---+     NA : [  3,  7, 10]              | +---+---+---+---+     NA : [  7, 10]                  |
        . | 0 |6.0| 0 | 0 |     P  : [5.2,6.0,6.0]              | | 0 |6.0| 0 | 0 |     P  : [6.0,6.0,6.0]              | | 0 |6.0| 0 | 0 |     P  : [6.0,6.0]                  |
        . +---+---+---+---+     NP : [P,1,4,5,2,6]              | +---+---+---+---+     NP : [P,1,4,5,2,6,8]            | +---+---+---+---+     NP : [P,1,4,5,2,6,8,4]          |
        . | # | 8 | # | # |     curseur = 8                     | | # | 8 | # | # |     curseur = 4                     | | # | 8 | # | # |     curseur = 7                     |
        . +---+-|-+---+---+                                     | +---+---+---+---+                                     | +---+---+---+---+                                     |
        . | 4 | 5 | 6 |6.0|     NA : [  3,  7, 10]              | | 4 | 5 | 6 |6.0|     NA : [  7, 10]                  | | 4 | 5---6---7 |     NA : [ 10]                      |
        . +---+-|-+---+---+     P  : [6.0,6.0,6.0]              | +---+---+---+---+     P  : [6.0,6.0]                  | +---+-|-+---+---+     P  : [6.0]                      |
        . | P---1 | 2 |6.0|     NP : [P,1,4,5,2,6,8]            | | P---1---2---4 |     NP : [P,1,4,5,2,6,8,4]          | | P---1 | 2 | 4 |     NP : [P,1,4,5,2,6,8,7]          |
        . +---+---+---+---+                                     | +---+---+---+---+                                     | +---+---+---+---+                                     |
        .=======================================================+=======================================================+=======================================================+
        .10.                                                    |11.                                                    |12.                                                    |
        . +---+---+---+---+     NA : [  7, 10]                  | +---+---+---+---+     NA : [ 10]                      | +---+---+---+---+     NA : [  9, 11]                  |
        . | 0 |6.0| 0 | 0 |     P  : [6.0,6.0]                  | |8.0|10 |6.0| 0 |     P  : [6.0]                      | |8.0|10--11 |6.0|     P  : [8.0,6.0]                  |
        . +---+---+---+---+     NP : [P,1,4,5,2,6,8,4]          | +---+-|-+---+---+     NP : [P,1,4,5,2,6,8,7]          | +---+-|-+---+---+     NP : [P,1,4,5,2,6,8,4,10]       |
        . | # | 8 | # | # |     curseur = 7                     | | # | 8 | # | # |     curseur = 10                    | | # | 8 | # | # |     curseur = 11                    |
        . +---+---+---+---+                                     | +---+-|-+---+---+                                     | +---+-|-+---+---+                                     |
        . | 4 | 5---6---7 |     NA : [ 10]                      | | 4 | 5 | 6 |6.0|     NA : [  9, 11]                  | | 4 | 5 | 6 |6.0|     NA : [  9,  X]                  |
        . +---+-|-+---+---+     P  : [6.0]                      | +---+-|-+---+---+     P  : [8.0,6.0]                  | +---+-|-+---+---+     P  : [8.0,6.0]                  |
        . | P---1 | 2 | 4 |     NP : [P,1,4,5,2,6,8,7]          | | P---1 | 2 | 4 |     NP : [P,1,4,5,2,6,8,4,10]       | | P---1 | 2 | 4 |     NP : [P,1,4,5,2,6,8,4,10,11]    |
        . +---+---+---+---+                                     | +---+---+---+---+                                     | +---+---+---+---+                                     |
        .=======================================================+=======================================================+=======================================================+
        .13.                                                    |13.                                                    |
        . +---+---+---+---+     NA : [  9,  X]                  |     +---+---+---+                                     |
        . |8.0|10--11---X |     P  : [8.0,6.0]                  |     |10--11---X |                                     |
        . +---+-|-+---+---+     NP : [P,1,4,5,2,6,8,4,10,11]    |     +-|-+---+---+     Trouvé!                         |
        . | # | 8 | # | # |     curseur = X                     |     | 8 |                                             |
        . +---+-|-+---+---+                                     |     +-|-+                                             |
        . | 4 | 5 | 6 |6.0|                                     |     | 5 |                                             |
        . +---+-|-+---+---+     Trouvé!                         | +---+-|-+             Trouvé!                         |
        . | P---1 | 2 | 4 |                                     | | P---1 |                                             |
        . +---+---+---+---+                                     | +---+---+                                             |
        .=======================================================+=======================================================+
        """
        
        print("Recherche d'un chemin à l'aide de A*")
        curseur = 0 # Curseur
        cases_actives = [self.pos] # Liste des cases actives
        cases_passives = [] # Liste des cases déjà évaluées
        chemins = [[self.pos]] # Liste des chemins pour se rendre à chaque case active
        poids = [Vec2.distance(self.pos, destination)] # Liste des poids
        n_pas = [0] # Distance à parcourir pour se rendre à chaque case active
        meilleur_chemin = []    # Meilleur chemin trouvé jusqu'à présent. Utilisé lorsqu'aucun chemin n'existe.
        meilleur_poid = int(2**32) # Meilleur poid trouvé jusqu'à présent. Utilisé lorsqu'aucun chemin n'existe.

        while True:

            #Choisir le poid le plus petit
            poid_min : float = sys.float_info.max
            i_case_min : int = -1 # Indexe de la case ayant le poid le plus petit. Est -1 pour évaluer si on a trouvé une case.
            for i in range(len(cases_actives)):
                if poids[i] < poid_min:
                    poid_min = poids[i]
                    i_case_min = i

            # S'assurer qu'on a trouvé une case
            if i_case_min != -1:
                curseur = i_case_min
            else :
                # Si on n'a rien trouvé
                print(coul("Aucun chemin n'existe vers la destination. Renvoie du chemin qui mène le plus près.",ROUGE))
                meilleur_chemin.pop(0)
                return meilleur_chemin
            
            # Dans le cas où la destination est un ennemi, on ne pourra jamais se rendre sur la destination, il faut donc se rendre sur la case adjascente.
            if not destination_adjascente:
                #Vérifier si le poid le plus petit est la destination
                if cases_actives[curseur] == destination:
                    print(coul("Chemin trouvé",VERT))
                    solution = chemins[curseur]
                    solution.pop(0)
                    return solution
            else:
                #Vérifier si la case adjascente est la destination
                if ( cases_actives[curseur]+Vec2( 1,0) == destination or
                     cases_actives[curseur]+Vec2(-1,0) == destination or
                     cases_actives[curseur]+Vec2(0, 1) == destination or
                     cases_actives[curseur]+Vec2(0,-1) == destination):
                    print(coul("Chemin trouvé",VERT))
                    solution = chemins[curseur]
                    solution.pop(0)
                    return solution
            
            #Ajouter les connexions du curseur à aux cases actives
            pos_curseur = cases_actives[curseur]
            px = pos_curseur + Vec2(1.0,0.0)    # Droite
            py = pos_curseur + Vec2(0.0,1.0)    # Haut
            nx = pos_curseur + Vec2(-1.0,0.0)   # Gauche
            ny = pos_curseur + Vec2(0.0,-1.0)   # Bas
            # Vérifier si px,py,nx ou ny sont dans les cases passives ou les actives
            px_dans_passif = False
            py_dans_passif = False
            nx_dans_passif = False
            ny_dans_passif = False
            for pos in cases_passives:
                px_dans_passif = px_dans_passif or px == pos
                py_dans_passif = py_dans_passif or py == pos
                nx_dans_passif = nx_dans_passif or nx == pos
                ny_dans_passif = ny_dans_passif or ny == pos
            for pos in cases_actives:
                px_dans_passif = px_dans_passif or px == pos
                py_dans_passif = py_dans_passif or py == pos
                nx_dans_passif = nx_dans_passif or nx == pos
                ny_dans_passif = ny_dans_passif or ny == pos
            
            # Si la case n'est pas dans les passives ou les actives et qu'on peut y aller
            if not px_dans_passif and self.carte.peutAller(self,px):
                cases_actives.append(px) # ajouter case adjascente aux cases actives
                n_pas.append(n_pas[curseur] + 1) # Ajouter la distance parcourue
                # Ajouter le chemin à parcourir
                c = deepcopy(chemins[curseur])
                c.append(px)
                chemins.append(c)
                # Ajouter le poid
                poids.append(n_pas[-1] + Vec2.distance(px,destination))

            if not py_dans_passif and self.carte.peutAller(self,py):
                cases_actives.append(py) # ajouter case adjascente aux cases actives
                n_pas.append(n_pas[curseur] + 1) # Ajouter la distance parcourue
                # Ajouter le chemin à parcourir
                c = deepcopy(chemins[curseur])
                c.append(py)
                chemins.append(c)
                # Ajouter le poid
                poids.append(n_pas[-1] + Vec2.distance(py,destination))

            if not nx_dans_passif and self.carte.peutAller(self,nx):
                cases_actives.append(nx) # ajouter case adjascente aux cases actives
                n_pas.append(n_pas[curseur] + 1) # Ajouter la distance parcourue
                # Ajouter le chemin à parcourir
                c = deepcopy(chemins[curseur])
                c.append(nx)
                chemins.append(c)
                # Ajouter le poidà
                poids.append(n_pas[-1] + Vec2.distance(nx,destination))

            if not ny_dans_passif and self.carte.peutAller(self,ny):
                cases_actives.append(ny) # ajouter case adjascente aux cases actives
                n_pas.append(n_pas[curseur] + 1) # Ajouter la distance parcourue
                # Ajouter le chemin à parcourir
                c = deepcopy(chemins[curseur])
                c.append(ny)
                chemins.append(c)
                # Ajouter le poid
                poids.append(n_pas[-1] + Vec2.distance(ny,destination))

            if Vec2.distance(pos_curseur,destination) < meilleur_poid:
                meilleur_poid = Vec2.distance(pos_curseur,destination)
                meilleur_chemin = chemins[curseur]

            #Passer le curseur aux cases passives
            n_pas.pop(curseur)
            poids.pop(curseur)
            chemins.pop(curseur)
            cases_passives.append(cases_actives.pop(curseur))