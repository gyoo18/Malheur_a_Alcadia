from typing_extensions import Self
import interface
from Ressources import Ressources
import os

class ÉtatJeu:
    MENU = "menu"
    MENU_CONTEXTUEL = "menu contextuel"
    JEU = "jeu"
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

class Jeu:

    def __init__(self):
        self.état : ÉtatJeu = ÉtatJeu()    # Indique l'état du jeu
        self.chapitre : Chapitre = Chapitre()   # Indique le chapitre scénaristique actuel et la zone.
        self.choix : str = ""       # Décrit le choix que le joueur a fait à la fin du niveau s'il y a lieu

    def miseÀJour(self):
        import menu
        res = Ressources.avoirRessources()
        os.system("cls" if os.name == 'nt' else "clear")
        if self.état.v == ÉtatJeu.JEU:
            res = Ressources.avoirRessources()
            print("Mise à jour des entitées.")
            for i in range(len(res.cartes[0].entités)):
                res.cartes[0].entités[i]._MiseÀJourIA()
            print("Entitées mises à jours.")

        if self.état.v == ÉtatJeu.MENU:
            menu.displayUI(res.cartes[0],self)
        elif self.état.v == ÉtatJeu.MENU_CONTEXTUEL:
            pass # TODO #11 Implémenter les menus contextuels
        else :
            menu.ingameUI(res.cartes[0],self)

        if self.état.v == ÉtatJeu.JEU:
            paysans = False
            golems = False
            for e in res.cartes[0].entités:
                if e.camp == "Golems":
                    golems = True
                
                if e.camp == "Paysans":
                    paysans = True
            
            if not paysans:
                self.état.v = ÉtatJeu.SUCCÈS
            elif not golems:
                self.état.v = ÉtatJeu.ÉCHEC
        
        if self.état.v == ÉtatJeu.TRANSITION:
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
        
        