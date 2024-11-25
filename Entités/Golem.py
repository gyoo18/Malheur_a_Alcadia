from Entités.Entité import *
import random

class Commande:
    def __init__():
        pass

class Golem(Entité):

    def __init__(self):
        super().__init__()

    def commande(self, commande : Commande):
        pass

class Earth_golem(Golem):
    def __init__(self):
        super().__init__()

    def Stats_Earth_golem():
         HP=150
         ATT=Entité.Random_Stats(10,16)
         DEF=Entité.Random_Stats(39,46)
         
class water_golems(Golem):
    def Stats_water_golem():
        HP=90
        ATT=Entité.Random_Stats(20,26)
        DEF=Entité.Random_Stats(25,31)

class Fire_Golem(Golem):
     def Stats_Fire_golem():
         HP=120
         ATT=Entité.Random_Stats(26,29)
         DEF=Entité.Random_Stats(35,39)
    