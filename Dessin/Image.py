from Dessin.Maillage import Maillage
from Dessin.Nuanceurs.NuaImage import NuaImage
from Dessin.Texture import Texture
from Maths.Vec2 import Vec2
from GestionnaireRessources import Ressources

class Image:

    points : list[float] = [
        -1.0,-1.0,
         1.0,-1.0,
        -1.0, 1.0,
         1.0, 1.0
    ]

    def __init__(self, texture : str):
        res = Ressources.avoirRessources()
        self.pos : Vec2 = Vec2(0,0)
        self.rot : float = 0
        self.échelle : Vec2 = Vec2(1,1)
        self.maillage : Maillage = Maillage()
        self.maillage.créer_bande([self.points],[2])
        self.nuanceur : NuaImage = res.chargerNuanceur("NuaImage",NuaImage)
        self.image : Texture = res.chargerTexture(texture)
        self.taille : Vec2 = Vec2(self.image.largeur,self.image.hauteur)

    def construire(self):
        self.maillage.construire()
        self.nuanceur.construire()
        self.image.construire()