from OpenGL.GL import *
from OpenGL.GLU import *

from Dessin.Image import Image
from Dessin.Maillage import Maillage
from Maths.Vec2 import Vec2

from tkinter_gl import GLCanvas

class Peintre(GLCanvas):
    hauteure : int
    largeure : int
    couleur_arrière_plan : tuple[float]

    image :Image
    
    initialisé : bool
    def __init__(self, parent):
        super().__init__(parent)
        print("Peintre créé.")
        self.couleur_arrière_plan = (0.2,0.5,0.8)
        # self.nuanceur = NuaBase("Dessin/Ressources/Nuanceurs/NuaBase")
        # self.maillage = Ressources.avoirRessources().chargerObj("Dessin/Ressources/Maillages/cube.obj")
        # self.trans = Matrice().positionner(Vec3(0,0,3.0))
        # self.rot = Matrice()
        self.image = Image("Test")
        self.initialisé = False
    
    def initialiser(self,largeure : int, hauteure : int):
        print("Couleur arrière-plan : ", self.couleur_arrière_plan)
        glClearColor(self.couleur_arrière_plan[0],self.couleur_arrière_plan[1],self.couleur_arrière_plan[2],1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # self.nuanceur.construire()
        # self.maillage.construire()
        self.image.construire()
        self.largeure = largeure
        self.hauteure = hauteure

        # glPointSize(4)
        glViewport(0,0,largeure, hauteure)
        self.initialisé = True
        print("Peintre Initialisé")

        error = glGetError()
        if error != GL_NO_ERROR:
            print("[GLError] :",gluErrorString(error))
    
    def surModificationFenetre(self,largeure : int, hauteure : int):
        glViewport(0,0,largeure,hauteure)
        self.largeure = largeure
        self.hauteure = hauteure

    def draw(self):
        if not self.initialisé:
            self.initialiser(self.winfo_width(),self.winfo_height())
        if self.winfo_width != self.largeure or self.winfo_height != self.hauteure:
            self.surModificationFenetre(self.winfo_width(), self.winfo_height())

        self.make_current()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # self.nuanceur.démarrer()

        # f = 100.0
        # n = 0.01
        # perspective = Matrice().fairePerspective(0.01, 100.0, 70.0, self.largeure/self.hauteure)
        # from math import cos,sin
        # x = 0.001
        # y = 0.001
        # z = 0.001
        # self.rot.tourner(Vec3(0.001))
        # matrice = perspective*self.trans*self.rot
        # self.nuanceur.chargerMatrice(matrice)

        # self.nuanceur.chargerColor(1.0)

        self.image.nuanceur.démarrer()

        glBindVertexArray(self.image.maillage.vao)
        for i in range(len(self.image.maillage.attributs)):
            glEnableVertexAttribArray(i)

        self.image.nuanceur.chargerUniformes(self.image.pos, self.image.rot, self.image.taille*self.image.échelle, Vec2(self.largeure,self.hauteure))

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D,self.image.image.ID)
        
        match self.image.maillage.mode_dessin:
            case Maillage.MODE_DESSIN_INDEXES:
                glDrawElements(GL_TRIANGLES,self.image.maillage.n_sommets,GL_UNSIGNED_INT,None)
            case Maillage.MODE_DESSIN_LISTE:
                glDrawArrays(GL_TRIANGLES,0,self.image.maillage.n_sommets)
            case Maillage.MODE_DESSIN_ÉVENTAIL:
                glDrawArrays(GL_TRIANGLE_FAN,0,self.image.maillage.n_sommets)
            case Maillage.MODE_DESSIN_BANDE:
                glDrawArrays(GL_TRIANGLE_STRIP,0,self.image.maillage.n_sommets)
        
        error = glGetError()
        if error != GL_NO_ERROR:
            print("[GLError] :",gluErrorString(error))

        self.swap_buffers()