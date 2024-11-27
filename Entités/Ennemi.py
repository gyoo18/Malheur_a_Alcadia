from Entités.Entité import *
import random


class Ennemi(Entité):

    def __init__(self):
        super().__init__()

    def AttaquerEnnemi(self):
        match self.étatCombat.v:
            case ÉtatCombat.CHARGER:
                self.chargement += 1
                if self.chargement >= self.TEMP_CHARGEMENT:
                    attaque = Attaque()
                    attaque.dégats = 1.0*self.attaque_chargée
                    self.ennemi.Attaquer(attaque)

            case ÉtatCombat.DÉFENSE:
                if self.ennemi.étatCombat.v != ÉtatCombat.CHARGER:
                    self.étatCombat.v = ÉtatCombat.LIBRE

            case ÉtatCombat.LIBRE:
                match self.ennemi.étatCombat.v:
                    case ÉtatCombat.LIBRE:
                        attaque = Attaque()
                        attaque.dégats = 1.0
                        self.ennemi.Attaquer(attaque)

                    case ÉtatCombat.DÉFENSE:
                        self.étatCombat = ÉtatCombat.CHARGER

                    case ÉtatCombat.CHARGER:
                        self.étatCombat = ÉtatCombat.DÉFENSE
    

class Child_1(Ennemi):
   
    Entité.Stats()
    HP=75
    ATT=Entité.Random_Stats(8,11)
    DEF=Entité.Random_Stats(5,11)

class Miners(Ennemi):
    
    Entité.Stats()
    HP=75
    ATT=Entité.Random_Stats(14,21)
    DEF=Entité.Random_Stats(10,16)

class Child_2(Ennemi):

        HP=75
        ATT=Entité.Random_Stats(12,17)
        DEF=Entité.Random_Stats(12,15)

class Knight(Ennemi):
    
        HP=125
        ATT=Entité.Random_Stats(19,26)
        DEF=Entité.Random_Stats(30,36)

class Gunner(Ennemi):
    
        HP=50
        ATT=Entité.Random_Stats(30,33)
        DEF=Entité.Random_Stats(5,11)