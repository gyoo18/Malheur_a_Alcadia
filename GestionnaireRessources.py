from __future__ import annotations
from InclusionsCirculaires.Ressources_Jeu import *
from Dessin.Texture import Texture
from Dessin.Nuanceurs.Nuanceur import Nuanceur
from Dessin.Image import Image
from Carte.Carte import *
from Carte.Tuile import Tuile
from Entités.Entité import *
from Entités.Golem import *
from Entités.Paysan import *
from Entités.Personnages import *
import codecs
import traceback
import json
import imageio.v3 as ImageIO
from GUI.TkFenetre import TkFenetre
from GUI.Log import Log
from TFX import *

class Ressources:

    ressources : Ressources = None # Structure du singleton

    def __init__(self) -> Ressources:
        # Initialisation des dictionnaires de ressources. Les ressources sont accessibles par leur nom
        self.cartes : dict[Carte] = {}
        self.entités : dict[Entité] = {}
        self.dialogues : dict[list[str]] = {}
        self.dialogues_titres : dict[list[str]] = {}
        self.textures : dict[Texture] = {}
        self.nuanceurs : dict[Nuanceur] = {}
        self.frames : dict[TkFenetre] = {}

        # Indexe des ressources. Dictionnaire décrivant l'emplacement de chaque fichier, en fonction de son nom.
        # Ainsi, si une ressource n'est pas chargée, l'indexe peut pointer vers son emplacement.
        self.indexe_ressources : dict = None
        fichier = codecs.open("Ressources/Définitions.json","r","utf-8") # Renvoie FileNotFoundError
        self.indexe_ressources = json.load(fichier)
        fichier.close()

        self.joueur = None # Référence au joueur.

    def avoirRessources() -> Ressources:
        """Renvoie l'instance unique de Ressources.

        Initialise Ressource lors du premier appel.

        **Ne pas appeller Ressources.__init__().**

        Returns:
            Ressources : Instance unique de Ressources qui gère toutes les ressources du jeu.
        """
        # Initialisation du singleton
        if Ressources.ressources == None:
            Ressources.ressources = Ressources()
        return Ressources.ressources
    
    def détruire(self):
        """Non implémenté
        """
        # Idéallement, appelé lors de la phase de destruction du programme.
        print(coul("Ressources.détruire n'est pas implémenté",ROUGE))
        pass

    def chargerCarte(self, nom : str) -> Carte:
        """Charge la carte spécifiée par `nom` et renvoie un objet `Carte` correspondant.

        Appelle `Ressources.chargerDialogue()` et `Ressources._chargerPlan()`

        Les entitées de la carte ne seront pas initialisé. Il est nécessaire de les initialiser avant de les utiliser.
        Il est préférable d'utiliser Jeu.changerCarte() pour cela.

        `nom` doit être le même définit dans `Définitions.json`. Cette fonction chargera alors le fichier correspondant.
        À noter que seul le dossier local à l'intérieur de `Ressources/Cartes/` doit être spécifié. Ainsi, avec une carte sous
        `Ressources/Cartes/A.json`, on ne spécifiera que `"carte":"A.json"` et avec une carte sous `Ressources/Cartes/Groupe/B.json`,
        on ne spécifiera que `"carte2":"Groupe/B.json"`. Pour charger l'un ou l'autre, il faut donc appeler `Ressources.chargerCarte("carte")`
        ou `Ressources.chargerCarte("carte2")`.

        Si la carte a déjà été chargée, elle sera simplement retournée.

        Args:
            nom (str): nom de la carte tel que spécifié dans `Définitions.json`

        Raises:
            AttributeError: Si `nom` n'est pas spécifié dans `Définitons.json`
            AttributeError: Si le fichier ne contient pas l'un des éléments suivants : "Carte", "Entités", "Prochaine", "Joueur_pos" ou "Séquence"
            AttributeError: Si "Scène" est `false` et que l'élément "Séquence" ne contient pas exactement les éléments suivants : "Début", "Jeu", "Succès" ou "Échec"
            ValueError: Si une tuile dans "Carte" n'est pas l'un des types reconnus, soit "0","*","~" ou "$"
            TypeError: Si l'un des éléments dans le fichier n'est pas du bon type.
            FileNotFoundError: Si le fichier spécifié dans `Définitions.json` ne se trouve pas dans Ressources/Cartes/

        Returns:
            Carte : Carte décrite dans le fichier
        """
        if nom in self.cartes.keys():
            # Si la carte est déjà chargée, simplement la renvoyer
            return self.cartes[nom]
        else: 
            # Si la carte n'est pas chargée
            # Vérifier si le nom spécifié est bien présent dans l'indexe des ressources
            if not nom in self.indexe_ressources["Cartes"]:
                # Si le nom n'est pas présent
                # Faire planter le programme avec informations pour éviter un bug introuvable
                raise AttributeError("[Charger Carte] La carte " + nom + " n'est pas définie.")
            # Si le nom est bien définis
            source = "Ressources/Cartes/" + self.indexe_ressources["Cartes"][nom]   # Toutes les cartes se trouvent dans le dossier Ressources/Cartes/, il ne reste donc qu'à chercher le nom du fichier dans l'indexe.
            # Initialisation des composantes de la carte
            matrice : list[list[Tuile]] = []
            entités : list[tuple[str,Vec2|None,str|None]] = []
            colonnes = 0
            lignes = 0
            estScène : bool= False
            séquences : Séquence|dict[Séquence] = None

            # Chargement de la carte
            fichier = codecs.open(source,"r","utf-8")   # PEUT RENVOYER FILE_NOT_FOUND_ERROR
            carte_dict : dict = json.load(fichier)             # Si tel est le cas, faire planter le programme avec informations pour éviter un bug introuvable.
            fichier.close()

            # Vérifier que le fichier est bien construit et faire planter le programme sinon, pour éviter un bug introuvable.
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
            
            # Charger la matrice de Tuiles qui formeront la carte.
            # Parcourir tout les éléments de la double liste spécifiée dans le fichier.
            # Dans le fichier, la liste externe représente les y et la liste interne représente les x, ce qui veut dire qu'on l'adresse ainsi : Carte[y][x]
            #   La matrice de Carte s'adresse à l'inverse : Carte.matrice[x][y]. Ainsi, il faut inverser les x et les y en parcourant la liste interne dans la
            #   boucle externe et vice-versa.
            for x in range(len(carte_dict["Carte"][0])):
                colonne = []
                for y in range(len(carte_dict["Carte"])):
                    # Construire la tuile selon le type spécifié
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
                            # Si la tuile n'est pas d'un type reconnus, faire planter le programme avec information pour empêcher une bug introuvable
                            raise ValueError("La tuile " + str(carte_dict[x][y]) + " à la position " + str(x) + ';' + str(y) + " n'est pas une tuile reconnue.")
                matrice.append(colonne)
            # Définir la taille de la carte
            colonnes = len(matrice)
            lignes = len(matrice[0])
            
            # Charger les entités.
            # Puisque certaines caractéristiques des entités doivent être unique par entité, mais que le système permet la réutilisation des définitions,
            #   cette section n'enregistre que les informations de chargement, qui seront utilisés par la suite par Jeu.changerCarte() pour charger les entités correctement.
            liste_entités : list[dict] = carte_dict["Entités"]
            for e in liste_entités:
                unité = (e["ID"],None,None) # Chaque unité pré-chargement est définie par un 3-tuple comme suit : (son nom, sa position initiale, son identificateur d'animation). Les deux derniers sont optionels.
                # Si la position est définie
                if "Position" in e:
                    # S'assurer que l'élément "Position" est définie avec le bon type et sinon, faire planter le programme avec information pour éviter un bug introuvable.
                    if type(e["Position"]) != list or (type(e["Position"][0]) != int and type(e["Position"][0]) != float) or (type(e["Position"][1]) != int and type(e["Position"][1]) != float):
                        raise TypeError("[Création de carte] L'élément 'Position' de " + e["ID"] + " doit être de type list[ int ou float ].")
                    # Rajouter la position initiale à l'unité
                    unité = (unité[0],Vec2(float(e["Position"][0]),float(e["Position"][1])),None)
                if "Anim ID" in e:
                    # S'assurer que l'élément "Anim ID" est défini avec le bon type et sinon, faire planter le programme avec information pour éviter un bug introuvable
                    if type(e["Anim ID"]) != str:
                        raise TypeError("[Création de carte] L'élément 'Anim ID' de " + e["ID"] + " doit être de type str.")
                    # Rajouter l'identificateur d'animation à l'unité
                    unité = (unité[0],unité[1],e["Anim ID"])

                entités.append(unité)
            
            # Détecter si la carte est une scène ou non
            if "Scène" in carte_dict:
                # S'assurer que l'élément "Scène" est défini avec le bon type et sinon, faire planter le programme avec information pour éviter un bug introuvable
                if type(carte_dict["Scène"]) != bool:
                    raise TypeError("[Création de carte] L'élément 'estScène' de " + str(source) + " doit être de type bool.")
                estScène = carte_dict["Scène"]
            
            # Charger la séquence
            if estScène:
                # Si la carte est une scène elle ne contient qu'une seule séquence et une liste de plans.
                séquences = Séquence()
                # S'assurer que l'élément "Séquence" est défini avec le bon type et sinon, faire planter le programme avec information pour éviter un bug introuvable
                if type(carte_dict["Séquence"]) != list:
                    raise TypeError("[Création de carte] L'élément 'Séquence' de " + str(source) + " doit être une list[dict]. Changez 'estScène' à False si vous voulez en faire une liste.")
                for plan_dict in carte_dict["Séquence"]:
                    # S'assurer que les sous-éléments de "Séquence" sont définits avec le bon type et sinon, faire planter le programme avec information pour éviter un bug introuvable
                    if type(plan_dict) != dict:
                        raise TypeError("[Création de carte] Les éléments de 'Séquence' dans " + str(source) + " ne doit contenir que des dictionnaires.")
                    
                    # Charger le plan
                    plan : Plan = self._chargerPlan(plan_dict,entités,source,None) 
                    séquences.plans.append(plan)
            else:
                # Si la carte n'est pas une scène, elle contient quatre séquences dans un dictionnaire sous les clés "Début", "Jeu", "Succès" et "Échec"
                séquences = {}
                # S'assurer que l'élément "Séquence" est défini avec le bon type et sinon, faire planter le programme avec information pour éviter un bug introuvable
                if type(carte_dict["Séquence"]) != dict:
                    raise TypeError("[Création de carte] L'élément 'Séquence' de " + str(source) + " doit être un dict[list[dict]]. Changez 'estScène' à False si vous voulez en faire une liste.")
                # S'assurer que le dictionaire "Séquence" contient exactement les éléments "Début", "Jeu", "Succès" et "Échec" et sinon, faire planter le programme avec information pour éviter un bug introuvable
                if not "Début" in carte_dict["Séquence"] or not "Jeu" in carte_dict["Séquence"] or not "Succès" in carte_dict["Séquence"] or not "Échec" in carte_dict["Séquence"]:
                    raise AttributeError("[Création de carte] L'élément 'Séquence' de " + str(source) + " doit contenir les clé suivantes : 'Début', 'Jeu', 'Succès' et 'Échec', qui sont toutes des list[dict]")
                # S'assurer que tout les éléments de "Séquence" sont des listes et sinon, faire planter le programme avec information pour éviter un bug introuvable
                if type(carte_dict["Séquence"]["Début"]) != list or type(carte_dict["Séquence"]["Jeu"]) != list or type(carte_dict["Séquence"]["Succès"]) != list or type(carte_dict["Séquence"]["Échec"]) != list:
                    raise TypeError("[Création de carte] Les clés de l'élément 'Séquence' de " + str(source) + " ne sont pas toutes des listes.")
                
                # Passer à travers chaque clé du dictionnaire "Séquence"
                for clé in list(carte_dict["Séquence"].keys()):
                    séquence : Séquence = Séquence()
                    # S'assurer que la clé est une clé reconnue et sinon, faire planter le programme avec information pour éviter un bug introuvable
                    if not clé in [Séquence.DÉBUT,Séquence.JEU,Séquence.SUCCÈS,Séquence.ÉCHEC]:
                        raise AttributeError("[Création de carte] La clé " + str(clé) + " de séquence n'est pas une clé reconnue. Veuillez utiliser 'Début', 'Jeu', 'Succès' ou 'Échec'.")

                    séquence.position = clé # Attribuer la position scénaristique de la séquence en fonction de la clé.
                    
                    # Passer à travers tout les plans de la séquence
                    for plan_dict in carte_dict["Séquence"][clé]:
                        # S'assurer que tout les plans de la séquence sont du bon type et sinon, faire planter le programme avec information pour éviter un bug introuvable
                        if type(plan_dict) != dict:
                            raise TypeError("[Création de carte] " + str(source) + ">Séquence>" + clé + " ne doit contenir que des dictionnaires.")
                        
                        # Charger le plan
                        plan : Plan = self._chargerPlan(plan_dict, entités,source,clé)
                        séquence.plans.append(plan)
                    séquences[clé] = séquence # Enregistrer la séquence

            # Charger la référence au script, s'il y en a un.
            script : str = None
            if "Script" in carte_dict:
                # S'assurer que l'élément "Script" est du bon type.
                if type(carte_dict["Script"]) != str:
                    raise TypeError("[Création de carte] L'élément 'Script' de " + source + " doit être de type string.")
                script = carte_dict["Script"]

            # Charger la référence à la prochaine carte
            # S'assurer que l'élément "Prochaine" est du bon type
            if type(carte_dict["Prochaine"]) != str:
                raise TypeError("[Création de carte] "+str(source)+">Prochaine doit être de type string.")
            # S'assurer que la référence à la prochaine carte point à une carte valide, ou à la fin du jeu.
            if not carte_dict["Prochaine"] in self.indexe_ressources["Cartes"] and not carte_dict["Prochaine"] == "$Terminé":
                raise ValueError("[Création de carte] "+str(source)+">Prochaine n'est pas une référence à une carte valide.")
            prochaine = carte_dict["Prochaine"]

            # Charger la position initiale du joueur
            # S'assurer que l'élément "Joueur_pos" est du bon type
            if type(carte_dict["Joueur_pos"]) != list or len(carte_dict["Joueur_pos"]) != 2 or (type(carte_dict["Joueur_pos"][0]) != float and type(carte_dict["Joueur_pos"][0]) != int) or (type(carte_dict["Joueur_pos"][1]) != float and type(carte_dict["Joueur_pos"][1]) != int):
                raise TypeError("[Création de carte] "+str(source)+">Joueur_pos doit être de type list[int|float] et de longueur 2")
            joueur_pos_init = Vec2(carte_dict["Joueur_pos"][0],carte_dict["Joueur_pos"][1])

            # Créer la carte
            carte = Carte(estScène,colonnes,lignes,matrice,entités,joueur_pos_init,séquences,prochaine)
            carte.estScène = estScène
            carte.script = script

            self.cartes[nom] = carte # Ajouter la carte au dictionnaire de cartes chargées

            return carte

    def chargerEntité(self,nom : str) -> Entité:
        """Charge l'entité spécifiée par `nom` et renvoie un objet Entité correspondant.

        Cette fonction n'est pas appellée par `Ressources.chargerEntité()`, mais par `Jeu.changerCarte()`.

        `nom` doit être le même définit dans `Définitions.json`. Cette fonction chargera alors le fichier correspondant.
        À noter que seul le dossier local à l'intérieur de `Ressources/Entités/` doit être spécifié. Ainsi, avec une entité sous
        `Ressources/Entités/A.json`, on ne spécifiera que `"entité":"A.json"` et avec une carte sous `Ressources/Entités/Groupe/B.json`,
        on ne spécifiera que `"entité2":"Groupe/B.json"`. Pour charger l'un ou l'autre, il faut donc appeler `Ressources.chargerEntité("entité")`
        ou `Ressources.chargerEntité("entité2")`.

        Si l'entité a déjà été chargée, elle serat simplement retournée

        Raises:
            AttributeError: Si `nom` n'est pas spécifié dans `Définitions.json`
            AttributeError: Si le fichier ne contient pas un élément "Type"
            ValueError: Si "Type" n'a pas une valeur reconnue parmis "GolemTerre", "GolemEau", "GolemFeu", "GolemOr", "Gosse", "Mineur", "Chevalier", "Arbalettier", "Prêtre" ou "Personnage".
            TypeError: Si l'un des attributs optionnels n'a pas le bon type.
            FileNotFoundError: Si le fichier spécifié dans `Définitions.json` ne se trouve pas dans Ressources/Entités/

        Returns:
            Entité : Entitée décrite dans le fichier. Peut être `GolemTerre`, `GolemEau`, `GolemFeu`, `GolemOr`, `Gosse`, `Mineur`, `Chevalier`, `Arbalettier`, `Prêtre` ou `Personnage`, selon le cas.
        """
        if nom in self.entités.keys():
            return copy.deepcopy(self.entités[nom])
        else :
            # Charger l'unité
            # S'assurer que le nom spécifié se trouve dans l'indexe
            if not nom in self.indexe_ressources["Entités"]:
                raise AttributeError("[Charger Entité] L'entité " + nom + " n'est pas définie.")
            # Charger le fichier
            source = "Ressources/Entités/" + self.indexe_ressources["Entités"][nom] # Toutes les entités se trouvent dans le dossier Ressources/Entités/, il ne reste donc qu'à chercher le nom du fichier dans l'indexe.
            fichier = codecs.open(source,"r","utf-8")   # PEUT RENVOYER FILE_NOT_FOUND_ERROR
            unitée_dict : dict = json.load(fichier)
            fichier.close()
            
            # S'assurer que l'élément "Type" est présent dans le fichier
            if not "Type" in unitée_dict:
                raise AttributeError("[Charger Entité] L'entité " + nom + " doit posséder un élément 'Type'.")

            # Créer l'entité en fonction du type spécifié
            unitée = None
            match unitée_dict["Type"]:
                case "GolemTerre":
                    unitée = GolemTerre()
                case "GolemEau":
                    unitée = GolemEau()
                case "GolemFeu":
                    unitée = GolemFeu()
                case "GolemOr":
                    unitée = GolemDoré()
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
            
            # Si le nom est spécifié
            if "Nom" in unitée_dict:
                # S'assurer que le nom est un string
                if type(unitée_dict["Nom"]) != str:
                    raise TypeError("[Création de carte] L'élément 'Nom' d'une entité doit être un string.")
                unitée.nom = unitée_dict["Nom"]
                unitée.nomAffichage = unitée.nom

            # Si la référence à la texture est spécifiée            
            if "Texture" in unitée_dict:
                # S'assurer que la référence à la texture est un string
                if type(unitée_dict["Texture"]) != str:
                    raise TypeError("L'élément 'Texture' de " + unitée.nom + " doit être de type str.")
                # S'assurer que la texture est définie dans l'indexe
                if not unitée_dict["Texture"] in self.indexe_ressources["Textures"]:
                    raise ValueError("La texture "+unitée_dict["Texture"]+" de "+unitée.nom+" n'est pas spécifiée dans 'Définitions.json'")
                unitée.dessin_Image = Image(unitée_dict["Texture"])

            # Si les PV maximums sont spécifiés
            if "PVMax" in unitée_dict:
                # S'assurer que l'élément "PVMax" est un nombre
                if type(unitée_dict["PVMax"]) != int and type(unitée_dict["PVMax"]) != float:
                    raise TypeError("L'élément 'PVMax' de " + unitée.nom + " doit être un int ou un float.")
                unitée.PVMax = int(unitée_dict["PVMax"])

            # Si les PV initiaux sont spécifiés
            if "PV" in unitée_dict:
                # S'assurer que l'élément "PV" est un nombre
                if type(unitée_dict["PV"]) != int and type(unitée_dict["PV"]) != float:
                    raise TypeError("L'élément 'PV' de " + unitée.nom + " doit être un int ou un float.")
                unitée.PV = unitée_dict["PV"]

            # Si le temps de chargement est spécifié
            if "Temp Chargement" in unitée_dict:
                # S'assurer que l'élément "Temp Chargement" est un nombre
                if type(unitée_dict["Temp Chargement"]) != int and type(unitée_dict["Temp Chargement"]) != float:
                    raise TypeError("L'élément 'Temp Chargement' de " + unitée.nom + " doit être un int ou un float.")
                unitée.TEMP_CHARGEMENT = int(unitée_dict["Temp Chargement"])

            # Si les dégats de l'attaque chargée sont spécifiés 
            if "Attaque Chargée" in unitée_dict:
                # S'assurer que l'élément "Attaque Chargée" est un nombre
                if type(unitée_dict["Attaque Chargée"]) != int and type(unitée_dict["Attaque Chargée"]) != float:
                    raise TypeError("L'élément 'Attaque Chargée' de " + unitée.nom + " doit être un int ou un float.")
                unitée.attaque_chargée = unitée_dict["Attaque Chargée"]

            # Si les dégats de l'attaque normale sont spécifés
            if "Attaque Normale" in unitée_dict:
                # S'assurer que l'élément "Attaque Normale" est un nombre
                if type(unitée_dict["Attaque Normale"]) != int and type(unitée_dict["Attaque Normale"]) != float:
                    raise TypeError("L'élément 'Attaque Normale' de " + unitée.nom + " doit être un int ou un float.")
                unitée.attaque_normale_dégats = unitée_dict["Attaque Normale"]

            # Si le pourcentage de réduction des dégats en mode défense est spécifié
            if "Dégats Défense" in unitée_dict:
                # S'assurer que l'élément "Dégats Défense" est un nombre
                if type(unitée_dict["Dégats Défense"]) != int and type(unitée_dict["Dégats Défense"]) != float:
                    raise TypeError("L'élément 'Dégats Défense' de " + unitée.nom + " doit être un int ou un float.")
                unitée.dégats_défense = unitée_dict["Dégats Défense"]

            # Si le pourcentage de réduction des dégats en mode libre est spécifié
            if "Dégats Libres" in unitée_dict:
                # S'assurer que l'élément "Dégats Libres" est un nombre
                if type(unitée_dict["Dégats Libres"]) != int and type(unitée_dict["Dégats Libres"]) != float:
                    raise TypeError("L'élément 'Dégats Libres' de " + unitée.nom + " doit être un int ou un float.")
                unitée.dégats_libre = unitée_dict["Dégats Libres"]

            # Si le pourcentage de réduction des dégats en mode charger est spécifié
            if "Dégats Charger" in unitée_dict:
                # S'assurer que l'élément "Dégats Charger" est un nombre
                if type(unitée_dict["Dégats Charger"]) != int and type(unitée_dict["Dégats Charger"]) != float:
                    raise TypeError("L'élément 'Dégats Charger' de " + unitée.nom + " doit être un int ou un float.")
                unitée.dégats_charger = unitée_dict["Dégats Charger"]

            # Si le camp est spécifié
            if "Camp" in unitée_dict:
                # S'assurer que l'élément "Camp" est un string
                if type(unitée_dict["Camp"]) != str:
                    raise TypeError("L'élément 'Camp' de " + unitée.nom + " doit être un string.")
                unitée.Camp = unitée_dict["Camp"]

            # Si les camps ennemis sont spécifiés
            if "Camps Ennemis" in unitée_dict:
                # S'assurer que l'élément "Camps Ennemis" est une liste de string
                if type(unitée_dict["Camps Ennemis"]) != list:
                    raise TypeError("L'élément 'Camps Ennemis' de " + unitée.nom + " doit être de type list[ str ].")
                for c in unitée_dict["Camps Ennemis"]:
                    # S'assurer que chaque éléments de l'élément "Camps Ennemis" sont des strings
                    if type(c) != str:
                        raise TypeError("L'élément 'Camps Ennemis' de " + unitée.nom + " ne doit contenir que des strings.")
                    unitée.campsEnnemis = unitée_dict["Camps Ennemis"]

            # Si l'entité est un personnage et que sa couleur est spécifiée
            if unitée_dict["Type"] == "Personnage" and "Couleur" in unitée_dict:
                # S'assurer que l'élément 'Couleur' est une liste de floats
                if type(unitée_dict["Couleur"]) != list:
                    raise TypeError("L'élément 'Couleur' de " + unitée.nom + " doit être de type list[ float ].")
                for c in unitée_dict["Couleur"]:
                    # S'assurer que chaque éléments de la liste 'Couleur' est un float
                    if type(c) != float:
                        raise TypeError("L'élément 'Couleur' de " + unitée.nom + " ne doit contenir que des float.")
                    unitée.nomAffichage = '<'+str(unitée_dict["Couleur"][0])+';'+str(unitée_dict["Couleur"][1])+';'+str(unitée_dict["Couleur"][2])+'>'+unitée.nom+"</>"
                
            self.entités[nom] = unitée # Enregistrer l'unité dans le dictionnaire
            return unitée
    
    def _chargerDialogue(self, groupe : str, ID : list[int]) -> tuple[str,str]:
        """Fonction interne
        
        Charge les dialogues spécifiés par `ID`, dans le groupe de dialogues spécifé par `groupe` et renvoie un tuple
        contenant le titre à afficher et le string combiné correspondant au dialogue.

        `groupe` doit être le même définit dans `Définitions.json`. Cette fonction chargera alors le fichier correspondant.
        À noter que seul le dossier local à l'intérieur de `Ressources/Dialogues/` doit être spécifié. Ainsi, avec une carte sous
        `Ressources/Dialogues/A.json`, on ne spécifiera que `"dialogue":"A.json"` et avec une carte sous `Ressources/Dialogues/Groupe/B.json`,
        on ne spécifiera que `"dialogue2":"Groupe/B.json"`. Pour charger l'un ou l'autre, il faut donc appeler `Ressources.chargerDialogue("dialogue")`
        ou `Ressources.chargerDialogue("dialogue2")`.

        `ID` correspond aux éléments dans la liste des dialogues spéficiés dans le fichier. Ils seront combinés dans l'ordre de leur spécification.

        Args:
            groupe (str): Groupe de dialogue spécifié. Correspond à la clé spécifiée dans "Définitions.json" et à "Dialogue Groupe" dans le fichier json de la carte
            ID (list[int]): indexes des dialogues à sélectionner dans la liste du groupe de dialogues.

        Raises:
            AttributeError: Si `groupe` n'est pas spécifié dans `Définitions.json`
            AttributeError: Si le fichier ne contient pas les éléments "Titre" et "Dialogues"
            AttributeError: Si l'un des éléments de "Dialogues" de contient pas un élément "Dialogue"
            IndexError: Si l'un des indexes dans `ID` n'est pas contenus dans la liste des Dialogues (plus petit que 0 ou plus grand que len(liste)-1)
            TypeError: Si l'un des éléments du fichier n'est pas du bon type.
            FileNotFoundError: Si le groupe de dialogue spécifié ne se trouve pas dans Ressources/Dialogues/

        Returns:
            tuple[str,str]: Titre et combinaison des dialogues décrite par `ID` et le fichier
        """
        from dialogue import dialogue   # Présent pour éviter des problèmes d'inclusion circulaire

        # Déterminer si tout les éléments du dialogue demandé sont déjà chargés et si oui, les renvoyer, sinon, les charger
        chargerFichier = False  # Indique si on a besoin d'aller chercher les données dans le fichier
        # Si le groupe de dialogue a déjà été ouvert
        if groupe in self.dialogues.keys():
            texte = ""  # Combinaison de tout les dialogues spécifiés
            # Parcourir la liste des dialogues demandés
            for i in ID:
                # Si le dialogue a été chargé
                if self.dialogues[groupe][i] != None:
                    texte += self.dialogues[groupe][i] # L'ajouter au texte
                else:
                    # Si le dialogue n'a pas été chargé, aller chercher dans le fichier
                    chargerFichier = True
                    break
            # Après toute la boucle, si on n'a pas besoin de charger le fichier, renvoyer le résultat
            if not chargerFichier:
                return (self.dialogues_titres[groupe][ID[-1]],texte)
        else:
            # Si le groupe de dialogue n'a jamais été ouvert, charger le fichier.
            chargerFichier = True
            
        # Si on a besoin d'aller chercher dans le fichier
        if chargerFichier:
            # TODO #35 enregistrer l'entièreté du fichier dialogue dans les ressources, car le fichier est déjà entièrement chargé.
            # S'assurer que le groupe de dialogues est bien spécifié dans l'indexe
            if not groupe in self.indexe_ressources["Dialogues"]:
                raise AttributeError("[Charger Dialogue] Le groupe de dialogue : " + str(groupe) + " n'est pas définit dans 'Définitions.json'.")
            # Charger le fichier
            source : str = "Ressources/Dialogues/" + self.indexe_ressources["Dialogues"][groupe]
            dialogue_dict : dict= None
            fichier = codecs.open(source,"r","utf-8")   # PEUT RENVOYER FILE_NOT_FOUND_ERROR
            dialogue_dict = json.load(fichier)
            fichier.close()

            # Si le fichier n'a jamais été ouvert, le groupe de dialogue ne serat pas présent dans le dictionnaire de dialogues. Il faudrat donc le rajouter.
            if not groupe in self.dialogues.keys():
                # Créer une liste de Nones de la longueure de la liste de Dialogues, qui pourrat être remplacée par des string à mesure que les dialogues seront nécessaires
                liste = []
                for i in range(len(dialogue_dict["Dialogues"])):
                    liste.append(None)
                self.dialogues[groupe] = liste
                self.dialogues_titres[groupe] = liste   # Initialiser un liste de titres de la même longueure
            
            # S'assurer que le fichier est bien construit.
            if not "Titre" in dialogue_dict:
                raise AttributeError("[Charger Dialogue] Le groupe de dialogues " + str(source) + " a besoin d'un 'Titre' par défaut.")
            if type(dialogue_dict["Titre"]) != str:
                raise TypeError("[Charger Dialogue] Le titre par défaut du groupe de dialogues " + str(source) + " doit être un string.")
            if not "Dialogues" in dialogue_dict:
                raise AttributeError("[Charger Dialogue] Le groupe de dialogues " + str(source) + " n'a pas de clé 'Dialogue'.")
            if type(dialogue_dict["Dialogues"]) != list:
                raise TypeError("[Charger Dialogue] L'élément 'Dialogue' du groupe de dialogues " + str(source) + " doit être une liste.")
            
            # Initialiser les variables
            dialogue_texte : tuple[str,str] = (dialogue_dict["Titre"],None) # Variable de retour. 2-tuple composé d'un titre et d'un texte de dialogue
            texte : str = ""

            # Parcourir les dialogues voulus
            for i in range(len(ID)):
                if self.dialogues[groupe][ID[i]] != None:
                    texte += self.dialogues[groupe][ID[i]]
                    continue

                if len(dialogue_dict["Dialogues"])-1 < ID[i] or ID[i] < 0:
                    raise IndexError("[Charger Dialogue] L'indexe " + str(ID[i]) + " n'existe pas dans le groupe " + source + ". L'indexe maximum est " + str(len(dialogue_dict["Dialogues"])-1))
                if not "Dialogue" in dialogue_dict["Dialogues"][ID[i]]:
                    raise AttributeError("[Charger Dialogue] Le dialogue à l'indexe " + str(ID[i]) + " du groupe" + source + " n'a pas d'élément 'Dialogue'.")
                if type(dialogue_dict["Dialogues"][ID[i]]["Dialogue"]) != list:
                    raise TypeError("[Charger Dialogue] L'élément 'Dialogue' à l'indexe " + str(ID[i]) + " du groupe " + source + " doit être une liste.")
                
                if "Titre" in dialogue_dict["Dialogues"][ID[i]]:
                    dialogue_texte = (dialogue_dict["Dialogue"][ID[i]]["Titre"],dialogue_texte[1])
                
                personnage : str = None
                if "Personnage" in dialogue_dict["Dialogues"][ID[i]]:
                    if type(dialogue_dict["Dialogues"][ID[i]]["Personnage"]) != str:
                        raise TypeError("[Charger Dialogue] " + source + ">Dialogues>" + str(ID[i]) + ">Personnage n'est pas un string.")
                    personnage = dialogue_dict["Dialogues"][ID[i]]["Personnage"]

                self.dialogues[groupe][ID[i]] = ""
                for d in dialogue_dict["Dialogues"][ID[i]]["Dialogue"]:
                    if type(d) != str:
                        raise TypeError("[Charger Dialogue] " + source + ">Dialogues>" + str(ID[i]) + ">Ligne " + str(dialogue_dict["Dialogues"][ID[i]]["Dialogue"].indexe(d)) + " n'est pas un string.")
                    
                    if personnage:
                        texte += dialogue(d,personnage) + '\n'
                        self.dialogues[groupe][ID[i]] += dialogue(d,personnage) + '\n'
                    else:
                        texte += d + '\n'
                        self.dialogues[groupe][ID[i]] += d + '\n'
                

            
            dialogue_texte = (dialogue_texte[0],texte) # TODO #34 Implémenter la persitstance des dialogues dans la gestion des ressources

            return dialogue_texte
        
    def _chargerPlan(self, plan_dict : dict, entités : list[tuple[str,Vec2|None,str|None]]|None, source : str|None, clé : str|None) -> Plan:
        """Fonction interne
        
        Charge le spécifiée dans `plan_dict` et renvoie un objet `Plan` correspondant.

        Appelle `Ressources.chargerDialogue()`

        Args:
            plan_dict (dict): Dictionnaire décrivant le plan
            entités (list[tuple[str,Vec2|None,str|None]]|None): Descritption pré-chargement de la liste des entités de la carte. Utilisé pour les messages d'erreurs seulement.
            source (str|None): Chemin vers le fichier source de la carte. Utilisé pour les messages d'erreur seulement.
            clé (str|None): Clé de la séquence ("Début", "Jeu", "Succès" ou "Échec"), si applicable. Utilisé pour les messages d'erreurs seulement.

        Raises:
            **Si la séquence n'est pas une animation :**
            AttributeError: Si le plan contient une clé qui n'est pas "Dialogue Groupe", "Dialogue ID" ou "Anim ID"
            AttributeError: Si le plan contient une clé "Dialogue Groupe", mais pas de clé "Dialogue ID"

            **Si la séquence est une animation :**
            AttributeError: Si le plan ne contient pas de clé "Plan"
            AttributeError: Si le sous-plan ne contient une clé qui n'est pas "Dialogue Groupe", "Dialogue ID" ou "Anim ID"
            AttributeError: Si le sous-plan contient une clé "Dialogue Groupe", mais pas de clé "Dialogue ID"

            TypeError: Si l'un des éléments du fichier n'est pas du bon type.

        Returns:
            Plan: Objet plan tel que décrit par `plan_dict`
        """
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
                        
                        dialogues : tuple[str,str] = self._chargerDialogue(anim_plan_dict["Dialogue Groupe"],anim_plan_dict["Dialogue ID"])
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
                    
                    dialogues : tuple[str,str] = self._chargerDialogue(plan_dict["Dialogue Groupe"],plan_dict["Dialogue ID"])
                    plan.dialogues[0] = dialogues[1]
                    plan.titres[0] = dialogues[0]
        return plan
    
    def chargerObj(self,source : str) -> Maillage:
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

    def chargerTexture(self, nom : str) -> Texture:
        """Charge la texture spécifiée par `nom` et renvoie un objet `Texture` correspondant.

        Il est à noter que bien que l'objet `Texture` renvoyé possède les données de la texture, ces données ne sont pas liés avec OpenGL,
        ainsi, pour l'utiliser, il faut par la suite appeler `Texture.construire()` à l'intérieur d'un contexte OpenGL.

        `nom` doit être le même définit dans `Définitions.json`. Cette fonction chargera alors le fichier correspondant.
        À noter que seul le dossier local à l'intérieur de `Ressources/Textures/` doit être spécifié. Ainsi, avec une carte sous
        `Ressources/Textures/A.png`, on ne spécifiera que `"tex":"A.png"` et avec une carte sous `Ressources/Textures/Groupe/B.jpg`,
        on ne spécifiera que `"tex2":"Groupe/B.jpg"`. Pour charger l'un ou l'autre, il faut donc appeler `Ressources.chargerTexture("tex")`
        ou `Ressources.chargerTexture("tex2")`.

        Si la texture a déjà été chargée, elle sera simplement retournée.

        Args:
            nom (str): Nom de la texture. Doit être identique au nom spécifié dans `Définitions.json`

        Returns:
            Texture: Objet Texture se chargeant de gérer la liaison avec OpenGL
        """
        if nom in self.textures.keys():
            return self.textures[nom]
        else:
            source = "Ressources/Textures/" + self.indexe_ressources["Textures"][nom]
            tex = ImageIO.imread(source)

            texture = Texture(source,tex)
            self.textures[nom] = texture
            return texture

    def chargerNuanceur(self, nom : str, enfant : type) -> Nuanceur:
        """Charge le nuanceur spécifiée par `nom` et `enfant` et renvoie un objet `Nuanceur` correspondant.

        Il est à noter que bien que l'objet `Nuanceur` renvoyé possède le code source du nuanceur, ce dernier ne serat pas compilé ou lié avec OpenGL.
        Ainsi, il faut par la suite appeler `Nuanceur.construire()` à l'intérieur d'un contexte OpenGL.

        `nom` doit être le même définit dans `Définitions.json`. Cette fonction chargera alors le fichier correspondant.
        À noter que seul le dossier local à l'intérieur de `Ressources/Nuanceurs/` doit être spécifié. De plus, les deux parties du nuancuers,
        le nuanceur de sommets et le nuanceur de fragement (.vert et .frag) doivent avoir le même nom et `nom` ne doit pointer que vers le nom
        du fichier et non son extension. Ainsi, avec un nuanceur sous `Ressources/Nuanceurs/A.vert` et `Ressources/Nuanceurs/A.frag`, on ne 
        spécifiera que `"nua":"A"` et avec une carte sous `Ressources/Nuanceurs/Groupe/B.vert` et `Ressources/Nuanceurs/Groupe/B.frag`,on ne 
        spécifiera que `"nua2":"Groupe/B"`. Pour charger l'un ou l'autre, il faut donc appeler `Ressources.chargerTexture("nua")`ou 
        `Ressources.chargerTexture("nua2")`.

        Puisque les nuanceurs ont une classe parente et implémentent une nouvelle classe par nuanceur, afin d'obtenir le bon nuanceur, il est
        nécessaire de spécifier la classe correspondante. Ainsi le paramètre `enfant` correspond à la classe correspondante au nuanceur. Ainsi,
        pour un nuanceur `A.vert` et `A.frag` implémentés dans la classe `NuaA`, qui hérite de `Nuanceur`, il faut appeler 
        `Ressources.chargerNuanceur("A",NuaA)` et renverra un objet `NuaA` au lieu d'un objet `Nuanceur`.

        Si le nuanceur a déjà été chargée, il sera simplement retournée.

        Args:
            nom (str): Nom du nuanceur. Doit être identique à celui spécifié dans `Définitions.json`
            enfant (type): Classe spécifique du nuanceur à instancier.

        Returns:
            enfant: Objet enfant de `Nuanceur` spécifié par `enfant`, qui décrit le nuanceur et gère sa connection avec OpenGL
        """
        if nom in self.nuanceurs.keys():
            return self.nuanceurs[nom]
        else:
            source = "Ressources/Nuanceurs/" + self.indexe_ressources["Nuanceurs"][nom]
            fichier = None
            try:
                fichier  = open(source+".vert","r")
            except Exception as e:
                traceback.print_exc()
                traceback.print_exception(e)
                exit(-1)
            lignes = fichier.readlines()
            sommets_source = ""
            for ligne in lignes:
                sommets_source += ligne
            fichier.close()
            
            try:
                fichier  = open(source+".frag","r")
            except Exception as e:
                traceback.print_exc()
                traceback.print_exception(e)
                exit(-1)
            lignes = fichier.readlines()
            fragments_source = ""
            for ligne in lignes:
                fragments_source += ligne
            fichier.close()

            nuanceur = enfant(sommets_source,fragments_source)
            self.nuanceurs[nom] = nuanceur
            return nuanceur
        
    def enregistrerMenu(self, fenêtre : TkFenetre, nom : str):
        """Enregistre une `TkFenetre` dans un dictionnaire sous la clé `nom`

        Pour réobtenir cette fenêtre, voir `Ressources.obtenirMenu()`

        Args:
            fenêtre (TkFenetre): TkFenetre à enregistrer
            nom (str): Nom de référence à la fenêtre

        Raises:
            ValueError: Si la clé `nom` est déjà présente dans le dictionnaire.
        """
        if not nom in self.frames.keys():
            self.frames[nom] = fenêtre
        else:
            raise ValueError("[enregistrerMenu] Un menu au nom de " + str(nom) + " existe déjà. Veuillez indiquer un nom unique pour chaque menu.")
    
    def obtenirMenu(self, nom : str) -> TkFenetre:
        """Renvoie le menu enregistré dans le dictionnaire sous la clé `nom`.

        Pour enregistrer une fenêtre, voir `Ressources.enregsitrerMenu()`

        Args:
            nom (str): Clé sous laquelle la fenêtre a été enregistrée

        Returns:
            TkFenetre: fenêtre enregistrée sous `nom`
        """
        if nom in self.frames.keys():
            return self.frames[nom]
        else:
            traceback.print_exc()
            print(markDownFormattage("<r>**[Erreur : obtenirMenu] Aucun menu du nom de " + str(nom) + " n'existe.**</>"))
            return None