from OpenGL.GL import *
from OpenGL.GLU import *

from Dessin.Image import Image
from Dessin.Maillage import Maillage
from Maths.Vec2 import Vec2

from tkinter_gl import GLCanvas

from Carte.Carte import Carte
from GestionnaireRessources import Ressources
from Jeu import Jeu

class Peintre(GLCanvas):

    def __init__(self, parent):
        from Entités.Golem import GolemEau, GolemFeu, GolemDoré
        super().__init__(parent)
        print("Création du peintre.")
        res = Ressources.avoirRessources()
        self.hauteure : int = 0
        self.largeure : int = 0
        self.couleur_arrière_plan = (0.8,0.8,0.8)
        self.carte : Carte = res.chargerCarte("Test")
        gE = GolemEau()
        gF = GolemFeu()
        gD = GolemDoré()
        gE.pos = Vec2(7,7)
        gF.pos = Vec2(3,3)
        gD.pos = Vec2(4,12)
        self.carte.entités.append(gE)
        self.carte.entités.append(gF)
        self.carte.entités.append(gD)

        jeu = Jeu.avoirJeu()
        jeu.changerCarte(self.carte)
        self.carte = jeu.carte
        self.initialisé = False
        print("Peintre créé.")
    
    def initialiser(self,largeure : int, hauteure : int):
        print("Couleur arrière-plan : ", self.couleur_arrière_plan)
        glClearColor(self.couleur_arrière_plan[0],self.couleur_arrière_plan[1],self.couleur_arrière_plan[2],1.0)
        #glEnable(GL_DEPTH_TEST)
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
        taille = min(largeure,hauteure)
        self.carte.dessin_taille = Vec2(taille, taille)

    def draw(self):
        if not self.initialisé:
            self.initialiser(self.winfo_width(),self.winfo_height())
        if self.winfo_width != self.largeure or self.winfo_height != self.hauteure:
            self.surModificationFenetre(self.winfo_width(), self.winfo_height())

        self.make_current()

        glClear(GL_COLOR_BUFFER_BIT)

        self.carte.dessin_nuanceur.démarrer()

        glBindVertexArray(self.carte.dessin_maillage.vao)
        for i in range(len(self.carte.dessin_maillage.attributs)):
            glEnableVertexAttribArray(i)

        self.carte.dessin_nuanceur.chargerUniformes(self.carte.dessin_position, self.carte.dessin_rotation, self.carte.dessin_taille*self.carte.dessin_échelle, Vec2(self.largeure,self.hauteure), Vec2(self.carte.colonnes,self.carte.lignes),self.carte.dessin_atlas_indexes,self.carte.dessin_atlas_taille)

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

        for i in range(len(self.carte.entités)):
            if self.carte.entités[i].dessin_Image != None:
                entité = self.carte.entités[i]
                image = self.carte.entités[i].dessin_Image
                image.nuanceur.démarrer()

                glBindVertexArray(image.maillage.vao)
                for i in range(len(image.maillage.attributs)):
                    glEnableVertexAttribArray(i)

                image.taille = self.carte.dessin_taille/Vec2(self.carte.colonnes,self.carte.lignes)
                image.pos = ((entité.pos+Vec2(0.5))/Vec2(self.carte.colonnes,self.carte.lignes)*2.0 - 1.0)*self.carte.dessin_taille
                image.pos.y = -image.pos.y

                image.nuanceur.chargerUniformes(image.pos, image.rot, image.taille*image.échelle, Vec2(self.largeure,self.hauteure))

                glActiveTexture(GL_TEXTURE0)
                glBindTexture(GL_TEXTURE_2D,image.image.ID)
                
                match image.maillage.mode_dessin:
                    case Maillage.MODE_DESSIN_INDEXES:
                        glDrawElements(GL_TRIANGLES,image.maillage.n_sommets,GL_UNSIGNED_INT,None)
                    case Maillage.MODE_DESSIN_LISTE:
                        glDrawArrays(GL_TRIANGLES,0,image.maillage.n_sommets)
                    case Maillage.MODE_DESSIN_ÉVENTAIL:
                        glDrawArrays(GL_TRIANGLE_FAN,0,image.maillage.n_sommets)
                    case Maillage.MODE_DESSIN_BANDE:
                        glDrawArrays(GL_TRIANGLE_STRIP,0,image.maillage.n_sommets)

        error = glGetError()
        if error != GL_NO_ERROR:
            print("[GLError] :",gluErrorString(error))

        self.swap_buffers()