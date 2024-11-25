from Entités.Entité import *
import random


class Ennemi(Entité):

    def __init__(self):
        super().__init__()
    

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