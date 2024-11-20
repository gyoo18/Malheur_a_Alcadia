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
         ATT=int(random.choice(range(10,16)))
         DEF=int(random.choice(range(39,46)))
         
class water_golems(Golem):
    def Stats_water_golem():
        HP=90
        ATT=int(random.choice(range(20,26)))
        DEF=int(random.choice(range(25,31)))

class Fire_Golem(Golem):
     def Stats_Fire_golem():
         HP=120
         ATT=int(random.choice(range(26,29)))
         DEF=int(random.choice(range(35,39)))
    