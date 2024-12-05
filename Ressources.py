from Carte.class_carte import Carte
from Entités.Entité import Entité
from typing_extensions import Self

class Ressources:

    ressources : Self = None

    def __init__(self):
        self.cartes : list[Carte] = []
        self.entités : list[Entité] = []
        self.resultat_zone_2 : str = ""

    def avoirRessources():
        if Ressources.ressources == None:
            Ressources.ressources = Ressources()
        return Ressources.ressources
    
    def détruire(self):
        pass