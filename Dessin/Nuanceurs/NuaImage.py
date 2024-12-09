from Dessin.Nuanceurs.Nuanceur import Nuanceur
from OpenGL.GL import *
from Maths.Vec2 import Vec2
from glm import float32

class NuaImage(Nuanceur):

    def __init__(self,sommets_source : str, fragments_source : str,):
        super().__init__(sommets_source, fragments_source)
        self.POSITION : int = -1
        self.ROTATION : int = -1
        self.TAILLE_FENÊTRE : int= -1
        self.ÉCHELLE  : int= -1

    def construire(self):
        super().construire()

        self.démarrer()

        glBindAttribLocation(self.programme,0,"i_pos")

        self.POSITION = glGetUniformLocation(self.programme,"pos")
        self.ROTATION = glGetUniformLocation(self.programme,"rot")
        self.TAILLE_FENÊTRE = glGetUniformLocation(self.programme,"taille_fenetre")
        self.ÉCHELLE = glGetUniformLocation(self.programme,"ech")

        glUniform1i(glGetUniformLocation(self.programme,"tex"),0)

    def chargerUniformes(self, position : Vec2, rot : float, échelle : Vec2, taille_fenetre : Vec2):
        glUniform2f(self.POSITION,float32(position.x),float32(position.y))
        glUniform1f(self.ROTATION,float32(rot))
        glUniform2f(self.ÉCHELLE,float32(échelle.x),float32(échelle.y))
        glUniform2f(self.TAILLE_FENÊTRE,float32(taille_fenetre.x),float32(taille_fenetre.y))
