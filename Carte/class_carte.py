from Maths.Vec2 import Vec2
from Entités.Entité import Entité
from Carte.Tuile import Tuiles
class Carte:
    ligne : int
    colonne : int

    entitées : list[Entité]
    
    def __init__(self,ligne : int ,colonne :int):
        self.ligne = ligne
        self.colonne= colonne

    

    def creation(self):
        matrice = []
        for ligne in range(self.ligne):
            ligne_donnee = []
            for colonne in range(self.colonne):
                ligne_donnee.append("0")
            matrice.append(ligne_donnee)
        return matrice
    
            
    def peutAller(self, pos : Vec2):
        tuiles = self.matrice[int(pos.x)][int(pos.y)]
        if tuiles.type == Tuiles.TYPE_MUR:
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

def mouvement(i,j,w,a,s,d):
    if w==1:
        creation_unite(i-1,j)
        effacer_unite(i,j)
    elif a==1:
        creation_unite (i,j-1)
        effacer_unite(i,j)

    elif s==1:
        creation_unite(i+1,j)
        effacer_unite(i,j)

    elif d==1:
        creation_unite(i,j+1)
        effacer_unite(i,j)
    
'''''
print (mape)
mouvement(1,1,1,0,0,0)
print (mape)
mouvement(0,1,0,1,0,0)
print (mape)
mouvement(0,0,0,0,1,0)
print (mape)
mouvement(1,0,0,0,0,1)
print (mape)
'''''
def distance(unite_1,unite_2):
    for key1,value1 in positions.items():
        if "unite_1" == value1:
             x1,y1 = key1
    
    for key2,value2 in positions.items():
        if "unite_2" == value2:
            x2,y2= key2

    dist = (((x2-x1)**2+(y2-y1)**2))**0.5
    return dist

print(distance("unite_1","unite_2"))
