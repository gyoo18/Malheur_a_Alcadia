from __future__ import annotations
from Maths.Vec2 import Vec2
from Entités.Paysan import *
from Entités.Golem import *
from Entités.Personnages import *
from Carte.Tuile import Tuile
from TFX import *
from InclusionsCirculaires.Entité_Carte import *

class Carte:
    
    def __init__(self,lignes : int ,colonnes :int, matrice : list[list[Tuile]], entités : list[Entité], positions_entitées_initiales : list[Vec2], joueur_pos_init : Vec2, prochaine : str):
        self.lignes : int = lignes
        self.colonnes : int = colonnes
        self.matrice : list[list[Tuile]] = matrice
        self.entités : list[Entité] = entités
        self.prochaine : str = prochaine
        self.positions_entitées_initiales : list[Vec2] = positions_entitées_initiales
        self.joueur_pos_init : Vec2 = joueur_pos_init
            
    def peutAller(self, entite: Entité, pos: Vec2):
        if pos.x<0 or pos.x>len(self.matrice)-1 or pos.y<0 or pos.y>len(self.matrice[0])-1:
            return False
        tuiles = self.matrice[int(pos.x)][int(pos.y)]
        if tuiles.type == Tuile.TYPE_MUR:
            return False
        elif tuiles.type == Tuile.TYPE_EAU and type(entite) != GolemEau:
            return False
        elif tuiles.type == Tuile.TYPE_FEUX and type(entite) != GolemFeu:
            return False
        else:
            return True

    def position(self):
        dict_position = {}
        for ligne in range(self.lignes):
            for colonne in range(self.colonnes):
                dict_position[ligne,colonne] = "0"
        return dict_position
    
    def dessiner(self):
        dessin = ""
        for y in range(self.lignes):
            ligne = ""
            for x in range(self.colonnes):
                
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
                                    en = gras(coul("P¬",ROUGE))
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
                        
                        if e.camp == "Personnages":
                            match e:
                                case Joueur():
                                    en = gras(coul("/\\",BLEU))
                    if en == "  " and len(e.chemin) > 0:
                        for pos in e.chemin:
                            if pos.x == x and pos.y == y:
                                if e.camp == "Paysans":
                                    en = gras(coul("++",ROUGE))
                                if e.camp == "Golems":
                                    en = gras(coul("••",NOIR))
                                break
                
                match self.matrice[x][y].type:
                    case Tuile.TYPE_EAU:
                        ligne += surl(en,CYAN_FONCÉ)
                    case Tuile.TYPE_TERRE:
                        ligne += surl(en,VERT)
                    case Tuile.TYPE_FEUX:
                        ligne += surl(en,ORANGE_FONCÉ)
                    case Tuile.TYPE_MUR:
                        ligne += surl(en,GRIS_FONCÉ)
                    case Tuile.TYPE_OR:
                        ligne += surl(en,OR)
                    case _:
                        raise TypeError("Tuile " + str(self.matrice[x][y]) + " de type " + str(self.matrice[x][y].type) + " n'a pas de type valide.")
            dessin += ligne + '\n'
        return dessin