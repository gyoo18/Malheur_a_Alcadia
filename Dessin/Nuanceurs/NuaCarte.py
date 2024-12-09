from Dessin.Nuanceurs.Nuanceur import Nuanceur
from Maths.Vec2 import Vec2
from OpenGL.GL import *
from glm import float32

class NuaCarte(Nuanceur):

    def __init__(self,sommets_source,fragments_source):
        super().__init__(sommets_source,fragments_source)
        self.POSITION = -1
        self.ROTATION = -1
        self.TAILLE_FENÊTRE = -1
        self.ÉCHELLE = -1

    def construire(self):
        super().construire()

        self.démarrer()

        glBindAttribLocation(self.programme,0,"i_pos")

        self.POSITION = glGetUniformLocation(self.programme,"pos")
        self.ROTATION = glGetUniformLocation(self.programme,"rot")
        self.TAILLE_FENÊTRE = glGetUniformLocation(self.programme,"taille_fenetre")
        self.ÉCHELLE = glGetUniformLocation(self.programme,"ech")
        self.TAILLE_CARTE = glGetUniformLocation(self.programme,"taille_carte")
        self.INDEXES_TEXTURE = glGetUniformLocation(self.programme,"indexes_texture")
        self.TAILLE_ATLAS = glGetUniformLocation(self.programme,"taille_atlas")

        glUniform1i(glGetUniformLocation(self.programme,"tex"),0)

    def chargerUniformes(self, position : Vec2, rot : float, échelle : Vec2, taille_fenetre : Vec2, taille_carte : Vec2, indexes_texture : list[int], taille_atlas : Vec2):
        glUniform2f(self.POSITION,float32(position.x),float32(position.y))
        glUniform1f(self.ROTATION,float32(rot))
        glUniform2f(self.ÉCHELLE,float32(échelle.x),float32(échelle.y))
        glUniform2f(self.TAILLE_FENÊTRE,float32(taille_fenetre.x),float32(taille_fenetre.y))
        glUniform2i(self.TAILLE_CARTE,int(taille_carte.x),int(taille_carte.y))
        données = (GLint * len(indexes_texture))(*indexes_texture)
        glUniform1iv(self.INDEXES_TEXTURE,len(indexes_texture),données)
        glUniform2i(self.TAILLE_ATLAS,int(taille_atlas.x),int(taille_atlas.y))