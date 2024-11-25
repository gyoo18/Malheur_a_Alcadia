from typing_extensions import Self
import random

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
    def Stats():
        HP=0
        ATT=1
        DEF=1

    def Random_Stats(x,y):
        Stats=int(random.choice(range(x,y)))
        return Stats

    def __init__(self):
        pass

    def MiseÀJourIA(self):
        Nombre_Tours=Nombre_Tours+1
        if Nombre_Tours==1:
            #Run les stats des golems + leur nom
            
        pass
    
    def AttaquerEnnemi(self):
        Dm=
       
        pass

    def Attaquer(self, attaque : Attaque):
        pass

    def Défense(self, attaque : Attaque):
        
        attaque=attaque-attaque*DEF/100
        return attaque