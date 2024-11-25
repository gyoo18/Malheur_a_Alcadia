from Entités.Entité import *
from Entités.Paysan import *
from Entités.Attaque import Attaque, Élément
from Maths.Vec2 import *

class Commande:
    DÉPLACEMENT = "déplacement"
    ATTAQUE = "attaque"
    ATTAQUE_SPÉCIALE = "attaque spéciale"
    DÉFENSE = "défense"
    LIBÉRER = "libre"
    CHARGER_ATTAQUE = "charger attaque"
    ATTAQUER_CHARGE = "attaquer charge"

    catégorie : str

    destination : Vec2 = None
    ennemi_cible : Entité = None
    attaque_spéciale : str = None
    
    def __init__(self):
        pass

    def faireCommandeDéplacement(self,destination : Vec2):
        self.catégorie = self.DÉPLACEMENT
        self.destination = destination
    
    def faireCommandeAttaque(self, ennemi : Entité):
        self.catégorie = self.ATTAQUE
        self.ennemi_cible = ennemi

    def faireCommandeAttaqueSpéciale(self, attaque : str):
        self.catégorie = self.ATTAQUE_SPÉCIALE
        self.attaque_spéciale = attaque

    def faireCommandeDéfense(self):
        self.catégorie = self.DÉFENSE
    
    def faireCommandeLibérer(self):
        self.catégorie = self.LIBÉRER
    
    def faireCommandeCharger(self):
        self.catégorie = self.CHARGER_ATTAQUE
    
    def faireCommandeAttaquerCharge(self, ennemi : Entité):
        self.catégorie = self.ATTAQUER_CHARGE
        self.ennemi_cible = ennemi

class Golem(Entité):

    def __init__(self):
        self.camp = "Golems"
        self.campsEnnemis = ["Paysans"]
        super().__init__()

    def commande(self, commande : Commande):
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

    def _commandeDéplacement(self, commande : Commande):
        if self.étatCombat.v == ÉtatCombat.CHARGER:
            self.chargement = 0

        self.état.v = ÉtatIA.DÉPLACEMENT
        self.naviguerVers(commande.destination)
    def _commandeAttaque(self, commande : Commande):
        if self.étatCombat.v == ÉtatCombat.CHARGER:
            self.chargement = 0

        self.état.v = ÉtatIA.DÉPLACEMENT
        self.cible = commande.ennemi_cible
        self.naviguerVers(self.cible.pos)
    def _commandeAttaqueSpéciale(self, commande : Commande):
        if self.étatCombat.v == ÉtatCombat.CHARGER:
            self.chargement = 0

        print("[ATTENTION] Le golem de base n'a pas d'attaque spéciale.")
    def _commandeDéfense(self, commande : Commande):
        if self.étatCombat.v == ÉtatCombat.CHARGER:
            self.chargement = 0

        self.état.v = ÉtatIA.COMBAT
        self.étatCombat = ÉtatCombat.DÉFENSE
    def _commandeLibérer(self, commande : Commande):
        if self.étatCombat.v == ÉtatCombat.CHARGER:
            self.chargement = 0

        self.état.v = ÉtatIA.RECHERCHE
    def _commandeChargerAttaque(self, commande : Commande):
        self.état.v = ÉtatIA.COMBAT
        self.étatCombat.v = ÉtatCombat.CHARGER
    def _commandeAttaquerCharge(self, commande : Commande):
        self.état.v = ÉtatIA.COMBAT
        self.étatCombat.v = ÉtatCombat.LIBRE
    
    def _modeCombat(self):
        if self.étatCombat.v == ÉtatCombat.CHARGER:
            self.chargement += 1
        elif self.cible.estVivant and Vec2.distance(self.cible.pos, self.pos) <= 1:
            self._AttaquerEnnemi()
        else:
            self.état.v = ÉtatIA.RECHERCHE
            self.estAttaqué = False
            self.cible = None

    def _AttaquerEnnemi(self):
        attaque = Attaque(self)
        attaque.dégats = self.attaque_normale_dégats + self.attaque_chargée*self.chargement
        self.cible.Attaquer(attaque)      

class GolemTerre(Golem):
    ATTAQUE_FRAPPER_SOL = "frapper sol"
    attaque_sol_rayon :float
    attaque_sol_dégats :float

    def __init__(self):
        super().__init__()
        self.attaque_sol_dégats = 1.0
        self.attaque_sol_rayon = 2.0

    def _commandeAttaqueSpéciale(self, commande : Commande):
        if commande.attaque_spéciale == self.ATTAQUE_FRAPPER_SOL:
            attaque = Attaque(self)
            attaque.dégats = self.attaque_sol_dégats + self.attaque_chargée*self.chargement
            attaque.élément = Élément.TERRE
            for ennemi in self.carte.entités:
                if distance(self.pos, ennemi.pos) < self.attaque_sol_rayon:
                    attaque.distance = distance(self.pos,ennemi.pos)
                    attaque.direction = ennemi.pos-self.pos
                    ennemi.Attaquer(attaque)
    
    def _AttaquerEnnemi(self):
        attaque = Attaque(self)
        attaque.dégats = self.attaque_normale_dégats + self.attaque_chargée*self.chargement
        attaque.élément = Élément.TERRE
        self.cible.Attaquer(attaque)
        self.chargement = 0

class GolemEau(Golem):
    ATTAQUE_TORNADE = "attaque tornade"
    tornade_pousser_distance : int = 3

    max_distance_attaque : float = 4

    def __init__(self):
        super().__init__()

    def _commandeAttaqueSpéciale(self, commande):
        if commande.attaque_spéciale == self.ATTAQUE_TORNADE and distance(self.pos, commande.ennemi_cible.pos) <= self.max_distance_attaque:
            for i in range(self.tornade_pousser_distance + self.chargement):
                direction = norm(commande.ennemi_cible.pos - self.pos)
                direction.x = round(direction.x)
                direction.y = round(direction.y)
                déplacement = Vec2(0)
                if self.carte.peutAller(commande.ennemi_cible.pos + ( direction*Vec2(1,0) )):
                    déplacement += direction*Vec2(1,0)
                if self.carte.peutAller(commande.ennemi_cible.pos + ( direction*Vec2(0,1) )):
                    déplacement += direction*Vec2(1,0)
                commande.ennemi_cible.pos += déplacement
            self.chargement = 0


    def _modeRecherche(self):
        ennemiPlusPrès = None
        distanceMinimale = sys.float_info.max
        for ennemi in self.carte.entités:
            if Vec2.distance(ennemi.pos,self.pos) < distanceMinimale and Vec2.distance(ennemi.pos,self.pos) <= self.max_distance_attaque and ennemi.camp in self.campsEnnemis:
                ennemiPlusPrès = ennemi
                distanceMinimale = Vec2.distance(ennemi.pos,self.pos)
        if ennemiPlusPrès != None:
            self.état.v = ÉtatIA.COMBAT
            self.destination = ennemi.pos
    
    def _AttaquerEnnemi(self):
        attaque = Attaque(self)
        attaque.dégats = self.attaque_normale_dégats + self.attaque_chargée*self.chargement
        attaque.élément = Élément.EAU
        attaque.est_projectile = True
        attaque.distance = Vec2.distance(self.pos, self.cible.pos)
        self.cible.Attaquer(attaque)
        self.chargement = 0

class GolemFeu(Golem):
    ATTAQUE_BOULE_FEU = "attaque boule de feu"
    attaque_max_distance : float = 4.0
    boule_feu_dégats : int = 3

    def __init__(self):
        super().__init__()
    
    def _commandeAttaqueSpéciale(self, commande):
        if commande.attaque_spéciale == self.ATTAQUE_BOULE_FEU and distance(self.pos,commande.ennemi_cible.pos) <= self.attaque_normale_dégats:
            attaque = Attaque(self)
            attaque.élément = Élément.FEU
            attaque.est_projectile = True
            attaque.distance = distance(self.pos, commande.ennemi_cible.pos)
            attaque.direction = commande.ennemi_cible.pos - self.pos
            attaque.dégats = self.boule_feu_dégats + self.attaque_chargée*self.chargement
            commande.ennemi_cible.Attaquer(attaque)
    
    def _AttaquerEnnemi(self):
        attaque = Attaque(self)
        attaque.dégats = self.attaque_normale_dégats + self.attaque_chargée*self.chargement
        attaque.élément = Élément.FEU
        self.cible.Attaquer(attaque)
        self.chargement = 0
