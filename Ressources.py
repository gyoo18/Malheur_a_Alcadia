from Carte.Carte import Carte
from Carte.Tuile import Tuile
from Entités.Entité import Entité
from Entités.Golem import *
from Entités.Paysan import *
from Entités.Personnages import *
from typing_extensions import Self
import traceback
import json

class Ressources:

    ressources : Self = None

    def __init__(self):
        self.cartes : list[Carte] = []
        self.cartes_chargées : list[str] = []
        self.entités : list[Entité] = []
        self.entités_chargées : list[str] = []
        self.resultat_zone_2 : str = ""
        self.indexe_ressources : dict = None
        try:
            self.indexe_ressources = json.load(open("Ressources/Définitions.json"))
        except Exception as e:
            traceback.print_exc()
            traceback.print_exception(e)
            exit(-1)
        self.joueur = Joueur()

    def avoirRessources():
        if Ressources.ressources == None:
            Ressources.ressources = Ressources()
        return Ressources.ressources
    
    def détruire(self):
        pass

    def chargerCarte(self, nom : str):
        if nom in self.cartes_chargées:
            return self.cartes[self.cartes_chargées.index(nom)]
        else: 
            source = "Ressources/Cartes/" + self.indexe_ressources["Cartes"][nom]
            matrice : list[list[Tuile]] = []
            entités : list[Entité] = []
            positions_entités_initiales = []
            colonnes = 0
            lignes = 0

            carte_dict : dict = None
            try:
                carte_dict = json.load(open(source,"r"))
            except Exception as e:
                traceback.print_exc()
                traceback.print_exception(e)
                exit(-1) 
            if not "Carte" in carte_dict:
                raise AttributeError("La carte " + str(source) + "doit contenir un attribut 'Carte' de type list[list[int]].")
            for x in range(len(carte_dict["Carte"])):
                colonne = []
                for y in range(len(carte_dict["Carte"])):
                    match carte_dict["Carte"][y][x]:
                        case Tuile.TYPE_TERRE:
                            colonne.append(Tuile(Tuile.TYPE_TERRE))
                        case Tuile.TYPE_EAU:
                            colonne.append(Tuile(Tuile.TYPE_EAU))
                        case Tuile.TYPE_FEUX:
                            colonne.append(Tuile(Tuile.TYPE_FEUX))
                        case Tuile.TYPE_MUR:
                            colonne.append(Tuile(Tuile.TYPE_MUR))
                        case _:
                            raise ValueError("La tuile " + str(carte_dict[x][y]) + " à la position " + str(x) + ';' + str(y) + " n'est pas une tuile reconnue.")
                matrice.append(colonne)

            colonnes = len(matrice)
            lignes = len(matrice[0])
            
            liste_entités : list[dict]= carte_dict["Entités"]
            for e in liste_entités:
                entités.append(self.chargerEntité(e["ID"]))
                if "Position" in e:
                    if type(e["Position"]) != list or (type(e["Position"][0]) != int and type(e["Position"][0]) != float) or (type(e["Position"][1]) != int and type(unitée_dict["Position"][1]) != float):
                        raise TypeError("[Création de carte] L'élément 'Position' de " + unitée.nom + " doit être de type list[ int ou float ].")
                    positions_entités_initiales.append(Vec2(float(e["Position"][0]),float(e["Position"][1])))
                else:
                    positions_entités_initiales.append(Vec2(random.randrange(0,colonnes),random.randrange(0,lignes)))

            prochaine = carte_dict["Prochaine"]
            joueur_pos_init = Vec2(carte_dict["Joueur_pos"][0],carte_dict["Joueur_pos"][1])
            carte = Carte(colonnes,lignes,matrice,entités,positions_entités_initiales,joueur_pos_init,prochaine)
            self.cartes.append(carte)
            self.cartes_chargées.append(nom)

            return carte

    def chargerEntité(self,nom : str):
        if nom in self.entités_chargées:
            return self.entités[self.entités_chargées.index(nom)]
        else :
            source = "Ressources/Entités/" + self.indexe_ressources["Entités"][nom]
            unitée_dict : dict = None
            try:
                unitée_dict = json.load(open(source,"r"))
            except Exception as e:
                traceback.print_exc()
                traceback.print_exception(e)
            
            unitée = None
            match unitée_dict["Type"]:
                case "GolemTerre":
                    unitée = GolemTerre()
                case "GolemEau":
                    unitée = GolemEau()
                case "GolemFeu":
                    unitée = GolemFeu()
                case "Gosse":
                    unitée = Gosse()
                case "Mineur":
                    unitée = Mineur()
                case "Chevalier":
                    unitée = Chevalier()
                case "Arbalettier":
                    unitée = Arbaletier()
                case _:
                    raise ValueError("L'entité " + str(unitée_dict["Type"]) + " n'est pas une entité reconnue.")
                
            if "Nom" in unitée_dict:
                if type(unitée_dict["Nom"]) != str:
                    raise TypeError("[Création de carte] L'élément 'Nom' d'une entité doit être un string.")
                unitée.nom = unitée_dict["Nom"]
            if "PVMax" in unitée_dict:
                if type(unitée_dict["PVMax"]) != int and type(unitée_dict["PVMax"]) != float:
                    raise TypeError("L'élément 'PVMax' de " + unitée.nom + " doit être un int ou un float.")
                unitée.PVMax = int(unitée_dict["PVMax"])
            if "PV" in unitée_dict:
                if type(unitée_dict["PV"]) != int and type(unitée_dict["PV"]) != float:
                    raise TypeError("L'élément 'PV' de " + unitée.nom + " doit être un int ou un float.")
                unitée.PV = unitée_dict["PV"]
            if "Temp Chargement" in unitée_dict:
                if type(unitée_dict["Temp Chargement"]) != int and type(unitée_dict["Temp Chargement"]) != float:
                    raise TypeError("L'élément 'Temp Chargement' de " + unitée.nom + " doit être un int ou un float.")
                unitée.TEMP_CHARGEMENT = int(unitée_dict["Temp Chargement"])
            if "Attaque Chargée" in unitée_dict:
                if type(unitée_dict["Attaque Chargée"]) != int and type(unitée_dict["Attaque Chargée"]) != float:
                    raise TypeError("L'élément 'Attaque Chargée' de " + unitée.nom + " doit être un int ou un float.")
                unitée.attaque_chargée = unitée_dict["Attaque Chargée"]
            if "Attaque Normale" in unitée_dict:
                if type(unitée_dict["Attaque Normale"]) != int and type(unitée_dict["Attaque Normale"]) != float:
                    raise TypeError("L'élément 'Attaque Normale' de " + unitée.nom + " doit être un int ou un float.")
                unitée.attaque_normale_dégats = unitée_dict["Attaque Normale"]
            if "Dégats Défense" in unitée_dict:
                if type(unitée_dict["Dégats Défense"]) != int and type(unitée_dict["Dégats Défense"]) != float:
                    raise TypeError("L'élément 'Dégats Défense' de " + unitée.nom + " doit être un int ou un float.")
                unitée.dégats_défense = unitée_dict["Dégats Défense"]
            if "Dégats Libres" in unitée_dict:
                if type(unitée_dict["Dégats Libres"]) != int and type(unitée_dict["Dégats Libres"]) != float:
                    raise TypeError("L'élément 'Dégats Libres' de " + unitée.nom + " doit être un int ou un float.")
                unitée.dégats_libre = unitée_dict["Dégats Libres"]
            if "Dégats Charger" in unitée_dict:
                if type(unitée_dict["Dégats Charger"]) != int and type(unitée_dict["Dégats Charger"]) != float:
                    raise TypeError("L'élément 'Dégats Charger' de " + unitée.nom + " doit être un int ou un float.")
                unitée.dégats_charger = unitée_dict["Dégats Charger"]
            if "Camp" in unitée_dict:
                if type(unitée_dict["Camp"]) != str:
                    raise TypeError("L'élément 'Camp' de " + unitée.nom + " doit être un string.")
                unitée.Camp = unitée_dict["Camp"]
            if "Camps Ennemis" in unitée_dict:
                if type(unitée_dict["Camps Ennemis"]) != list:
                    raise TypeError("L'élément 'Camps Ennemis' de " + unitée.nom + " doit être de type listunitée_dict[ str ].")
                for c in unitée_dict["Camps Ennemis"]:
                    if type(c) != str:
                        raise TypeError("L'élément 'Camps Ennemis' de " + unitée.nom + " ne doit contenir que des strings.")
                    unitée.campsEnnemis = unitée_dict["Camps Ennemis"]
                
            self.entités.append(unitée)
            self.entités_chargées.append(nom)
            return unitée