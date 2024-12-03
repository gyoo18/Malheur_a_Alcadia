from OpenGL.GL import *
from Dessin.Nuanceurs.Nuanceur import Nuanceur
from Maths.Matrice import Matrice
import glm

class NuaBase(Nuanceur):
    MATRICE : int
    COLOR : int

    def __init__(self,source : str):
        super().__init__(source)

    def construire(self):
        super().construire()

        glUseProgram(self.programme)
        
        glBindAttribLocation(self.programme,0,"POS")
        glBindAttribLocation(self.programme,1,"NORM")
        glBindAttribLocation(self.programme,2,"UV")

        self.MATRICE = glGetUniformLocation(self.programme,"matrice")
        self.COLOR = glGetUniformLocation(self.programme,"color")

        glUseProgram(0)

    def chargerMatrice(self, matrice : Matrice):
        glUniformMatrix4fv(self.MATRICE,1,GL_FALSE,matrice.mat)

    def chargerColor(self, color):
        glUniform1f(self.COLOR,glm.float32(color))