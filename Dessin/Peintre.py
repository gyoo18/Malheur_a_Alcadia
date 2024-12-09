from OpenGL.GL import *
from OpenGL.GLU import *

from Dessin.Image import Image
from Dessin.Maillage import Maillage
from Maths.Vec2 import Vec2

from tkinter_gl import GLCanvas

from Carte.Carte import Carte
from GestionnaireRessources import Ressources

class Peintre(GLCanvas):

    def __init__(self, parent):
        super().__init__(parent)
        print("Création du peintre.")
        res = Ressources.avoirRessources()
        self.hauteure : int = 0
        self.largeure : int = 0
        self.couleur_arrière_plan = (0.2,0.5,0.8)
        self.carte : Carte = res.chargerCarte("Test")
        self.initialisé = False
        print("Peintre créé.")
    
    def initialiser(self,largeure : int, hauteure : int):
        print("Couleur arrière-plan : ", self.couleur_arrière_plan)
        glClearColor(self.couleur_arrière_plan[0],self.couleur_arrière_plan[1],self.couleur_arrière_plan[2],1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.carte.dessin_construire()
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

        self.carte.dessin_nuanceur.démarrer()

        glBindVertexArray(self.carte.dessin_maillage.vao)
        for i in range(len(self.carte.dessin_maillage.attributs)):
            glEnableVertexAttribArray(i)

        indexes_texture = [
            0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
            0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
            0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
            0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
            0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
            0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
            0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
            0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
            0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
            0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
            0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
            0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
            0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
            0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
            0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
            0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        ]
        self.carte.dessin_nuanceur.chargerUniformes(self.carte.dessin_position, self.carte.dessin_rotation, self.carte.dessin_taille*self.carte.dessin_échelle, Vec2(self.largeure,self.hauteure), Vec2(self.carte.colonnes,self.carte.lignes),indexes_texture,Vec2(4,4),Vec2(64,64))

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D,self.carte.dessin_atlas.ID)
        
        match self.carte.dessin_maillage.mode_dessin:
            case Maillage.MODE_DESSIN_INDEXES:
                glDrawElements(GL_TRIANGLES,self.carte.dessin_maillage.n_sommets,GL_UNSIGNED_INT,None)
            case Maillage.MODE_DESSIN_LISTE:
                glDrawArrays(GL_TRIANGLES,0,self.carte.dessin_maillage.n_sommets)
            case Maillage.MODE_DESSIN_ÉVENTAIL:
                glDrawArrays(GL_TRIANGLE_FAN,0,self.carte.dessin_maillage.n_sommets)
            case Maillage.MODE_DESSIN_BANDE:
                glDrawArrays(GL_TRIANGLE_STRIP,0,self.carte.dessin_maillage.n_sommets)
        
        error = glGetError()
        if error != GL_NO_ERROR:
            print("[GLError] :",gluErrorString(error))

        self.swap_buffers()