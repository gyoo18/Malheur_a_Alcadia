from Entités.Entité import Entité,ÉtatCombat,ÉtatIA
from InclusionsCirculaires.Entité_Attaque import *
from Maths.Vec2 import *
from math import acos, sqrt
import copy
from TFX import *

class Paysan(Entité):

    def __init__(self):
        super().__init__()
        self.camp = Entité.CAMP_PAYSANS
        self.campsEnnemis = [Entité.CAMP_GOLEMS,Entité.CAMP_JOUEUR,Entité.CAMP_PERSONNAGES]
        self.nom = "Paysan"
        self.nomAffichage = self.nom

    def _AttaquerEnnemi(self):
        match self.étatCombat.v:
            case ÉtatCombat.CHARGER:
                self.chargement += 1
                if self.chargement >= self.TEMP_CHARGEMENT:
                    self._exécuterAttaque()
                    self.chargement = 0
                    self.étatCombat.v = ÉtatCombat.LIBRE

            case ÉtatCombat.DÉFENSE:
                if self.cible.étatCombat.v != ÉtatCombat.CHARGER:
                    self.étatCombat.v = ÉtatCombat.LIBRE

            case ÉtatCombat.LIBRE:
                match self.cible.étatCombat.v:
                    case ÉtatCombat.LIBRE:
                        attaque = Attaque(self)
                        attaque.dégats = self.attaque_normale_dégats
                        self.cible.Attaquer(attaque)

                    case ÉtatCombat.DÉFENSE:
                        self.étatCombat = ÉtatCombat.CHARGER

                    case ÉtatCombat.CHARGER:
                        self.étatCombat = ÉtatCombat.DÉFENSE
    
    def _exécuterAttaque(self):
        attaque = Attaque(self)
        attaque.dégats = self.attaque_normale_dégats + self.chargement*self.attaque_chargée
        self.cible.Attaquer(attaque)
        self.chargement = 0

class Gosse(Paysan):

    noms_originaux : list[str] = ["Lhucra","Karck","Gryui","Vhynch"]
    noms : list[str] = copy.deepcopy(noms_originaux)

    def __init__(self):
        super().__init__()
        self.PVMax=75
        self.PV = self.PVMax
        self.attaque_normale_dégats=self.Random_Stats(8,11)
        self.dégats_libre=self.Random_Stats(5,11)
        self.nom=Entité.nom_aléatoire(Gosse.noms)
        self.nomAffichage = self.nom

    def _exécuterAttaque(self):
        attaque = Attaque(self)
        attaque.dégats = self.attaque_normale_dégats + self.chargement*self.attaque_chargée
        self.cible.Attaquer(attaque)
        self.chargement = 0

class Mineur(Paysan):

    noms_originaux : list[str] = ["Kol","Patt","Mork","Bury","Jack"]
    noms : list[str] = copy.deepcopy(noms_originaux)

    def __init__(self):
        super().__init__()
        self.PVMax=75
        self.PV = self.PVMax
        self.attaque_normale_dégats=self.Random_Stats(14,21)
        self.dégats_libre=self.Random_Stats(10,16)
        self.nom=Entité.nom_aléatoire(Mineur.noms)
        self.nomAffichage = self.nom
        self.bonus_terre : int = 2 # Bonus contre les golems de terre

    def _exécuterAttaque(self):
        attaque = Attaque(self)
        attaque.dégats = self.attaque_normale_dégats + self.chargement*self.attaque_chargée
        if type(self.cible) == GolemTerre:
            attaque.dégats += self.bonus_terre
        self.cible.Attaquer(attaque)
        self.chargement = 0
    
class Prêtre(Paysan):

    noms_originaux : list[str] = ["StFray","StClark","StTurc","StJoph","StLam"]
    noms : list[str] = copy.deepcopy(noms_originaux)

    def __init__(self):
        super().__init__()
        self.PVMax=75
        self.PV = self.PVMax
        self.attaque_normale_dégats=self.Random_Stats(12,17)
        self.dégats_libre=self.Random_Stats(12,15)
        self.nom=Entité.nom_aléatoire(Prêtre.noms)   
        self.nomAffichage = self.nom     
        self.PVAddition : int = 2

    def _modeRecherche(self):
        ennemiPlusPrès = None
        alliéPlusPrès = None
        distanceMinimaleEnnemi = sys.float_info.max
        distanceMinimaleAllié = sys.float_info.max
        for entité in self.carte.entités:
            if Vec2.distance(entité.pos,self.pos) < distanceMinimaleEnnemi and self._estEnnemi(entité):
                ennemiPlusPrès = entité
                distanceMinimaleEnnemi = Vec2.distance(entité.pos,self.pos)
            elif Vec2.distance(entité.pos,self.pos) < distanceMinimaleAllié and entité.camp == self.camp:
                alliéPlusPrès = entité
                distanceMinimaleAllié = Vec2.distance(entité.pos,self.pos)
        if ennemiPlusPrès != None and alliéPlusPrès == None:
            self.état.v = ÉtatIA.DÉPLACEMENT
            self.destination = ennemiPlusPrès.pos
        elif ennemiPlusPrès == None and alliéPlusPrès != None:
            self.état.v = ÉtatIA.DÉPLACEMENT
            self.destination = alliéPlusPrès.pos
        elif ennemiPlusPrès != None and alliéPlusPrès != None:
            if ennemiPlusPrès.PV/ennemiPlusPrès.PVMax < alliéPlusPrès.PV/alliéPlusPrès.PVMax:
                self.destination = ennemiPlusPrès.pos
            else :
                self.destination = alliéPlusPrès.pos
        
    def _modeDéplacement(self): # TODO #23 L'arbalettier ne se déplace pas
        faire_pathfinding = True
        if len(self.chemin) > 0:
            if self.carte.peutAller(self.chemin[0].pos):
                self.direction = self.chemin[0].pos - self.pos
                self.pos = self.chemin[0].pos.copie()
                faire_pathfinding = False

                for ennemi in self.carte.entités:
                    if Vec2.distance(ennemi.pos, self.pos) <= 1 and self.cible.camp in self.campsEnnemis:
                        self.état.v = ÉtatIA.COMBAT
                        self.cible = ennemi
                        break
                    elif Vec2.distance(ennemi.pos, self.pos) <= 1 and self.cible.camp == self.camp:
                        self.état.v = ÉtatIA.GUÉRISON
                        break
                if self.cible == None and self.pos == self.destination and self.état.v == ÉtatIA.DÉPLACEMENT:
                    self.état.v = ÉtatIA.RECHERCHE
                elif self.cible == None and self.pos == self.destination and self.état.v == ÉtatIA.DÉPLACEMENT_IMMOBILE:
                    self.état.v = ÉtatIA.IMMOBILE
            else:
                self.chemin = []
                faire_pathfinding = True

        if faire_pathfinding:
            self.chemin = self._A_étoile(self.carte, self.pos, self.destination)
    
    def _exécuterAttaque(self):
        attaque = Attaque(self)
        attaque.dégats = self.attaque_normale_dégats + self.chargement*self.attaque_chargée
        self.cible.Attaquer(attaque)
    
    def _modeGuérison(self):
        if self.cible.PV < self.cible.PVMax and Vec2.distance(self.cible.pos, self.pos) <= 1:
            self.cible.PV += self.PVAddition
            self.cible.PV = min(self.cible.PV,self.cible.PVMax)
        else:
            self.état.v = ÉtatIA.RECHERCHE
            self.cible = None
    
class Chevalier(Paysan):

    noms_originaux : list[str] = ["SirRaudryguish","SirHarchurt","SirMorline","SirLrimqu"]
    noms : list[str] = copy.deepcopy(noms_originaux)

    def __init__(self):
        super().__init__()
        self.PVMax=125
        self.PV = self.PVMax
        self.attaque_normale_dégats=self.Random_Stats(19,26)
        self.dégats_libre=self.Random_Stats(30,36)
        self.nom=Entité.nom_aléatoire(Chevalier.noms)
        self.nomAffichage = self.nom

    def _exécuterAttaque(self):
        attaque = Attaque(self)
        attaque.dégats = self.attaque_normale_dégats + self.chargement*self.attaque_chargée
        if self.chargement > 0:
            for entité in self.carte.entités:
                angle = acos(self.direction.norm() @ Vec2.norm(entité.pos - self.pos))   # Le @ est un produit scalaire (a•b)
                """
                #   Les trois cases en face du chevaliere se trouvent à un angle d'au plus 45° de la direction vers laquelle il fait face
                #   et à une distance d'au plus √2. Pour s'assurer que les entitées prises dans l'attaque soient détectée, on augmente
                #   légèrement la zone d'effet (47° au lieu de 45° et √2.1 au lieu de √2 )
                # 
                #                 +-----+-----+-----+         +-----+-----+-----+
                #                 |\    |     |     |         |     |     |     |
                #              47°->\X  |  X  |  X  |         |  X  |  X  |  O  |
                #                 |   \\|  |  |/ <---√2       √2-> \|  |  |     |
                #                 +-----+-----+-----+         +-----+--|--+-----+
                #                 |     |\ |^/| <- 45°       45°-> ( \ |  |     |
                #                 |  O  |  C  |  O  |         |  X-----C  |  O  |
                #                 |     |     |     |         |     |     |     |
                #                 +-----+-----+-----+         +-----+-----+-----+
                #                 |     |     |     |         |     |     |     |
                #                 |  O  |  O  |  O  |         |  O  |  O  |  O  |
                #                 |     |     |     |         |     |     |     |
                #                 +-----+-----+-----+         +-----+-----+-----+
                #                            
                """
                if angle <= 47 and Vec2.distance(self.pos, entité.pos) <= sqrt(2.1):
                    entité.Attaquer(attaque)
        else:
            self.cible.Attaquer(attaque)
    
class Arbalettier(Paysan):
    
    noms_originaux : list[str] = ["Rambo","Rocky","Laçette","Fréch","Chaubin","Soly"]
    noms : list[str] = copy.deepcopy(noms_originaux)

    def __init__(self):
        super().__init__()
        self.PVMax=int(50)
        self.PV = self.PVMax
        self.attaque_normale_dégats=self.Random_Stats(30,33)
        self.dégats_libre=self.Random_Stats(5,11)
        self.nom=Entité.nom_aléatoire(Arbalettier.noms)   
        self.nomAffichage = self.nom     
        self.max_distance_attaque : float = 4.0
        self.min_distance_ennemi : float = 2.0

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
        modefuite = False
        ennemiTropPrès = None
        for ennemi in self.carte.entités:
            # Chercher un ennemi à une distance de 1 ou moins de nous (sur une case adjascente)
            if Vec2.distance(ennemi.pos, self.pos) <= self.min_distance_ennemi and (ennemi.camp in self.campsEnnemis or ennemi == self.cible):
                modefuite= True
                direction = Vec2.norm(self.pos - ennemi.pos)

                xp = direction @ Vec2(1.0,0.0)
                yp = direction @ Vec2(0.0,1.0)
                xn = direction @ Vec2(-1.0,0.0)
                yn = direction @ Vec2(0.0,-1.0)

                trouvé = False
                dirs = [xp,yp,xn,yn]
                while not trouvé and len(dirs) != 0:
                    maxd = -10
                    for e in dirs:
                        maxd = max(maxd,e)
                    if maxd == xp and not trouvé:
                        self.destination = self.pos + Vec2(1.0,0.0)
                        if self.carte.peutAller(self,self.destination):
                            trouvé = True
                        else:
                            dirs.remove(xp)
                    if maxd == xn and not trouvé:
                        self.destination = self.pos + Vec2(-1.0,0.0)
                        if self.carte.peutAller(self,self.destination):
                            trouvé = True
                        else:
                            dirs.remove(xn)
                    if maxd == yp and not trouvé:
                        self.destination = self.pos + Vec2(0.0,1.0)
                        if self.carte.peutAller(self,self.destination):
                            trouvé = True
                        else:
                            dirs.remove(yp)
                    if maxd == yn and not trouvé:
                        self.destination = self.pos + Vec2(0.0,-1.0)
                        if self.carte.peutAller(self,self.destination):
                            trouvé = True
                        else:
                            dirs.remove(yn)
                break
            
        if not modefuite:
            for ennemi in self.carte.entités:
                # Chercher un ennemi à une distance de 1 ou moins de nous (sur une case adjascente)
                if Vec2.distance(ennemi.pos, self.pos) <= self.max_distance_attaque and Vec2.distance(ennemi.pos, self.pos) > self.min_distance_ennemi and (ennemi.camp in self.campsEnnemis or ennemi == self.cible):
                    print("Un ennemi est à proximité! Mode combat activé.")
                    self.chemin = []
                    self.état.v = ÉtatIA.COMBAT
                    self.cible = ennemi
                    return
            
        if self.état.v == ÉtatIA.DÉPLACEMENT:
            if self.cible != None and self.cible.estVivant :
                print("Recherche d'un chemin vers " + self.cible.nom)
                self.naviguerVers(self.cible.pos,True)
            elif self.cible != None and not self.cible.estVivant:
                print("La cible est morte. À la recherche d'un nouvel ennemi")
                self.état.v = ÉtatIA.RECHERCHE
            elif self.pos != self.destination:
                print("Recherche d'un chemin ver " + str(self.destination))
                self.naviguerVers(self.destination,False)
        elif self.état.v == ÉtatIA.DÉPLACEMENT_IMMOBILE:
            print("Recherche d'un chemin vers " + str(self.destination.x) + ';' + str(self.destination.y))
            self.naviguerVers(self.destination,False)

        # Si on n'a pas atteint le bout du chemin
        if len(self.chemin) > 0:
            print("Un chemin existe, avançons")
            # Avancer sur le chemin
            self.direction = self.chemin[0] - self.pos
            self.pos = self.chemin.pop(0)

            if not modefuite:
                # Si un ennemi se trouve sur une case adjascente, virer en mode combat
                for ennemi in self.carte.entités:
                    # Chercher un ennemi à une distance de 1 ou moins de nous (sur une case adjascente)
                    if Vec2.distance(ennemi.pos, self.pos) <= self.max_distance_attaque and Vec2.distance(ennemi.pos, self.pos) > self.min_distance_ennemi and (ennemi.camp in self.campsEnnemis or ennemi == self.cible):
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
        if self.pos == Vec2(5,4):
            print("Hey")
        for entité in self.carte.entités:
            if Vec2.distance(self.pos, entité.pos) <= self.min_distance_ennemi and entité.camp in self.campsEnnemis:
                print(coul("L'ennemi est trop près, fuyons!",ORANGE))
                self.état.v = ÉtatIA.DÉPLACEMENT
                self.cible = None
                return
        if self.cible.estVivant and Vec2.distance(self.cible.pos, self.pos) <= self.max_distance_attaque:
            self._AttaquerEnnemi()
        else:
            self.état.v = ÉtatIA.RECHERCHE
            self.estAttaqué = False
            self.cible = None
    
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
            self.estAttaqué = True
    
        attaque = self._Défense(attaque)    # Évaluer la défense
        self.PV -= attaque.dégats          # Retirer les points de vies
        # Évaluer si on est morts
        if self.PV <= 0.0:
            print(TFX(self.nom,gras=True,Pcoul=ROUGE) + TFX(" est mort.",Pcoul=ROUGE))
            self.PV = 0.0
            self.estVivant = False


