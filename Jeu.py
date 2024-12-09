from __future__ import annotations
import GestionnaireRessources
#from InclusionsCirculaires.Ressources_Jeu import *
from InclusionsCirculaires.Jeu_Carte import *
import os
from Entités.Entité import Entité
from Entités.Golem import *
from Entités.Paysan import *
from Entités.Personnages import *
import copy
from Ressources.Scripts import GestionnaireScripts

class ÉtatJeu:
    MENU = "menu"
    MENU_CONTEXTUEL = "menu contextuel"
    JEU = "Jeu"
    FIN_TOUR = "fin de tour"
    DÉBUT = "Début"
    CHOIX = "choix"
    SUCCÈS = "Succès"
    ÉCHEC = "Échec"
    TRANSITION = "transition"
    TERMINÉ = "terminé"
    SCÈNE = "scène"

    def __init__(self, valeur = MENU):
        self.v : str = valeur
        self.scène_étape = 0
        self.scène_animation_étape = 0

class Chapitre:
    INTRODUCTION = "Introduction"
    CHAPITRE1 = "Prairie"
    CHAPITRE2 = "Cité"
    CHAPITRE3 = "Château"

    def __init__(self, valeur = INTRODUCTION):
        self.v : str = valeur

class MenuContextuel:
    AIDE = "aide"   # Menu d'aide aux commandes
    COMBAT = "combat"   # Menu d'état du combat
    INFO = "info"   # Menu d'état des entités
    SELECT = "select"   # Menu de commande des golems

    def __init__(self, valeur = AIDE):
        self.v = valeur
        self.menu_entité_entité : Entité = None
        self.menu_historique : list[str] = []
        self.menu_select_entité : Golem = None

class Jeu:
    jeu : Jeu = None

    def __init__(self):
        self.état : ÉtatJeu = ÉtatJeu()    # Indique l'état du jeu
        self.chapitre : Chapitre = Chapitre()   # Indique le chapitre scénaristique actuel et la zone.
        self.choix : str = ""       # Décrit le choix que le joueur a fait à la fin du niveau s'il y a lieu
        self.menu : MenuContextuel = MenuContextuel() # Décrit le menu contextuel ouvert ou précédemment ouvert.
        self.carte : Carte = None
        self.conditionsDeTransitionManuelles = False
    
    def avoirJeu():
        if Jeu.jeu == None:
            Jeu.jeu = Jeu()
        return Jeu.jeu

    def miseÀJour(self):
        import menu
        res = GestionnaireRessources.Ressources.avoirRessources()

        if self.état.v == ÉtatJeu.MENU:
            menu.displayUI()
        elif self.état.v == ÉtatJeu.MENU_CONTEXTUEL:
            menu.menu_contextuel()
        else :
            menu.ingameUI()
        
        if self.état.v in [ÉtatJeu.DÉBUT,ÉtatJeu.SUCCÈS,ÉtatJeu.ÉCHEC,ÉtatJeu.SCÈNE]:
            for i in range(len(self.carte.entités)):
                self.carte.entités[i].MiseÀJour()

        os.system("cls" if os.name == 'nt' else "clear")
        if self.état.v == ÉtatJeu.FIN_TOUR:
            paysans = False
            joueur = False
            for e in self.carte.entités:
                if type(e) == Joueur and e.estVivant:
                    joueur = True
                
                if e.camp == Entité.CAMP_PAYSANS:
                    paysans = True
            
            if not paysans and not self.conditionsDeTransitionManuelles:
                self.état.v = ÉtatJeu.SUCCÈS
            elif not joueur and not self.conditionsDeTransitionManuelles:
                self.état.v = ÉtatJeu.ÉCHEC
            else :
                print("Mise à jour des entitées.")
                for i in range(len(self.carte.entités)):
                    self.carte.entités[i].MiseÀJour()
                lo = len(self.carte.entités) -1
                for i in range(len(self.carte.entités)):
                    if not self.carte.entités[lo-i].estVivant:
                        self.carte.entités.pop(lo-i)
                print("Entitées mises à jours.")
                self.état.v = ÉtatJeu.JEU
        
        elif self.état.v == ÉtatJeu.TRANSITION:
            if self.carte.prochaine != "$TERMINÉ":
                if self.carte.script != None:
                    GestionnaireScripts.Terminer(self.carte.script)
                GolemTerre.noms = copy.deepcopy(GolemTerre.noms_originaux)
                GolemEau.noms = copy.deepcopy(GolemEau.noms_originaux)
                GolemFeu.noms = copy.deepcopy(GolemFeu.noms_originaux)
                GolemDoré.noms = copy.deepcopy(GolemDoré.noms_originaux)
                Gosse.noms = copy.deepcopy(Gosse.noms_originaux)
                Mineur.noms = copy.deepcopy(Mineur.noms_originaux)
                Prêtre.noms = copy.deepcopy(Prêtre.noms_originaux)
                Arbalettier.noms = copy.deepcopy(Arbalettier.noms_originaux)
                Chevalier.noms = copy.deepcopy(Chevalier.noms_originaux)
                self.changerCarte(res.chargerCarte(self.carte.prochaine))
                if self.carte.estScène:
                    self.état.v = ÉtatJeu.SCÈNE
                else:
                    self.état.v = ÉtatJeu.DÉBUT
                for e in self.carte.entités:
                    e.MiseÀJour()
            else:
                self.état.v = ÉtatJeu.TERMINÉ

        if self.carte.script != None:
            GestionnaireScripts.MettreÀJourScript(self.carte.script)

    def changerCarte(self,carte : Carte):
        res = GestionnaireRessources.Ressources.avoirRessources()

        if self.carte != None:
            del self.carte

        self.carte = copy.deepcopy(carte)
        for i in range(len(self.carte.entités_préchargement)):
            entité = res.chargerEntité(self.carte.entités_préchargement[i][0])
            entité.pos = self.carte.entités_préchargement[i][1].copie()
            entité.animID = self.carte.entités_préchargement[i][2]
            entité.carte = self.carte
            self.carte.entités.append(entité)

        joueur = copy.deepcopy(res.joueur)
        joueur.pos = self.carte.joueur_pos_init
        joueur.carte = self.carte
        self.carte.entités.append(joueur)

        if self.carte.script != None:
            GestionnaireScripts.InitialiserScript(self.carte.script)