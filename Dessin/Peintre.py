from OpenGL.GL import *
from OpenGL.GLU import *
import time

from Dessin.Nuanceurs.NuaBase import NuaBase
from Ressources import Ressources
from Dessin.Maillage import Maillage
import math
from Maths.Matrice import Matrice
from Maths.Vec2 import Vec2
import glm
from Dessin.Image import Image

class Peintre:
    hauteure : int
    largeure : int
    couleur_arrière_plan : tuple[float]

    image :Image
    
    initialisé : bool
    def __init__(self):
        print("Peintre créé.")
        self.couleur_arrière_plan = (0.2,0.5,0.8)
        # self.nuanceur = NuaBase("Dessin/Ressources/Nuanceurs/NuaBase")
        # self.maillage = Ressources.avoirRessources().chargerObj("Dessin/Ressources/Maillages/cube.obj")
        # self.trans = Matrice().positionner(Vec3(0,0,3.0))
        # self.rot = Matrice()
        self.image = Image()
        self.initialisé = False
    
    def initialiser(self,largeure : int, hauteure : int):
        print("Couleur arrière-plan : ", self.couleur_arrière_plan)
        glClearColor(self.couleur_arrière_plan[0],self.couleur_arrière_plan[1],self.couleur_arrière_plan[2],1.0)
        glEnable(GL_DEPTH_TEST)

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

    def dessiner(self):
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