from __future__ import annotations
from typing_extensions import Self
from Maths.Vec2 import Vec2
from InclusionsCirculaires.Entité_Attaque import *

class Élément:
    TERRE = "terre"
    PIERRE = "pierre"
    FEU = "feu"
    EAU = "eau"
    AIR = "air"

    def __init__(self, valeur = TERRE):
        self.v : str = valeur

# Décrit une attaque et ses composantes
class Attaque:

    def __init__(self, provenance : Entité):
        self.provenance : Entité = provenance

        self.dégats : float = 0 # Dégats infligés à l'ennemi

        self.est_projectile = False
        self.distance : float = 1.0
        self.élément : Élément = None
        self.repousse : int = 0
        self.direction : Vec2 = Vec2(0)