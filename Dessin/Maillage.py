from OpenGL.GL import *
from glm import int8

class Maillage:
    MODE_DESSIN_INDEXES = "Mode Dessin Indexes"
    MODE_DESSIN_LISTE = "Mode Dessin Liste"
    MODE_DESSIN_ÉVENTAIL = "Mode Dessin Éventail"
    MODE_DESSIN_BANDE = "Mode Dessin Bande"

    indexes : list[int]
    attributs : list[list[float]]
    attributs_types : list[int]
    n_sommets : int

    mode_dessin : str

    vao : int
    ivbo : int

    def __init__(self):
        self.indexes = []
        self.attributs = []
        self.attributs_types = []
        self.n_sommets = 0
        self.mode_dessin = ""
    
    def créer_indexes(self, attributs : list[list[float]], attributs_types : list[int], indexes : list[int]):
        # Vérifications de la validité des paramètres
        if type(attributs) != list or len(attributs) == 0 or type(attributs[0]) != list or len(attributs[0]) == 0:
            raise ArgumentError("Le paramètre « attributs » doit être de type list[list[float]].")
        else:
            for liste in attributs:
                for e in liste:
                    if type(e) != float:
                        raise ArgumentError("Le paramètre « attributs » doit être de type list[list[float]].")
                    
        if type(attributs_types) != list or len(attributs_types) == 0:
            raise ArgumentError("Le paramètre « attributs_types » doit être de type list[int].")
        else:
            for e in attributs_types:
                if type(e) != int:
                    raise ArgumentError("Le paramètre « attributs_types » doit être de type list[int].")
                    
        if type(indexes) != list or len(indexes) == 0:
            raise ArgumentError("Le paramètre « indexes » doit être de type list[int].")
        else:
            for e in indexes:
                if type(e) != int:
                    raise ArgumentError("Le paramètre « indexes » doit être de type list[int].")
        
        # Création
        self.indexes = indexes
        self.attributs = attributs
        self.attributs_types = attributs_types
        self.n_sommets = len(indexes)
        self.mode_dessin = self.MODE_DESSIN_INDEXES
    
    def créer_liste(self, attributs : list[list[float]], attributs_types : list[int]):
        # Vérifications de la validité des paramètres
        if type(attributs) != list or len(attributs) == 0 or type(attributs[0]) != list or len(attributs[0]) == 0:
            raise ArgumentError("Le paramètre « attributs » doit être de type list[list[float]].")
        else:
            for liste in attributs:
                for e in liste:
                    if type(e) != float:
                        raise ArgumentError("Le paramètre « attributs » doit être de type list[list[float]].")
                    
        if type(attributs_types) != list or len(attributs_types) == 0:
            raise ArgumentError("Le paramètre « attributs_types » doit être de type list[int].")
        else:
            for e in attributs_types:
                if type(e) != int:
                    raise ArgumentError("Le paramètre « attributs_types » doit être de type list[int].")
        
        #Création 
        self.indexes = []
        self.attributs = attributs
        self.attributs_types = attributs_types
        self.n_sommets = len(attributs[0])//attributs_types[0]
        for i in range(len(attributs)):
            if len(attributs[i])%attributs_types[i] != 0:
                raise ArgumentError("L'attribut " + str(i) + " contient " + str(len(attributs[i])) + " éléments, ce qui n'est pas un multiple de " + str(attributs_types[i]) + ".")
            elif self.n_sommets != len(attributs[i])//attributs_types[i]:
                raise ArgumentError("L'attribut " + str(i) + " n'a pas le même nombre de points que le premier attribut.")
        self.mode_dessin = self.MODE_DESSIN_LISTE

    def créer_éventail(self, attributs : list[list[float]], attributs_types : list[int]):
        self.créer_liste(attributs,attributs_types)
        self.mode_dessin = self.MODE_DESSIN_ÉVENTAIL
    
    def créer_bande(self, attributs : list[list[float]], attributs_types : list[int]):
        self.créer_liste(attributs,attributs_types)
        self.mode_dessin = self.MODE_DESSIN_BANDE
    
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
