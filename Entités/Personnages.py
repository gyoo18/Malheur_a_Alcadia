from Entités.Entité import *
from Entités.Golem import *
from Maths.Vec2 import Vec2
from Carte.Tuile import Tuile

class Joueur(Golem):

    def __init__(self):
        super().__init__()
        self.nom = "Mélios"
        self.camp = "Personnages"
        self.campsEnnemis = ["Paysans"]
        self.état.v = ÉtatIA.IMMOBILE
        self.PVMax = 20
        self.PV = self.PVMax
        
        self.distance_création_golem = 4.0

    def commande(self, commande):
        """commande Reçoit et interpète une commande donnée par le joueur

        Args:
            commande (Commande): commande à exécuter

        Raises:
            AttributeError: Si la commande est d'une catégorie invalide
        """
        match commande.catégorie:
            case Commande.DÉPLACEMENT:
                self._commandeDéplacement(commande)
            case Commande.CRÉER_GOLEM:
                self._commandeCréerGolem(commande)
            case _:
                raise AttributeError(coul("[Golem.commande] Commande mal construite : catégorie" + str(commande.catégorie) + " invalide.",ROUGE))
    
    def _commandeCréerGolem(self, commande : Commande):
        if self.carte.matrice[int(commande.position_création_golem.x)][int(commande.position_création_golem.y)] != Tuile.TYPE_MUR and Vec2.distance(self.pos, commande.position_création_golem) <= self.distance_création_golem:
            golem : Golem = None
            carte = self.carte.matrice
            cp = commande.position_création_golem
            match carte[int(cp.x)][int(cp.y)].type:
                case Tuile.TYPE_TERRE:
                    golem = GolemTerre()
                case Tuile.TYPE_EAU:
                    golem = GolemEau()
                case Tuile.TYPE_FEUX:
                    golem = GolemFeu()
                case _:
                    raise TypeError("[Joueur._commandeCréerGolem] Impossible de créer un golem sur une tuile de type " + str(carte[int(cp.x)][int(cp.y)].type) + '.')
            golem.pos = commande.position_création_golem
            golem.carte = self.carte
            self.carte.entités.append(golem)

    def Attaquer(self, attaque : Attaque):
        """Attaquer Fonction pour recevoir une attaque

        Prend une Attaque en argument. Active l'indice self.estAttaqué.

        Args:
            attaque (Attaque): Un objet Attaque qui contient les informations nécessaires pour subir une attaque.
        """
        print(self.nom + " reçoit une attaque de " + attaque.provenance.nom)
        print(self.nom + " a " + str(self.PV) + " PV, l'attaque fait " + str(attaque.dégats) + " PD")
        # Virer au mode combat, si on n'y est pas déjà
        if not self.estAttaqué:
            self.estAttaqué = True
    
        attaque = self._Défense(attaque)    # Évaluer la défense
        self.PV -= attaque.dégats          # Retirer les points de vies
        # Évaluer si on est morts
        if self.PV <= 0.0:
            print(self.nom + " est mort.")
            self.PV = 0.0
            self.estVivant = False

    def _modeDéplacement(self):
        """ Se déplace vers la destination sélectionnée

        Calcule un chemin vers la destination et s'y déplace.
        """
        faire_pathfinding = True
        # Si on n'a pas atteint le bout du chemin
        if len(self.chemin) > 0:
            print("Un chemin existe")
            # Avancer sur le chemin
            if self.carte.peutAller(self,self.chemin[0]):
                print("Le chemin est praticable, avançons.")
                self.direction = self.chemin[0] - self.pos
                self.pos = self.chemin.pop(0)
                faire_pathfinding = False

                # Si on est arrivé au bout du chemin,
                if self.pos == self.destination:
                    print("Arrivé à destination. Mode immobile activé")
                    # Rester immobile
                    self.état.v = ÉtatIA.IMMOBILE
            else:
                print("Le chemin n'est pas praticable.")
                # Si on ne peut pas se déplacer sur le chemin, en trouver un nouveau
                self.chemin = []
                faire_pathfinding = True

        if faire_pathfinding:
            print("Recherche d'un chemin.")
            self.chemin = self._A_étoile()


    def _modeImmobile(self):
        """_modeImmobile Rest immobile à la suite d'un déplacement dûs à une commande

        Vire en mode combat s'il reçoit une attaque
        """
        if self.estAttaqué:
            print("Je suis attaqué!")