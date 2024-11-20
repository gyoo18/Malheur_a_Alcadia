from Entités.Entité import *
import random
def Random_Stats(x,y):
    Stats=int(random.choice(range(x,y)))
    return Stats

class Ennemi(Entité):

    def __init__(self):
        super().__init__()

class Child_1(Ennemi):
    def Stats_Child_1():
        HP=50
        ATT=Random_Stats(8,15)
        DEF=Random_Stats(5,11)

class Miners(Ennemi):
    def Stats_Miners():
        HP=75
        ATT=Random_Stats(14,21)
        DEF=Random_Stats(10,16)

class Child_2(Ennemi):
    def Stats_Child_2():
        HP=75
        ATT=Random_Stats(12,17)
        DEF=Random_Stats(12,15)

class Knight(Ennemi):
    def Stats_Knight():
        HP=125
        ATT=Random_Stats(19,26)
        DEF=Random_Stats(30,36)

class Gunner(Ennemi):
    def Stats_Gunner():
        HP=50
        ATT=Random_Stats(30,33)
        DEF=Random_Stats(5,11)