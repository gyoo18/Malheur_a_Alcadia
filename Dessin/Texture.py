import numpy
from OpenGL.GL import *

class Texture:

    def __init__(self, source : str, texture : numpy.ndarray):
        self.source : str = source
        self.tex : numpy.ndarray = texture
        self.hauteur : int = texture.shape[0]
        self.largeur : int = texture.shape[1]
        self.ID : int = -1
        self.estConstruit : bool = False
    
    def construire(self):
        self.ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D,self.ID)
        format = None
        match len(self.tex[0][0]):
            case 1:
                format = GL_RED
            case 2:
                format = GL_RG
            case 3:
                format = GL_RGB
            case 4:
                format = GL_RGBA
            case _:
                raise ValueError("L'image " + self.source + " contient " + str(len(self.tex[0][0])) + " valeurs de couleurs. Les valeurs acceptées sont : 1, 2, 3 ou 4.")
        
        data_type = None
        match self.tex.dtype:
            case numpy.uint8:
                data_type = GL_UNSIGNED_BYTE
            case numpy.int8:
                data_type = GL_BYTE
            case numpy.uint16:
                data_type = GL_UNSIGNED_SHORT
            case numpy.int16:
                data_type = GL_SHORT
            case numpy.uint32:
                data_type = GL_UNSIGNED_INT
            case numpy.int32:
                data_type = GL_INT
            case numpy.float32:
                data_type = GL_FLOAT

        glTexImage2D(GL_TEXTURE_2D,0,format,self.largeur,self.hauteur,0,format,data_type,self.tex.tobytes())

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        # glGenerateMipmap(GL_TEXTURE_2D)

        self.estConstruit = True