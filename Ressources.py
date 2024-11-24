from Carte.class_carte import Carte
from Entités.Entité import Entité
from typing_extensions import Self

class Ressources:
    cartes : list[Carte] = []
    entités : list[Entité] = []

    ressources : Self = None

    resultat_zone_2 : str = ""

    def __init__(self):
        pass

    def avoirRessources():
        if Ressources.ressources == None:
            Ressources.ressources = Ressources()
        return Ressources.ressources
    
    def détruire(self):
        pass