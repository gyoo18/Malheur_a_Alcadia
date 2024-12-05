from Entités.Entité import *
import random
from Entités.Paysan import *
from Entités.Attaque import Attaque, Élément
from Maths.Vec2 import *
from TFX import *

class Commande:
    """ Classe décrivant une commande à un Golem

    Plusieures commandes sont disponibles:
     - DÉPLACEMENT          Déplacer le golem vers une position spécifique
     - ATTAQUE              Attaquer un paysans spécifique
     - ATTAQUE_SPÉCIALE     Activer l'attaque spéciale
     - DÉFENSE              Activer le mode défense
     - LIBÉRER              Libérer le golem et lui redonner son autonomie
     - CHARGER_ATTAQUE      Commencer une attaque chargé
     - ATTAQUER_CHARGE      Frapper avec l'attaque chargée
    
    Pour envoyer une commande, utiliser
    
    `Golem.commande( commande )`

    Afin de construire une commande, utiliser

    `commande = Commande`

    Suivit de l'une des fonctions suivantes:
     - `commande.faireCommandeDéplacement( destination : Vec2 )`
     - `commande.faireCommandeAttaque( ennemi : Entité )`
     - `commande.faireCommandeAttaqueSpéciale( attaque : str )` *Préciser l'attaque à effectuer avec l'une des attaques du golem en question Ex. : `GolemEau.ATTAQUE_SPÉCIALE`*
     - `commande.faireCommandeDéfense()`
     - `commande.faireCommandeLibérer()`
     - `commande.faireCommandeCharger()`
     - `commande.faireCommandeAttaquerCharge( ennemi : Entité )`

    """
    DÉPLACEMENT = "déplacement"
    ATTAQUE = "attaque"
    ATTAQUE_SPÉCIALE = "attaque spéciale"
    DÉFENSE = "défense"
    LIBÉRER = "libre"
    CHARGER_ATTAQUE = "charger attaque"
    ATTAQUER_CHARGE = "attaquer charge"

    CRÉER_GOLEM = "créer golem"
    
    def __init__(self):
        self.catégorie : str = ""

        self.destination : Vec2 = None
        self.ennemi_cible : Entité = None
        self.attaque_spéciale : str = None
        self.position_création_golem : Vec2 = None

    def faireCommandeDéplacement(self,destination : Vec2):
        """ Créé une commande qui déplace un golem vers `destination`

        Place le Golem dans le mode DÉPLACEMENT_IMMOBILE

        Args:
            destination (Vec2) : Destination vers laquelle se dirigera le golem
        """
        self.catégorie = self.DÉPLACEMENT
        self.destination = destination
    
    def faireCommandeAttaque(self, ennemi : Entité):
        """faireCommandeAttaque Créé une commande qui demandera à un golem d'attaquer un ennemi spécifique

        Placera le Golem dans le mode COMBAT

        Args:
            ennemi (Entité): Ennemi à attaquer
        """
        self.catégorie = self.ATTAQUE
        self.ennemi_cible = ennemi

    def faireCommandeAttaqueSpéciale(self, attaque : str):
        """ Créé une commande qui demandera au golem de commencer à charger une attaque

        **Pour le paramètre attaque, se référer au golem auquel on tente d'accéder, exemple `GolemEau.ATTAQUE_SPÉCIALE`**
        
        Placera le golem dans le mode CHARGER.

        Args:
            attaque (str) : Nom de l'attaque à utiliser. Se référer au golem auquel on tente d'accéder, `exemple GolemEau.ATTAQUE_SPÉCIALE`
        """
        self.catégorie = self.ATTAQUE_SPÉCIALE
        self.attaque_spéciale = attaque

    def faireCommandeDéfense(self):
        """ Créé une commande qui mettra un Golem dans le mode défense

        Placera le Golem dans le mode DÉFENSE
        """
        self.catégorie = self.DÉFENSE
    
    def faireCommandeLibérer(self):
        """ Crééra une commande qui libérera le golem du contrôle du joueur.

        Placera le golem dans le mode RECHERCHE
        """
        self.catégorie = self.LIBÉRER
    
    def faireCommandeCharger(self):
        """faireCommandeCharger Crééra une commande qui demandera au golem de commencer à charger une attaque

        Placera le Golem dans le mode CHARGER
        """
        self.catégorie = self.CHARGER_ATTAQUE
    
    def faireCommandeAttaquerCharge(self, ennemi : Entité):
        """faireCommandeAttaquerCharge Crééra une commande qui demandera au Golem de frapper avec son attaque chargée

        Attaque l'Entité spécifié par `ennemi`

        Args:
            ennemi (Entité): Entité à frapper avec l'attaque chargée
        """
        self.catégorie = self.ATTAQUER_CHARGE
        self.ennemi_cible = ennemi
    
    def faireCommandeCréerGolem(self, position : Vec2):
        """crééra une commande qui demandera au joueur de créer un golem à la position relative précisée

        **Notez que la commande ne serat acceptée que par le joueur**

        Raises:
            AttributeError: Si `position` n'est pas un `Vec2`
        """
        if type(position) != Vec2:
            raise AttributeError("L'argument 'position' doit être de type Vec2.")
        self.catégorie = self.CRÉER_GOLEM
        self.position_création_golem = position

class Golem(Entité):

    def __init__(self):
        super().__init__()
        self.camp = "Golems"
        self.campsEnnemis = ["Paysans"]
        self.nom = "Golem"

    
    def commande(self, commande : Commande):
        """commande Reçoit et interpète une commande donnée par le joueur

        Args:
            commande (Commande): commande à exécuter

        Raises:
            AttributeError: Si la commande est d'une catégorie invalide
        """
        match commande.catégorie:
            case Commande.DÉPLACEMENT:
                self._commandeDéplacement(commande)
            case Commande.ATTAQUE:
                self._commandeAttaque(commande)
            case Commande.ATTAQUE_SPÉCIALE:
                self._commandeAttaqueSpéciale(commande)
            case Commande.DÉFENSE:
                self._commandeDéfense(commande)
            case Commande.LIBÉRER:
                self._commandeLibérer(commande)
            case Commande.CHARGER_ATTAQUE:
                self._commandeChargerAttaque(commande)
            case Commande.ATTAQUER_CHARGE:
                self._commandeAttaquerCharge(commande)
            case _:
                raise AttributeError(coul("[Golem.commande] Commande mal construite : catégorie" + str(commande.catégorie) + " invalide.",ROUGE))

    def _commandeDéplacement(self, commande : Commande):
        """ Exécute une commande déplacement
        Raises:
            AttributeError: Si `commande.destination` n'est pas de type Vec2 (potentiellement NoneType)
        """
        if type(commande.destination) != Vec2:
            raise AttributeError(coul("[Golem._commandeDéplacement] Commande mal construite : commande.destination est un " + str(type(commande.destination)) + ", mais seuls les Vec2 sont acceptés",ROUGE))
        
        if self.étatCombat.v == ÉtatCombat.CHARGER:
            self.chargement = 0

        self.naviguerVers(commande.destination)
        self.état.v = ÉtatIA.DÉPLACEMENT_IMMOBILE
    def _commandeAttaque(self, commande : Commande):
        """_commandeAttaque Exécute une commande ATTAQUE

        Args:
            commande (Commande): commande à exécuter

        Raises:
            AttributeError: Si `commande.ennemi_cible` n'est pas une Entité
        """
        if not issubclass(type(commande.ennemi_cible),Entité):
            raise AttributeError(coul("[Golem._commandeAttaque] Commande mal construite : commande.ennemi_cible est un " + str(type(commande.ennemi_cible)) + ", mais seules les Entités sont acceptées.",ROUGE))
        
        if self.étatCombat.v == ÉtatCombat.CHARGER:
            self.chargement = 0

        self.état.v = ÉtatIA.DÉPLACEMENT
        self.cible = commande.ennemi_cible
        self.naviguerVers(self.cible.pos)
    def _commandeAttaqueSpéciale(self, commande : Commande):
        """ Exécute une commande ATTAQUE_SPÉCIALE

        Le golem de base n'a pas d'attaque spéciale
        """

        if self.étatCombat.v == ÉtatCombat.CHARGER:
            self.chargement = 0

        print(coul("[ATTENTION] Le golem de base n'a pas d'attaque spéciale.",JAUNE))
    def _commandeDéfense(self, commande : Commande):
        """ Exécute la commande DÉFENSE
        """
        if self.étatCombat.v == ÉtatCombat.CHARGER:
            self.chargement = 0

        self.état.v = ÉtatIA.COMBAT
        self.étatCombat.v = ÉtatCombat.DÉFENSE
    def _commandeLibérer(self, commande : Commande):
        """ Exécute la commande LIBÉRER
        """
        if self.étatCombat.v == ÉtatCombat.CHARGER:
            self.chargement = 0

        self.état.v = ÉtatIA.RECHERCHE
    def _commandeChargerAttaque(self, commande : Commande):
        """_commandeChargerAttaque Exécute la commande CHARGER_ATTAQUE
        """
        self.état.v = ÉtatIA.COMBAT
        self.étatCombat.v = ÉtatCombat.CHARGER
    def _commandeAttaquerCharge(self, commande : Commande):
        """_commandeAttaquerCharge Exécute la commande ATTAQUER_CHARGE
        """
        self.état.v = ÉtatIA.COMBAT
        self.étatCombat.v = ÉtatCombat.LIBRE # TODO #17 implémenter la commande d'attaque chargée des golems
    
    def _modeCombat(self):
        """_modeCombat Exécute le combat du Golem

        Supplante Entité._modeCombat

        Incrémente le compteur de chargement et appelle self._AttaquerCible()
        """
        if self.étatCombat.v == ÉtatCombat.CHARGER:
            self.chargement += 1
        elif self.cible.estVivant and Vec2.distance(self.cible.pos, self.pos) <= 1:
            self._AttaquerCible()
        else:
            self.état.v = ÉtatIA.RECHERCHE
            self.estAttaqué = False
            self.cible = None

    def _AttaquerCible(self):
        """_AttaquerCible Attaque la cible définie par self.cible

        Appelle self.cible.Attaquer()
        """
        attaque = Attaque(self)
        attaque.dégats = self.attaque_normale_dégats + self.attaque_chargée*self.chargement
        self.cible.Attaquer(attaque)      

class GolemTerre(Golem):
    """GolemTerre Golem de type terre

    Gros tas de terre avec un arbre sur le dos, il est polyvalent, mais faible.

    Propriétées : 
     - Attaque spéciale : FRAPPE LE SOL, attaque de zone.
     - Camp : "Golems"
     - CampsEnnemis : ["Paysans"]
    """
    ATTAQUE_SPÉCIALE = "frapper sol"

    def __init__(self):
        super().__init__()
        self.PVMax=150
        self.PV = self.PVMax
        self.attaque_normale_dégats= Entité.Random_Stats(10,16)
        self.dégats_libre= Entité.Random_Stats(39,46)
        self.nom=Golem.nom_aléatoire(["Gorb","Bob","Pierre","Fero","Crys"])
        self.attaque_sol_dégats : float = 1.0
        self.attaque_sol_rayon : float = 2.0
    def _commandeAttaqueSpéciale(self, commande : Commande):
        if commande.attaque_spéciale == self.ATTAQUE_SPÉCIALE:
            attaque = Attaque(self)
            attaque.dégats = self.attaque_sol_dégats + self.attaque_chargée*self.chargement
            attaque.élément = Élément.TERRE
            for ennemi in self.carte.entités:
                if Vec2.distance(self.pos, ennemi.pos) < self.attaque_sol_rayon:
                    attaque.distance = Vec2.distance(self.pos,ennemi.pos)
                    attaque.direction = ennemi.pos-self.pos
                    ennemi.Attaquer(attaque)
    
    def _AttaquerCible(self):
        attaque = Attaque(self)
        attaque.dégats = self.attaque_normale_dégats + self.attaque_chargée*self.chargement
        attaque.élément = Élément.TERRE
        self.cible.Attaquer(attaque)
        self.chargement = 0

class GolemEau(Golem):
    """GolemEau Golem de type Eau

    Colonne d'eau, il n'est pas très mobile et difficile à placer, mais peut attaquer à distance

    Propriétés : 
     - Attaque Spéciale : ATTAQUE TORNADE, repousse les ennemis des quelques cases
     - Camp : "Golem"
     - CampsEnnemis : ["Paysans"]
     - Immobile
     - Attaque à distance
    """
    ATTAQUE_SPÉCIALE = "attaque tornade"

    def __init__(self):
        super().__init__()
        self.PVMax=90
        self.PV = self.PVMax
        self.attaque_normale_dégats=Entité.Random_Stats(20,26)
        self.dégats_libre=Entité.Random_Stats(25,31)
        self.nom=Golem.nom_aléatoire(["Blob","Plouf","Sploch","Casca","Rive"])
        self.tornade_pousser_distance : int = 3

        self.max_distance_attaque : float = 4

    def _commandeAttaqueSpéciale(self, commande):
        if commande.attaque_spéciale == self.ATTAQUE_ and Vec2.distance(self.pos, commande.ennemi_cible.pos) <= self.max_distance_attaque:
            for i in range(self.tornade_pousser_distance + self.chargement):
                direction = Vec2.norm(commande.ennemi_cible.pos - self.pos)
                direction.x = round(direction.x)
                direction.y = round(direction.y)
                déplacement = Vec2(0)
                if self.carte.peutAller(commande.ennemi_cible.pos + ( direction*Vec2(1,0) )):
                    déplacement += direction*Vec2(1,0)
                if self.carte.peutAller(commande.ennemi_cible.pos + ( direction*Vec2(0,1) )):
                    déplacement += direction*Vec2(1,0)
                commande.ennemi_cible.pos += déplacement
            self.chargement = 0
    
    def _commandeDéplacement(self, commande):
        print(coul("Le golem d'eau ne peut pas se déplacer!",JAUNE))

    def _modeRecherche(self):
        ennemiPlusPrès = None
        distanceMinimale = sys.float_info.max
        for ennemi in self.carte.entités:
            if Vec2.distance(ennemi.pos,self.pos) < distanceMinimale and Vec2.distance(ennemi.pos,self.pos) <= self.max_distance_attaque and ennemi.camp in self.campsEnnemis:
                ennemiPlusPrès = ennemi
                distanceMinimale = Vec2.distance(ennemi.pos,self.pos)
        if ennemiPlusPrès != None:
            self.état.v = ÉtatIA.COMBAT
            self.cible = ennemiPlusPrès
    
    def _modeCombat(self):
        """_modeCombat Exécute le combat du Golem

        Supplante Entité._modeCombat

        Incrémente le compteur de chargement et appelle self._AttaquerCible()
        """
        if self.étatCombat.v == ÉtatCombat.CHARGER:
            self.chargement += 1
        elif self.cible.estVivant and Vec2.distance(self.cible.pos, self.pos) <= self.max_distance_attaque:
            self._AttaquerCible()
        else:
            self.état.v = ÉtatIA.RECHERCHE
            self.estAttaqué = False
            self.cible = None
    
    def _AttaquerCible(self):
        attaque = Attaque(self)
        attaque.dégats = self.attaque_normale_dégats + self.attaque_chargée*self.chargement
        attaque.élément = Élément.EAU
        attaque.est_projectile = True
        attaque.distance = Vec2.distance(self.pos, self.cible.pos)
        self.cible.Attaquer(attaque)
        self.chargement = 0

class GolemFeu(Golem):
    """GolemFeu Golem de type feu

    Extrait des profondeures de la terre, sa croûte de lave, lechée par ses cheveux de feux, peut cracher des boules brûlantes qui fonderont les armures.

    Propriétées :
     - Attaque spéciale : BOULE DE FEU, lance une boule de feu sur les ennemis
     - Camp : "Golems"
     - CampsEnnemis : ["Paysans"]
    """
    ATTAQUE_SPÉCIALE = "attaque boule de feu"
    

    def __init__(self):
        super().__init__()
        self.PVMax=120
        self.PV = self.PVMax
        self.attaque_normale_dégats=Entité.Random_Stats(26,29)
        self.dégats_libre=Entité.Random_Stats(35,39)
        self.nom=Golem.nom_aléatoire(["Magme","Fusio","Larva","Manta","Ardenne"])
        self.attaque_max_distance : float = 4.0
        self.boule_feu_dégats : int = 3

    def _commandeAttaqueSpéciale(self, commande):
        if commande.attaque_spéciale == self.ATTAQUE_SPÉCIALE and Vec2.distance(self.pos,commande.ennemi_cible.pos) <= self.attaque_normale_dégats:
            attaque = Attaque(self)
            attaque.élément = Élément.FEU
            attaque.est_projectile = True
            attaque.distance = Vec2.distance(self.pos, commande.ennemi_cible.pos)
            attaque.direction = commande.ennemi_cible.pos - self.pos
            attaque.dégats = self.boule_feu_dégats + self.attaque_chargée*self.chargement
            commande.ennemi_cible.Attaquer(attaque)
    
    def _AttaquerCible(self):
        attaque = Attaque(self)
        attaque.dégats = self.attaque_normale_dégats + self.attaque_chargée*self.chargement
        attaque.élément = Élément.FEU
        self.cible.Attaquer(attaque)
        self.chargement = 0

class GolemDoré(Golem):

    def __init__(self):
        super().__init__()
        vieMax=150
        attaque_normale_dégats=Entité.Random_Stats(25,31)
        dégats_libre=Entité.Random_Stats(36,42)
        nom=Entité.nom_aléatoire(["Goldy","Flash","Shiny","Conqi","King"])