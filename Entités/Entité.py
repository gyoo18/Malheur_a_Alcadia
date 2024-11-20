from typing_extensions import Self

class État:
    POURSUITE = "poursuite"
    RECHERCHE = "recherche"
    COMBAT = "combat"
    DÉPLACEMENT = "déplacement"
    IMMOBILE = "immobile"

    v : str

    def __init__(self, valeur = Self.RECHERCHE):
        self.v = valeur

class ÉtatCombat:
    LIBRE = "libre"
    DÉFENSE = "défense"
    CHARGER = "charger"

    v : str

    def __init__(self, valeur = Self.LIBRE):
        self.v = valeur

class Attaque:

    def __init__(self):
        pass

class Entité:

    état : État

    def __init__(self):
        pass

    def MiseÀJourIA(self):
        pass
    
    def AttaquerEnnemi(self):
        pass

    def Attaquer(self, attaque : Attaque):
        pass

    def Défense(self, attaque : Attaque):
        return attaque