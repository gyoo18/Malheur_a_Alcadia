from typing_extensions import Self
from Ressources import Ressources
from Carte.Carte import Carte
import os
from Entités.Entité import Entité
from Entités.Golem import Golem
import copy

class ÉtatJeu:
    MENU = "menu"
    MENU_CONTEXTUEL = "menu contextuel"
    JEU = "jeu"
    FIN_TOUR = "fin de tour"
    DÉBUT = "début"
    CHOIX = "choix"
    SUCCÈS = "succès"
    ÉCHEC = "échec"
    TRANSITION = "transition"
    TERMINÉ = "terminé"

    def __init__(self, valeur = MENU):
        self.v : str = valeur

class Chapitre:
    INTRODUCTION = "Introduction"
    CHAPITRE1 = "Prairie"
    CHAPITRE2 = "Cité"
    CHAPITRE3 = "Château"

    def __init__(self, valeur = INTRODUCTION):
        self.v : str = valeur

class MenuContextuel:
    AIDE = "aide"   # Menu d'aide aux commandes
    COMBAT = "combat"   # Menu d'état du combat
    INFO = "info"   # Menu d'état des entités
    SELECT = "select"   # Menu de commande des golems

    def __init__(self, valeur = AIDE):
        from Entités.Entité import Entité
        self.v = valeur
        self.menu_entité_entité : Entité = None
        self.menu_historique : list[str] = []
        self.menu_select_entité : Golem = None

class Jeu:
    jeu : Self = None

    def __init__(self):
        self.état : ÉtatJeu = ÉtatJeu()    # Indique l'état du jeu
        self.chapitre : Chapitre = Chapitre()   # Indique le chapitre scénaristique actuel et la zone.
        self.choix : str = ""       # Décrit le choix que le joueur a fait à la fin du niveau s'il y a lieu
        self.menu : MenuContextuel = MenuContextuel() # Décrit le menu contextuel ouvert ou précédemment ouvert.
        self.carte : Carte = None
    
    def avoirJeu():
        if Jeu.jeu == None:
            Jeu.jeu = Jeu()
        return Jeu.jeu

    def miseÀJour(self):
        import menu
        res = Ressources.avoirRessources()

        if self.état.v == ÉtatJeu.MENU:
            menu.displayUI()
        elif self.état.v == ÉtatJeu.MENU_CONTEXTUEL:
            menu.menu_contextuel()
        else :
            menu.ingameUI()

        os.system("cls" if os.name == 'nt' else "clear")
        if self.état.v == ÉtatJeu.FIN_TOUR:
            paysans = False
            golems = False
            for e in self.carte.entités:
                if e.camp == "Golems":
                    golems = True
                
                if e.camp == "Paysans":
                    paysans = True
            
            if not paysans:
                self.état.v = ÉtatJeu.SUCCÈS
            elif not golems:
                self.état.v = ÉtatJeu.ÉCHEC
            else :
                print("Mise à jour des entitées.")
                for i in range(len(self.carte.entités)):
                    self.carte.entités[i]._MiseÀJourIA()
                lo = len(self.carte.entités) -1
                for i in range(len(self.carte.entités)):
                    if not self.carte.entités[lo-i].estVivant:
                        self.carte.entités.pop(lo-i)
                print("Entitées mises à jours.")
                self.état.v = ÉtatJeu.JEU
        
        elif self.état.v == ÉtatJeu.TRANSITION:
            self.état.v = ÉtatJeu.DÉBUT
            match self.chapitre.v:
                case Chapitre.INTRODUCTION:
                    self.chapitre.v = Chapitre.CHAPITRE1
                case Chapitre.CHAPITRE1:
                    self.chapitre.v = Chapitre.CHAPITRE2
                case Chapitre.CHAPITRE2:
                    self.chapitre.v = Chapitre.CHAPITRE3
                case Chapitre.CHAPITRE3:
                    self.chapitre.v = Chapitre.INTRODUCTION
            self.changerCarte(res.chargerCarte(self.carte.prochaine))

    def changerCarte(self,carte : Carte):
        res = Ressources.avoirRessources()
        if self.carte != None:
            del self.carte
        self.carte = copy.deepcopy(carte)
        for i in range(len(self.carte.entités)):
            self.carte.entités[i].carte = self.carte
            self.carte.entités[i].pos = carte.positions_entitées_initiales[i]
        joueur = copy.deepcopy(res.joueur)
        joueur.pos = self.carte.joueur_pos_init
        joueur.carte = self.carte
        self.carte.entités.append(joueur)
        
        