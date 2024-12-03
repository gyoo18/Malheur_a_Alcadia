from Carte.class_carte import Carte
from Entités.Entité import Entité
from typing_extensions import Self
from Dessin.Maillage import Maillage

class Ressources:

    ressources : Self = None

    def __init__(self):
        self.cartes : list[Carte] = []
        self.entités : list[Entité] = []
        self.resultat_zone_2 : str = ""

    def avoirRessources():
        if Ressources.ressources == None:
            Ressources.ressources = Ressources()
        return Ressources.ressources
    
    def détruire(self):
        pass
    
    def chargerObj(self,source : str):
        fichier = open(source,"r")
        sommets = []
        sommets_indexés = []
        normales = []
        normales_indexées = []
        uv = []
        uv_indexés = []
        indexes = []
        for ligne in fichier.readlines():
            mots = ligne.split(" ")
            if mots[0] == "v":
                sommets.append((float(mots[1]),float(mots[2]),float(mots[3])))
            if mots[0] == "vn":
                normales.append((float(mots[1]),float(mots[2]),float(mots[3])))
            if mots[0] == "vt":
                uv.append((float(mots[1]),float(mots[2])))
            if mots[0] == "f":
                obji = []
                obji.append(mots[1].split("/"))
                obji.append(mots[2].split("/"))
                obji.append(mots[3].split("/"))

                for l in range(len(obji)):
                    est_présent = False
                    indexe_présent = 0
                    for i in range(len(sommets_indexés)):
                        if ( sommets_indexés[i] == sommets[int(obji[l][0])-1]  and 
                            ( not (len(obji[l]) == 3) or normales_indexées[i] == normales[int(obji[l][2])-1] ) and 
                            ( not (len(obji[l]) >= 2) or uv_indexés[i] == uv[int(obji[l][1])-1] ) ):

                            est_présent = True
                            indexe_présent = i
                            break
                    
                    if est_présent:
                        indexes.append(indexe_présent)
                    else:
                        sommets_indexés.append(sommets[int(obji[l][0])-1])
                        if len(obji[l]) == 3:
                            normales_indexées.append(normales[int(obji[l][2])-1])
                        if len(obji[l]) >= 2:
                            uv_indexés.append(uv[int(obji[l][1])-1])
                        indexes.append(len(sommets_indexés)-1)
        sommets_float = []
        normales_float = []
        uv_float = []
        for i in range(len(sommets_indexés)):
            sommets_float.append(sommets_indexés[i][0])
            sommets_float.append(sommets_indexés[i][1])
            sommets_float.append(sommets_indexés[i][2])
        for i in range(len(normales_indexées)):
            normales_float.append(normales_indexées[i][0])
            normales_float.append(normales_indexées[i][1])
            normales_float.append(normales_indexées[i][2])
        for i in range(len(uv_indexés)):
            uv_float.append(uv_indexés[i][0])
            uv_float.append(uv_indexés[i][1])

        attributs = [sommets_float]
        attibuts_types = [3]
        if len(normales_float) > 0:
            attributs.append(normales_float)
            attibuts_types.append(3)
        if len(uv_float) > 0:
            attributs.append(uv_float)
            attibuts_types.append(2)
        
        m = Maillage()
        m.créer_indexes(attributs,attibuts_types,indexes)
        return m