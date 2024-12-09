from __future__ import annotations
from InclusionsCirculaires.Ressources_Jeu import *
from Carte.Carte import *
from Carte.Tuile import Tuile
from Entités.Entité import *
from Entités.Golem import *
from Entités.Paysan import *
from Entités.Personnages import *
import codecs
import traceback
import json

class Ressources:

    ressources : Ressources = None

    def __init__(self):
        self.cartes : list[Carte] = []
        self.cartes_chargées : list[str] = []
        self.entités : list[Entité] = []
        self.entités_chargées : list[str] = []
        self.dialogues : dict[list[str]] = []
        self.dialogues_chargés : list[str] = []
        self.resultat_zone_2 : str = ""
        self.indexe_ressources : dict = None
        try:
            self.indexe_ressources = json.load(codecs.open("Ressources/Définitions.json","r","utf-8"))
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
            if not nom in self.indexe_ressources["Cartes"]:
                raise AttributeError("[Charger Carte] La carte " + nom + " n'est pas définie.")
            source = "Ressources/Cartes/" + self.indexe_ressources["Cartes"][nom]
            matrice : list[list[Tuile]] = []
            entités : list[tuple[str,Vec2|None,str|None]] = []
            colonnes = 0
            lignes = 0
            estScène : bool= False
            séquences : Séquence|dict[Séquence] = None

            carte_dict : dict = None
            try:
                fichier = codecs.open(source,"r","utf-8")
                carte_dict = json.load(fichier)
                fichier.close()
            except Exception as e:
                traceback.print_exc()
                traceback.print_exception(e)
                exit(-1) 

            if not "Carte" in carte_dict:
                raise AttributeError("La carte " + str(source) + " doit contenir un attribut 'Carte' de type list[list[str]].")
            
            if not "Entités" in carte_dict:
                raise AttributeError("La Carte " + str(source) + " doit contenir un attribut 'Entités' de type list[dict]")
            
            if not "Prochaine" in carte_dict:
                raise AttributeError("La Carte " + str(source) + " doit contenir un attribut 'Prochaine' de type str")
            
            if not "Joueur_pos" in carte_dict:
                raise AttributeError("La Carte " + str(source) + " doit contenir un attribut 'Joueur_pos' de type list[int] et de longueur 2")
            
            if not "Séquence" in carte_dict:
                raise AttributeError("La Carte " + str(source) + " doit contenir un attribut 'Séquence' de type liste ou dictionnaire.")
            
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
                        case Tuile.TYPE_OR:
                            colonne.append(Tuile(Tuile.TYPE_OR))
                        case Tuile.TYPE_MUR:
                            colonne.append(Tuile(Tuile.TYPE_MUR))
                        case _:
                            raise ValueError("La tuile " + str(carte_dict[x][y]) + " à la position " + str(x) + ';' + str(y) + " n'est pas une tuile reconnue.")
                matrice.append(colonne)

            colonnes = len(matrice)
            lignes = len(matrice[0])
            
            liste_entités : list[dict] = carte_dict["Entités"]
            for e in liste_entités:
                unité = (e["ID"],None,None)
                if "Position" in e:
                    if type(e["Position"]) != list or (type(e["Position"][0]) != int and type(e["Position"][0]) != float) or (type(e["Position"][1]) != int and type(e["Position"][1]) != float):
                        raise TypeError("[Création de carte] L'élément 'Position' de " + e["ID"] + " doit être de type list[ int ou float ].")
                    unité = (unité[0],Vec2(float(e["Position"][0]),float(e["Position"][1])),unité[2])
                if "Anim ID" in e:
                    if type(e["Anim ID"]) != str:
                        raise TypeError("[Création de carte] L'élément 'Anim ID' de " + e["ID"] + " doit être de type str.")
                    unité = (unité[0],unité[1],e["Anim ID"])
                entités.append(unité)
            
            if "Scène" in carte_dict:
                if type(carte_dict["Scène"]) != bool:
                    raise TypeError("[Création de carte] L'élément 'estScène' de " + str(source) + " doit être de type bool.")
                estScène = carte_dict["Scène"]
            
            if estScène:
                séquences = Séquence()
                if type(carte_dict["Séquence"]) != list:
                    raise TypeError("[Création de carte] L'élément 'Séquence' de " + str(source) + " doit être une list[dict]. Changez 'estScène' à False si vous voulez en faire une liste.")
                for plan_dict in carte_dict["Séquence"]:
                    if type(plan_dict) != dict:
                        raise TypeError("[Création de carte] Les éléments de 'Séquence' dans " + str(source) + " ne doit contenir que des dictionnaires.")
                    
                    plan : Plan = self.chargerPlan(plan_dict,entités,source,None)
                    séquences.plans.append(plan)
            else:
                séquences = {}
                if type(carte_dict["Séquence"]) != dict:
                    raise TypeError("[Création de carte] L'élément 'Séquence' de " + str(source) + " doit être un dict[list[dict]]. Changez 'estScène' à False si vous voulez en faire une liste.")
                
                if not "Début" in carte_dict["Séquence"] or not "Jeu" in carte_dict["Séquence"] or not "Succès" in carte_dict["Séquence"] or not "Échec" in carte_dict["Séquence"]:
                    raise AttributeError("[Création de carte] L'élément 'Séquence' de " + str(source) + " doit contenir les clé suivantes : 'Début', 'Jeu', 'Succès' et 'Échec', qui sont toutes des list[dict]")
                
                if type(carte_dict["Séquence"]["Début"]) != list or type(carte_dict["Séquence"]["Jeu"]) != list or type(carte_dict["Séquence"]["Succès"]) != list or type(carte_dict["Séquence"]["Échec"]) != list:
                    raise TypeError("[Création de carte] Les clés de l'élément 'Séquence' de " + str(source) + " ne sont pas toutes des listes.")
                
                for clé in list(carte_dict["Séquence"].keys()):
                    séquence : Séquence = Séquence()
                    match clé:
                        case "Début":
                            séquence.position = Séquence.DÉBUT
                        case "Jeu":
                            séquence.position = Séquence.JEU
                        case "Succès":
                            séquence.position = Séquence.SUCCÈS
                        case "Échec":
                            séquence.position = Séquence.ÉCHEC
                        case _:
                            raise AttributeError("[Création de carte] La clé " + str(clé) + " de séquence n'est pas une clé reconnue. Veuillez utiliser 'Début', 'Jeu', 'Réussite' ou 'Échec'.")
                        
                    for plan_dict in carte_dict["Séquence"][clé]:
                        if type(plan_dict) != dict:
                            raise TypeError("[Création de carte] " + str(source) + ">Séquence>" + clé + " ne doit contenir que des dictionnaires.")
                        
                        plan : Plan = self.chargerPlan(plan_dict, entités,source,clé)
                        séquence.plans.append(plan)
                    séquences[clé] = séquence
                pass

            script : str = None
            if "Script" in carte_dict:
                if type(carte_dict["Script"]) != str:
                    raise TypeError("[Création de carte] L'élément 'Script' de " + source + " doit être de type string.")
                script = carte_dict["Script"]

            prochaine = carte_dict["Prochaine"]
            joueur_pos_init = Vec2(carte_dict["Joueur_pos"][0],carte_dict["Joueur_pos"][1])
            carte = Carte(estScène,colonnes,lignes,matrice,entités,joueur_pos_init,séquences,prochaine)
            carte.estScène = estScène
            carte.script = script
            self.cartes.append(carte)
            self.cartes_chargées.append(nom)

            return carte

    def chargerEntité(self,nom : str):
        if False and nom in self.entités_chargées:
            return self.entités[self.entités_chargées.index(nom)]
        else :
            if not nom in self.indexe_ressources["Entités"]:
                raise AttributeError("[Charger Entité] L'entité " + nom + " n'est pas définie.")
            source = "Ressources/Entités/" + self.indexe_ressources["Entités"][nom]
            unitée_dict : dict = None
            try:
                fichier = codecs.open(source,"r","utf-8")
                unitée_dict = json.load(fichier)
                fichier.close()
            except Exception as e:
                traceback.print_exc()
                traceback.print_exception(e)
                exit(-1)
            
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
                    unitée = Arbalettier()
                case "Prêtre":
                    unitée = Prêtre()
                case "Personnage":
                    unitée = Personnage("Personnage")
                case _:
                    raise ValueError("L'entité " + str(unitée_dict["Type"]) + " n'est pas une entité reconnue.")
                
            if "Nom" in unitée_dict:
                if type(unitée_dict["Nom"]) != str:
                    raise TypeError("[Création de carte] L'élément 'Nom' d'une entité doit être un string.")
                unitée.nom = unitée_dict["Nom"]
                unitée.nomAffichage = unitée.nom

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
                    raise TypeError("L'élément 'Camps Ennemis' de " + unitée.nom + " doit être de type list[ str ].")
                for c in unitée_dict["Camps Ennemis"]:
                    if type(c) != str:
                        raise TypeError("L'élément 'Camps Ennemis' de " + unitée.nom + " ne doit contenir que des strings.")
                    unitée.campsEnnemis = unitée_dict["Camps Ennemis"]

            if unitée_dict["Type"] == "Personnage" and "Caractère" in unitée_dict:
                if type(unitée_dict["Caractère"]) != str:
                    raise TypeError("L'élément 'Caractère' de " + unitée.nom + " doit être de type str.")
                unitée.caratère_dessin = gras(unitée_dict["Caractère"])

            if unitée_dict["Type"] == "Personnage" and "Caractère Couleur" in unitée_dict:
                if type(unitée_dict["Caractère Couleur"]) != list:
                    raise TypeError("L'élément 'Caractère Couleur' de " + unitée.nom + " doit être de type list[ float ].")
                for c in unitée_dict["Caractère Couleur"]:
                    if type(c) != float:
                        raise TypeError("L'élément 'Caractère Couleur' de " + unitée.nom + " ne doit contenir que des float.")
                    unitée.nomAffichage = coul(unitée.nomAffichage,Vec3(unitée_dict["Caractère Couleur"][0],unitée_dict["Caractère Couleur"][1],unitée_dict["Caractère Couleur"][2]))
                
            self.entités.append(unitée)
            self.entités_chargées.append(nom)
            return unitée
    
    def chargerDialogue(self, groupe : str, ID : list[int]):
        from dialogue import dialogue

        if groupe in self.dialogues_chargés:
            texte = ""
            for i in ID:
                texte += self.dialogues[groupe][i] + '\n'
            return texte
        else:
            if not groupe in self.indexe_ressources["Dialogues"]:
                raise AttributeError("[Charger Dialogue] Le groupe de dialogue : " + str(groupe) + " n'est pas définit.")
            source : str = "Ressources/Dialogues/" + self.indexe_ressources["Dialogues"][groupe]
            dialogue_dict : dict= None
            try:
                fichier = codecs.open(source,"r","utf-8")
                dialogue_dict = json.load(fichier)
                fichier.close()
            except Exception as e:
                traceback.print_exc()
                traceback.print_exception(e)
                exit(-1)
            
            if not "Titre" in dialogue_dict:
                raise AttributeError("[Charger Dialogue] Le groupe de dialogues " + str(source) + " a besoin d'un 'Titre' par défaut.")
            if type(dialogue_dict["Titre"]) != str:
                raise AttributeError("[Charger Dialogue] Le titre par défaut du groupe de dialogues " + str(source) + " doit être un string.")
            if not "Dialogues" in dialogue_dict:
                raise AttributeError("[Charger Dialogue] Le groupe de dialogues " + str(source) + " n'a pas de clé 'Dialogue'.")
            if type(dialogue_dict["Dialogues"]) != list:
                raise AttributeError("[Charger Dialogue] L'élément 'Dialogue' du groupe de dialogues " + str(source) + " doit être une liste.")
            
            dialogue_texte : tuple[str,str] = (dialogue_dict["Titre"],None)
            texte : str = ""

            for i in ID:
                if len(dialogue_dict["Dialogues"])-1 < i:
                    raise IndexError("[Charger Dialogue] L'indexe " + str(i) + " n'existe pas dans le groupe " + source + ". L'indexe maximum est " + str(len(dialogue_dict["Dialogues"])-1))
                if not "Dialogue" in dialogue_dict["Dialogues"][i]:
                    raise AttributeError("[Charger Dialogue] Le dialogue à l'indexe " + str(i) + " du groupe" + source + " n'a pas d'élément 'Dialogue'.")
                if type(dialogue_dict["Dialogues"][i]["Dialogue"]) != list:
                    raise TypeError("[Charger Dialogue] L'élément 'Dialogue' à l'indexe " + str(i) + " du groupe " + source + " doit être une liste.")
                
                if "Titre" in dialogue_dict["Dialogues"][i]:
                    dialogue_texte = (dialogue_dict["Dialogue"][i]["Titre"],None)
                
                personnage : str = None
                if "Personnage" in dialogue_dict["Dialogues"][i]:
                    if type(dialogue_dict["Dialogues"][i]["Personnage"]) != str:
                        raise TypeError("[Charger Dialogue] " + source + ">Dialogues>" + str(i) + ">Personnage n'est pas un string.")
                    personnage = dialogue_dict["Dialogues"][i]["Personnage"]

                for d in dialogue_dict["Dialogues"][i]["Dialogue"]:
                    if type(d) != str:
                        raise TypeError("[Charger Dialogue] " + source + ">Dialogues>" + str(i) + ">Ligne " + str(dialogue_dict["Dialogues"][i]["Dialogue"].indexe(d)) + " n'est pas un string.")
                    
                    if personnage:
                        texte += dialogue(d,personnage) + '\n'
                    else:
                        texte += d + '\n'
                dialogue_texte = (dialogue_texte[0],texte)
            return dialogue_texte
        
    def chargerPlan(self, plan_dict : dict, entités : list[tuple[str,Vec2|None,str|None]], source : str, clé : str|None,):
        plan = Plan()
        if clé == None:
            clé_str = ""
        else:
            clé_str = clé + '>'
        if "estAnimation" in plan_dict and type(plan_dict["estAnimation"]) == bool and plan_dict["estAnimation"]:
            plan.estAnimation = True
            Temps_défaut : float = None
            if "Temps" in plan_dict:
                if type(plan_dict["Temps"]) != float and type(plan_dict["Temps"]) != int:
                    raise TypeError("[Charger Plan] L'élément 'Temps' dans " + source + '>' + clé_str + str(plan_dict) + " doit être de type int ou float.")
                Temps_défaut = plan_dict["Temps"]
            if not "Plans" in plan_dict:
                raise AttributeError("[Charger Plan] " + source + '>' + clé_str + str(plan_dict) + " doit contenir une clé 'Plans' de type list[dict]")
            if type(plan_dict["Plans"]) != list:
                raise TypeError("[Charger Plan] " + source + '>' + clé_str + str(plan_dict) + " doit contenir une clé 'Plans' de type list[dict]")
            
            for anim_plan_dict in plan_dict["Plans"]:
                plan.personnages.append([])
                plan.personnages_positions.append([])
                plan.dialogues.append("")
                plan.titres.append("")
                if type(anim_plan_dict) != dict:
                    raise TypeError("[Charger Plan] " + source + '>Séquence>' + clé_str + str(plan_dict) + '>' + str(anim_plan_dict) + " doit être de type dict")
                
                if not "Temps" in anim_plan_dict:
                    plan.temps.append(Temps_défaut)
                
                for e in list(anim_plan_dict.keys()):
                    estEntité = False
                    if not (e == "Dialogue Groupe" or e == "Dialogue ID" or e == "Mélios"):
                        for en in entités:
                            if en[2] == e:
                                estEntité = True

                    if not (e == "Dialogue Groupe" or e == "Dialogue ID" or e == "Temps" or e == "Mélios" or estEntité):
                        raise AttributeError("[Création de carte] Le plan " + str(source) + ">Séquence>" + clé_str + str(plan_dict) + '>' + str(anim_plan_dict) + " contient une clé invalide : " + str(e) + " qui n'est ni 'Dialogue Groupe', ni 'Dialogue ID', ni 'Temps', ni un 'Anim ID' de cette carte.")

                    if estEntité or e == "Mélios":
                        if type(anim_plan_dict[e]) != list or len(anim_plan_dict[e]) != 2 or (type(anim_plan_dict[e][0]) != int and type(anim_plan_dict[e][0]) != float) or (type(anim_plan_dict[e][1]) != int and type(anim_plan_dict[e][1]) != float):
                            raise TypeError("[Création de carte] L'élément " + e + " dans "  + str(source) + ">Séquence>" + clé_str + str(plan_dict) + '>' + str(anim_plan_dict) + " doit être de type list[int|float] de longueur 2")
                        
                        plan.personnages[-1].append(e)
                        plan.personnages_positions[-1].append(Vec2(anim_plan_dict[e][0],anim_plan_dict[e][1]))
                    
                    if e == "Dialogue Groupe":
                        if not "Dialogue ID" in anim_plan_dict:
                            raise AttributeError("[Création de carte] " + str(source) + '>Séquences>' + clé_str + str(plan_dict) + '>' + str(anim_plan_dict) + " ne possède pas d'élément 'Dialogue ID'.")
                        
                        dialogues : tuple[str,str] = self.chargerDialogue(anim_plan_dict["Dialogue Groupe"],anim_plan_dict["Dialogue ID"])
                        plan.dialogues[-1] = dialogues[1]
                        plan.titres[-1] = dialogues[0]

                    if e == "Temps":
                        if type(anim_plan_dict["Temps"]) != int and type(anim_plan_dict["Temps"]) != float:
                            raise TypeError( TypeError("[Création de carte] L'élément " + e + " dans "  + str(source) + ">Séquence>" + clé_str + str(plan_dict) + '>' + str(anim_plan_dict) + " doit être de type int ou float."))
                        plan.temps.append(anim_plan_dict["Temps"])
                
        elif "estAnimation" in plan_dict and type(plan_dict["estAnimation"] != bool):
            raise TypeError("[Charger Plan] L'élément 'estAnimation' dans " + source + '>' + clé_str + str(plan_dict) + " doit être de type bool.")
        else:
            plan.personnages.append([])
            plan.personnages_positions.append([])
            plan.dialogues.append("")
            plan.titres.append("")
            for e in list(plan_dict.keys()):
                estEntité = False
                if not (e == "Dialogue Groupe" or e == "Dialogue ID" or e == "Mélios"):
                    for en in entités:
                        if en[2] == e:
                            estEntité = True

                if not (e == "Dialogue Groupe" or e == "Dialogue ID" or e == "Mélios" or estEntité):
                    raise AttributeError("[Création de carte] Le plan " + str(source) + ">Séquence>" + clé_str + str(plan_dict) + " contient une clé invalide : " + str(e) + " qui n'est ni 'Dialogue Groupe', ni 'Dialogue ID', ni un 'Anim ID' de cette carte.")

                if estEntité or e == "Mélios":
                    if type(plan_dict[e]) != list or len(plan_dict[e]) != 2 or (type(plan_dict[e][0]) != int and type(plan_dict[e][0]) != float) or (type(plan_dict[e][1]) != int and type(plan_dict[e][1]) != float):
                        raise TypeError("[Création de carte] L'élément " + e + " dans "  + str(source) + ">Séquence>" + clé_str + str(plan_dict) + " doit être de type list[int|float] de longueur 2")
                    
                    plan.personnages[0].append(e)
                    plan.personnages_positions[0].append(Vec2(plan_dict[e][0],plan_dict[e][1]))
                
                if e == "Dialogue Groupe":
                    if not "Dialogue ID" in plan_dict:
                        raise AttributeError("[Création de carte] " + str(source) + '>Séquences>' + clé_str + " ne possède pas d'élément 'Dialogue ID'.")
                    
                    dialogues : tuple[str,str] = self.chargerDialogue(plan_dict["Dialogue Groupe"],plan_dict["Dialogue ID"])
                    plan.dialogues[0] = dialogues[1]
                    plan.titres[0] = dialogues[0]
        return plan
    
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
