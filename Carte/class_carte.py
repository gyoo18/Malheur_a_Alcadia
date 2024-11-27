from Maths.Vec2 import Vec2
from Entités.Entité import *
from Carte.Tuile import Tuiles
from Entités.Golem import *
class Carte:
    ligne : int
    colonne : int
    matrice : list[list[Tuiles]]

    entitées : list[Entité]
    
    def __init__(self,ligne : int ,colonne :int):
        self.ligne = ligne
        self.colonne = colonne
        self.matrice = []

    

    def creation(self):
        self.matrice = []
        for ligne in range(self.ligne):
            ligne_donnee = []
            for colonne in range(self.colonne):
                ligne_donnee.append(Tuiles(Tuiles.TYPE_TERRE))
            self.matrice.append(ligne_donnee)
        
    
            
    def peutAller(self, entite: Entité, pos: Vec2):
        if pos.x<0 or pos.x>len(self.matrice)-1 or pos.y<0 or pos.y>len(self.matrice[0])-1:
            return False
        tuiles = self.matrice[int(pos.x)][int(pos.y)]
        if tuiles.type == Tuiles.TYPE_MUR:
            return False
        elif tuiles.type == Tuiles.TYPE_EAU and type(entite) != GolemEau:
            return False
        else:
            return True

    def position(self):
        dict_position = {}
        for ligne in range(self.ligne):
            for colonne in range(self.colonne):
                dict_position[ligne,colonne] = "0"
        return dict_position
    

    
carte_1 = Carte(5,5) 

mape = carte_1.creation()
print(mape)
positions =carte_1.position()


def creation_unite(i,j,x):
    try:
        if (i or j) <0:
            return (f"Le jeux accepte uniquement les nombres positifs")
        elif type(i or j)!= int:
            return (f"Le jeux accepte uniquement les entiers")
        elif mape[i][j] == "0":
            positions[(i,j)]= x
            mape[i][j] = x
            return mape
        else:
            return(f"Case non disponible")
    except IndexError:
        return("Coordonnés en dehors de la carte")
    

def effacer_unite(i,j,x):
    try:
        if (i or j) <0:
            return (f"Le jeux accepte uniquement les nombres positifs")
        elif type(i or j)!= int:
            return (f"Le jeux accepte uniquement les entiers")
        elif mape[i][j] == x:
            positions[(i,j)]= "0"
            mape[i][j] = "0"
            return mape
        else:
            return(f"Case non disponible")
    except IndexError:
        return("Coordonnés en dehors de la carte")

mape=creation_unite(1,1,"unite_2")
mape=creation_unite(2,2,"unite_1")

print(mape)
#print(positions)


   