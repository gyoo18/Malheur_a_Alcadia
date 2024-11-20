from typing_extensions import Self
import interface

class ÉtatJeu:
    MENU = "menu"
    ZONE1 = "zone1"
    ZONE2 = "zone2"
    ZONE3 = "zone3"
    TERMINÉ = "terminé"

    v : str

    def __init__(self, valeur = ZONE1):
        self.v = valeur

class Jeu:
    état : ÉtatJeu

    def __init__(self):
        self.état = ÉtatJeu(ÉtatJeu.ZONE1)

    def miseÀJour(self):
        interface.miseÀJour(self)