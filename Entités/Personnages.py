from Entités.Entité import *
from Entités.Golem import *
from Entités.Paysan import *
from Maths.Vec2 import Vec2
from Carte.Tuile import Tuile

class Joueur(Golem):

    def __init__(self):
        from Dessin.Image import Image
        super().__init__()
        self.nom = "Mélios"
        self.animID = "Mélios"
        self.camp = Entité.CAMP_JOUEUR
        self.campsEnnemis = [Entité.CAMP_PAYSANS]
        self.état.v = ÉtatIA.IMMOBILE
        self.PVMax = 20
        self.PV = self.PVMax
        self.limite_golem = 4
        self.distance_création_golem = 4.0

        self.dessin_Image : Image = Image("Mélios")

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
                Log.mdwn("<r>La commande : "+str(commande.catégorie)+" n'est pas acceptée par Mélios.</>")
                # raise AttributeError(coul("[Golem.commande] Commande mal construite : catégorie" + str(commande.catégorie) + " invalide.",ROUGE))
    
    def _commandeCréerGolem(self, commande : Commande):
        if Vec2.distance(self.pos, commande.position_création_golem) > self.distance_création_golem:
            Log.mdwn("<r>L'emplacement spécifié est trop loin. Vous ne pouvez pas créer de golem à plus de " + str(self.distance_création_golem) + " mètres de distance.</>")
            return
        
        if self.carte.matrice[int(commande.position_création_golem.x)][int(commande.position_création_golem.y)] == Tuile.TYPE_MUR:
            Log.mdwn("<r>Impossible de créer un golem à cet endroit : un mur s'y trouve.</>")
            return
        
        for e in self.carte.entités:
            if e.pos == commande.position_création_golem:
                Log.mdwn("<r>Impossible de créer un golem à cet endroit : **"+e.nom,ROUGE+"** s'y trouve déjà.</>")
                return
            
        élément = ""
        if self.limite_golem ==0:
            print("Limite de golems atteinte.")
            return
        else :
            golem : Golem = None
            carte = self.carte.matrice
            cp = commande.position_création_golem
            match carte[int(cp.x)][int(cp.y)].type:
                case Tuile.TYPE_TERRE:
                    golem = GolemTerre()
                    élément = "Terre"
                case Tuile.TYPE_EAU:
                    golem = GolemEau()
                    élément = "Eau"
                case Tuile.TYPE_FEUX:
                    golem = GolemFeu()
                    élément = "Feu"
                case Tuile.TYPE_OR:
                    golem = GolemDoré()
                    élément = "Or"
                case _:
                    raise TypeError("[Joueur._commandeCréerGolem] Impossible de créer un golem sur une tuile de type " + str(carte[int(cp.x)][int(cp.y)].type) + '.')
        golem.pos = commande.position_création_golem
        golem.carte = self.carte
        self.carte.entités.append(golem)
        Log.mdwn("<v>Golem de type "+élément+" créé. Son nom : **"+golem.nom+"**</>")
        self.limite_golem=self.limite_golem-1

    def Attaquer(self, attaque : Attaque):
        """Attaquer Fonction pour recevoir une attaque

        Prend une Attaque en argument. Active l'indice self.estAttaqué.

        Args:
            attaque (Attaque): Un objet Attaque qui contient les informations nécessaires pour subir une attaque.
        """
        Log.log(self.nom + " reçoit une attaque de " + attaque.provenance.nom)
        Log.log(self.nom + " a " + str(self.PV) + " PV, l'attaque fait " + str(attaque.dégats) + " PD")
        # Virer au mode combat, si on n'y est pas déjà
        if not self.estAttaqué:
            self.estAttaqué = True
    
        attaque = self._Défense(attaque)    # Évaluer la défense
        self.PV -= attaque.dégats          # Retirer les points de vies
        # Évaluer si on est morts
        if self.PV <= 0.0:
            Log.mdwn("**<r>"+self.nom+" est mort.</>**")
            self.PV = 0.0
            self.estVivant = False

    def _modeDéplacement(self):
        """ Se déplace vers la destionation sélectionnée

        Calcule un chemin vers la destination et s'y déplace.
        """
            
        Log.log("Recherche d'un chemin vers " + str(self.destination.x) + ';' + str(self.destination.y))
        self.naviguerVers(self.destination,False)

        # Si on n'a pas atteint le bout du chemin
        if len(self.chemin) > 0:
            Log.log("Un chemin existe, avançons")
            # Avancer sur le chemin
            self.direction = self.chemin[0] - self.pos
            self.pos = self.chemin.pop(0)

            # Si on n'a pas trouvé d'ennemi, mais qu'on est arrivé au bout du chemin,
            if self.pos == self.destination and self.état.v == ÉtatIA.COMBAT:
                Log.log("Arrivé à destination. Aucun ennemi à l'horison, Mode recherche activé.")
                # Chercher un autre ennemi si on est dans la boucle normale,
                # Rester immobile si on se déplace à cause d'une commande
                self.état.v = ÉtatIA.IMMOBILE

    def _modeImmobile(self):
        """_modeImmobile Rest immobile à la suite d'un déplacement dûs à une commande

        Vire en mode combat s'il reçoit une attaque
        """
        if self.estAttaqué:
            Log.mdwn("<o>Je suis attaqué!</>")

class Personnage(Chevalier):
    def __init__(self,nom : str):
        super().__init__()
        self.nom = nom
        self.état.v = ÉtatIA.IMMOBILE
        self.caratère_dessin = gras(coul("*|",GRIS))
        self.camp = Entité.CAMP_PERSONNAGES
        self.campsEnnemis = [Entité.CAMP_PAYSANS]
    
    def avoir_caractère_dessin(self):
        return self.caratère_dessin