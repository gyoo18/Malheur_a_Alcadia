from typing_extensions import Self
from Maths.Vec2 import Vec2
from Entités.Entité import Entité

class Élément:
    TERRE = "terre"
    PIERRE = "pierre"
    FEU = "feu"
    EAU = "eau"
    AIR = "air"

    v : str

    def __init__(self, valeur = TERRE):
        self.v = valeur

# Décrit une attaque et ses composantes
class Attaque:

    provenance : Entité = None

    dégats : float # Dégats infligés à l'ennemi

    est_projectile = False
    distance : float = 1.0
    élément : Élément = None
    repousse : int = 0
    direction : Vec2 = Vec2(0)

    def __init__(self, provenance : Entité):
        self.dégats = 0
        self.provenance = provenance