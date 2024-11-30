from typing_extensions import Self
import interface
import menu
from Ressources import Ressources

class ÉtatJeu:
    MENU = "menu"
    INTRODUCTION = "introduction"
    ZONE1 = "zone1"
    ZONE2 = "zone2"
    ZONE3 = "zone3"
    TERMINÉ = "terminé"

    def __init__(self, valeur = INTRODUCTION):
        self.v : str = valeur

class Jeu:

    def __init__(self):
        self.état : ÉtatJeu = ÉtatJeu(ÉtatJeu.ZONE1)

    def miseÀJour(self):
        res = Ressources.avoirRessources()
        menu.displayUI(res.cartes[0])
        # interface.miseÀJour(self)