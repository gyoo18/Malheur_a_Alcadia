from OpenGL.GL import *
import time

class Nuanceur:
    sommets_source : str
    fragments_source : str
    programme : int

    def __init__(self, source : str):
        fichier  = open(source+".vert","r")
        lignes = fichier.readlines()
        self.sommets_source = ""
        for ligne in lignes:
            self.sommets_source += ligne
        fichier.close()
        
        fichier  = open(source+".frag","r")
        lignes = fichier.readlines()
        self.fragments_source = ""
        for ligne in lignes:
            self.fragments_source += ligne
        fichier.close()
    
    def construire(self):
        programme_sommets = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(programme_sommets, self.sommets_source)
        glCompileShader(programme_sommets)
        succès_compilation = glGetShaderiv(programme_sommets, GL_COMPILE_STATUS)
        if succès_compilation == 0:
            raise ErreurCompilationNuanceur(glGetShaderInfoLog(programme_sommets),"Sommets")

        
        programme_fragment = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(programme_fragment, self.fragments_source)
        glCompileShader(programme_fragment)
        succès_compilation = glGetShaderiv(programme_fragment, GL_COMPILE_STATUS)
        if succès_compilation == 0:
            raise ErreurCompilationNuanceur(glGetShaderInfoLog(programme_fragment),"Fragments")
        
        self.programme = glCreateProgram()
        glAttachShader(self.programme,programme_sommets)
        glAttachShader(self.programme,programme_fragment)
        glLinkProgram(self.programme)
        succès_compilation = glGetProgramiv(self.programme, GL_LINK_STATUS)
        if succès_compilation == 0:
            raise ErreurLiaisonNuanceur(glGetProgramInfoLog(self.programme))
        
    def démarrer(self):
        glUseProgram(self.programme)
        

class ErreurCompilationNuanceur(Exception):
    def __init__(self,message : str,type :str):
        super().__init__("Erreur de compilation de nuancueur de type " + str(type) + " : " + str(message))

class ErreurLiaisonNuanceur(Exception):
    def __init__(self,message : str):
        super().__init__("Erreur de liaison de nuancueur : " + str(message))