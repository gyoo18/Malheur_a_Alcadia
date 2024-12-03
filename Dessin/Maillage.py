from OpenGL.GL import *

class Maillage:
    indexes : list[int]
    attributs : list[list[float]]
    attributs_types : list[int]
    n_sommets : int

    vao : int
    ivbo : int

    def __init__(self, attributs : list[list[float]], attributs_types : list[int], indexes : list[int]):
        self.indexes = indexes
        self.attributs = attributs
        self.attributs_types = attributs_types
        self.n_sommets = len(indexes)
    
    def construire(self):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        for i in range(len(self.attributs)):
            vbo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER,vbo)
            données = (GLfloat * len(self.attributs[i]))(*self.attributs[i])
            glBufferData(GL_ARRAY_BUFFER,sizeof(GLfloat)*len(self.attributs[i]),données, GL_STATIC_DRAW)
            glVertexAttribPointer(i,self.attributs_types[i],GL_FLOAT,GL_FALSE,0,None)
        self.ivbo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.ivbo)
        données = (GLuint * len(self.indexes))(*self.indexes)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,sizeof(GLuint)*len(self.indexes),données,GL_STATIC_DRAW)
