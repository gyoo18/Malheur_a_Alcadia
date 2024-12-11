# Ce module n'est utilisé que pour tester OpenGL tout seul. Il est supposé être remplacé par Tkinter
from OpenGL.GLUT import *
from Dessin.Peintre import Peintre
import time

class Fenetre:
    largeure : int # En pixels
    hauteure : int # En pixels
    gluFenetre : int
    peintre : Peintre

    fpsChrono : float
    fpsPostier : int

    def __init__(self, largeure:int, hauteure:int, positionX = 0, positionY = 0, nom = "Fenetre"):
        print("Création d'une fenêtre.")
        self.largeure = largeure
        self.hauteure = hauteure
        self.fpsChrono = time.time()
        self.fpsPostier = 0

        print("Initialisation du peintre.")
        self.peintre = Peintre()

        print("Initialisation de GLUT.")
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
        glutInitWindowSize(largeure,hauteure)
        glutInitWindowPosition(positionX,positionY)
        self.gluFenetre = glutCreateWindow(nom)
        glutDisplayFunc(self.surModification)
        glutIdleFunc(self.dessin)

    def partirGL(self):
        glutMainLoop()
    
    def surModification(self):
        print("Fenêtre modifiée.")

        self.largeure = glutGet(GLUT_WINDOW_WIDTH)
        self.hauteure = glutGet(GLUT_WINDOW_HEIGHT)
        print("nouvelles dimensions :",self.largeure,self.hauteure)

        print("peintre Initialisé :",self.peintre.initialisé)
        if not self.peintre.initialisé:
            print("Initialiser peintre")
            self.peintre.initialiser(self.largeure,self.hauteure)
        else:
            self.peintre.surModificationFenetre(self.largeure,self.hauteure)
        
        self.peintre.dessiner()
        glutSwapBuffers()

    def dessin(self):
        self.fpsPostier += 1
        self.peintre.peindre()
        glutSwapBuffers()

        if self.fpsPostier >= 5000:
            print("FPS :", int((self.fpsPostier)/(time.time()-self.fpsChrono)),"Time :",int((time.time()-self.fpsChrono)*100000/5000)/100,"ms")
            self.fpsPostier = 0
            self.fpsChrono = time.time()