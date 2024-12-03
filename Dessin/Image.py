from Dessin.Maillage import Maillage
from Dessin.Nuanceurs.NuaImage import NuaImage
from Dessin.Texture import Texture
from Maths.Vec2 import Vec2

class Image:
    pos : Vec2
    rot : float
    taille : Vec2
    échelle : Vec2

    points : list[float] = [
        -1.0,-1.0,
         1.0,-1.0,
        -1.0, 1.0,
         1.0, 1.0
    ]
    nuanceur : NuaImage
    maillage : Maillage
    image : Texture

    def __init__(self, texture : str):
        self.pos = Vec2(0,0)
        self.rot = 0
        self.échelle = Vec2(1,1)
        self.maillage = Maillage()
        self.maillage.créer_bande([self.points],[2])
        self.nuanceur = NuaImage("Ressources/Nuanceurs/NuaImage")
        self.image = Texture(texture)
        self.taille = Vec2(self.image.largeur,self.image.hauteur)

    def construire(self):
        self.maillage.construire()
        self.nuanceur.construire()
        self.image.construire()