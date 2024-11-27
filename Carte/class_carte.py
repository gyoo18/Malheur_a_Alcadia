from __future__ import annotations
from Maths.Vec2 import Vec2
from Entités.Paysan import *
from Entités.Golem import *
from Carte.Tuile import Tuiles
from TFX import *
from InclusionsCirculaires.Entité_Carte import *

class Carte:
    ligne : int
    colonne : int
    matrice : list[list[Tuiles]]

    entités : list[Entité]
    
    def __init__(self,ligne : int ,colonne :int):
        self.ligne = ligne
        self.colonne = colonne
        self.matrice = []
        self.entités = []

    

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
    
    def dessiner(self):
        dessin = ""
        for y in range(self.ligne):
            ligne = ""
            for x in range(self.colonne):
                
                en = "  "
                for e in self.entités:
                    if e.pos.x == x and e.pos.y == y:
                        if e.camp == "Paysans":
                            match e:
                                case Gosse():
                                    en = gras(coul("çç",ROUGE))
                                    break
                                case Mineur():
                                    en = gras(coul("/>",ROUGE))
                                    break
                                case Prêtre():
                                    en = gras(coul("Ot",ROUGE))
                                    break
                                case Arbaletier():
                                    en = coul("G>",ROUGE)
                                    break
                                case Paysan():
                                    en = gras(coul("PP",ROUGE))
                                    break
                                case _:
                                    raise TypeError("Entité " + str(e) + " n'est pas un paysan valide.")
                        
                        if e.camp == "Golems":
                            match e:
                                case GolemTerre():
                                    en = gras(coul("(u",BRUN))
                                    break
                                case GolemEau():
                                    en = gras(coul("}{",BLEU))
                                    break
                                case GolemFeu():
                                    en = gras(coul("MM",ORANGE))
                                    break
                                case Golem():
                                    en = gras(coul("GG",GRIS))
                                    break
                                case _:
                                    raise TypeError("Entité " + str(e) + " n'est pas un golem valide.")
                
                match self.matrice[x][y].type:
                    case Tuiles.TYPE_EAU:
                        ligne += surl(en,CYAN_FONCÉ)
                    case Tuiles.TYPE_TERRE:
                        ligne += surl(en,VERT)
                    case Tuiles.TYPE_FEUX:
                        ligne += surl(en,ORANGE_FONCÉ)
                    case Tuiles.TYPE_MUR:
                        ligne += surl(en,GRIS_FONCÉ)
                    case _:
                        raise TypeError("Tuile " + str(self.matrice[x][y]) + " de type " + str(self.matrice[x][y].type) + " n'a pas de type valide.")
            dessin += ligne + '\n'
        return dessin
    
carte_1 = Carte(5,5) 

mape = carte_1.creation()
print(mape)
positions =carte_1.position()


# def creation_unite(i,j,x):
#     try:
#         if (i or j) <0:
#             return (f"Le jeux accepte uniquement les nombres positifs")
#         elif type(i or j)!= int:
#             return (f"Le jeux accepte uniquement les entiers")
#         elif mape[i][j] == "0":
#             positions[(i,j)]= x
#             mape[i][j] = x
#             return mape
#         else:
#             return(f"Case non disponible")
#     except IndexError:
#         return("Coordonnés en dehors de la carte")
#     
# 
# def effacer_unite(i,j,x):
#     try:
#         if (i or j) <0:
#             return (f"Le jeux accepte uniquement les nombres positifs")
#         elif type(i or j)!= int:
#             return (f"Le jeux accepte uniquement les entiers")
#         elif mape[i][j] == x:
#             positions[(i,j)]= "0"
#             mape[i][j] = "0"
#             return mape
#         else:
#             return(f"Case non disponible")
#     except IndexError:
#         return("Coordonnés en dehors de la carte")
# 
# mape=creation_unite(1,1,"unite_2")
# mape=creation_unite(2,2,"unite_1")
# 
# print(mape)
# #print(positions)
# 
# def mouvement(i,j,w,a,s,d):
#     if w==1:
#         creation_unite(i-1,j)
#         effacer_unite(i,j)
#     elif a==1:
#         creation_unite (i,j-1)
#         effacer_unite(i,j)
# 
#     elif s==1:
#         creation_unite(i+1,j)
#         effacer_unite(i,j)
# 
#     elif d==1:
#         creation_unite(i,j+1)
#         effacer_unite(i,j)
#     
# '''''
# print (mape)
# mouvement(1,1,1,0,0,0)
# print (mape)
# mouvement(0,1,0,1,0,0)
# print (mape)
# mouvement(0,0,0,0,1,0)
# print (mape)
# mouvement(1,0,0,0,0,1)
# print (mape)
# '''''
# def distance(unite_1,unite_2):
#     for key1,value1 in positions.items():
#         if "unite_1" == value1:
#              x1,y1 = key1
#     
#     for key2,value2 in positions.items():
#         if "unite_2" == value2:
#             x2,y2= key2
# 
#     dist = (((x2-x1)**2+(y2-y1)**2))**0.5
#     return dist
# 
# print(distance("unite_1","unite_2"))
