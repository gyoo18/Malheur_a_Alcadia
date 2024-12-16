from __future__ import annotations
from OpenGL.GL import *
from OpenGL.GLU import *

from Dessin.Maillage import Maillage
from Maths.Vec2 import Vec2
from Maths.Vec4 import Vec4

from Carte.Carte import Carte
from InclusionsCirculaires.Jeu_Peintre import *

import tkinter
import sys
import os

class Peintre(tkinter.Widget, tkinter.Misc):

    def __init__(self, parent, cnf={}, **kw):
        print("Création du peintre.")
        self.hauteure_visuelle : int = 0
        self.largeure_visuelle : int = 0
        self.largeure_physique : int = 0
        self.hauteure_physique : int = 0
        self.couleur_arrière_plan = (0.098,0.102,0.118)
        self.carte : Carte = None
        self.initialisé = False
        self.estVisible = False

        # !==== Code copié de la librairie tkinter-gl ====!

        if sys.platform == 'win32':
            # Make sure the parent has been mapped.
            parent.update()
        pkg_dir = "TkGL/"+str(sys.platform)
        if not os.path.exists(pkg_dir):
            raise RuntimeError('TkGL package directory "%s" is missing.' % pkg_dir)
        parent.tk.call('lappend', 'auto_path', pkg_dir)
        parent.tk.call('package', 'require', 'Tkgl')

        tkinter.Widget.__init__(self, parent, 'tkgl', cnf, kw)
        
        # !==== Code copié de la librairie tkinter-gl ====!

        self.bind("<Map>",self.initialiser)
        self.bind("<Expose>",self.surModificationFenetre)
        self.bind("<Visibility>",self.surModificationFenetre)
        self.bind("<Configure>",self.surModificationFenetre)

        # self.bind("<Enter>",self.surCurseurEntrer)
        self.bind("<Leave>",self.surCurseurSortir)
        self.bind("<Motion>",self.surCurseurMouvement)
        self.bind("<Button-1>",self.surClique)

        print("Peintre créé.")
    
    def initialiser(self,event):
        print("Couleur arrière-plan : ", self.couleur_arrière_plan)
        glClearColor(self.couleur_arrière_plan[0],self.couleur_arrière_plan[1],self.couleur_arrière_plan[2],0.0)
        #glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.largeure_visuelle = self.winfo_width()
        self.hauteure_visuelle = self.winfo_height()
        self.largeure_physique = self.winfo_width()
        self.hauteure_physique = self.winfo_height()

        glViewport(0,0,self.largeure_visuelle, self.hauteure_visuelle)
        self.initialisé = True
        print("Peintre Initialisé")

        error = glGetError()
        if error != GL_NO_ERROR:
            print("[GLError] :",gluErrorString(error))
    
    def surModificationFenetre(self,event):
        self.largeure_physique = self.winfo_width()
        self.hauteure_physique = self.winfo_height()
        if self.carte != None:
            facteur_x = self.largeure_physique/self.carte.colonnes
            facteur_y = self.hauteure_physique/self.carte.lignes
            facteur = min(facteur_x,facteur_y)
            self.largeure_visuelle = int(facteur*self.carte.colonnes)
            self.hauteure_visuelle = int(facteur*self.carte.lignes)
        else:
            self.largeure_visuelle = self.largeure_physique
            self.hauteure_visuelle = self.hauteure_physique
        glViewport((self.largeure_physique-self.largeure_visuelle)//2,(self.hauteure_physique-self.hauteure_visuelle)//2,self.largeure_visuelle,self.hauteure_visuelle)
        self.carte.dessin_taille = Vec2(self.largeure_visuelle, self.hauteure_visuelle)

    def peindre(self):
        self.make_current()

        glClear(GL_COLOR_BUFFER_BIT)

        for e in self.carte.entités:
            if not e.dessin_Image.estConstruit:
                e.dessin_Image.construire()

        self.carte.dessin_nuanceur.démarrer()

        glBindVertexArray(self.carte.dessin_maillage.vao)
        for i in range(len(self.carte.dessin_maillage.attributs)):
            glEnableVertexAttribArray(i)

        self.carte.dessin_nuanceur.chargerUniformes(self.carte.dessin_position, self.carte.dessin_rotation, self.carte.dessin_taille*self.carte.dessin_échelle, Vec2(self.largeure_visuelle,self.hauteure_visuelle), Vec2(self.carte.colonnes,self.carte.lignes),self.carte.dessin_atlas_indexes,self.carte.dessin_atlas_taille, [self.carte.case_sélectionnée_bordure,self.carte.case_survol_bordure], [self.carte.case_sélectionnée_couleur,self.carte.case_survol_couleur], [self.carte.case_sélectionnée,self.carte.case_survol])

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

                image.nuanceur.chargerUniformes(image.pos, image.rot, image.taille*image.échelle, Vec2(self.largeure_visuelle,self.hauteure_visuelle),entité.couleur_bordure)

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

    def changerCarte(self,carte : Carte):
        self.carte = carte
        self.carte.dessin_construire()
    
    def surCurseurSortir(self,event):
        self.carte.curseurSort()

    def surCurseurMouvement(self,event):
        taille_physique = Vec2(self.largeure_physique,self.hauteure_physique)
        taille_visuelle = Vec2(self.largeure_visuelle,self.hauteure_visuelle)
        position_visuelle = ( Vec2(event.x,event.y) - ( ( taille_physique - taille_visuelle )/2.0 ) )
        if position_visuelle.x > 0 and position_visuelle.x < taille_visuelle.x and position_visuelle.y > 0 and position_visuelle.y < taille_visuelle.y:
            self.carte.curseurSurvol( position_visuelle/taille_visuelle )
        else:
            self.surCurseurSortir(event)
    
    def surClique(self,event):
        taille_physique = Vec2(self.largeure_physique,self.hauteure_physique)
        taille_visuelle = Vec2(self.largeure_visuelle,self.hauteure_visuelle)
        self.carte.curseurClique( ( Vec2(event.x,event.y) - ( ( taille_physique - taille_visuelle )/2.0 ) )/taille_visuelle )

    # !==== Code copié de la librairie tkinter-gl ====!

    def gl_version(self):
        """
        The result of glGetString(GL_VERSION).
        """
        return self.tk.call(self._w, 'glversion')

    def gl_extensions(self):
        return self.tk.call(self._w, 'extensions')

    def make_current(self):
        """
        Makes the OpenGL context for this GLCanvas the current context.
        """
        self.tk.call(self._w, 'makecurrent')

    def swap_buffers(self):
        """
        Makes back buffer (which we draw to by default) be displayed
        in GLCanvas.
        """
        self.tk.call(self._w, 'swapbuffers')
    
    # !==== Code copié de la librairie tkinter-gl ====!