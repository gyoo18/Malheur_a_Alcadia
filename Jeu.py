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
import tkinter as tk
from InclusionsCirculaires.Jeu_Peintre import *
from GUI.TkFenetre import TkFenetre
from Maths.Vec2 import Vec2

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
        import menu
        self.état : ÉtatJeu = ÉtatJeu()    # Indique l'état du jeu
        self.chapitre : Chapitre = Chapitre()   # Indique le chapitre scénaristique actuel et la zone.
        self.choix : str = ""       # Décrit le choix que le joueur a fait à la fin du niveau s'il y a lieu
        self.menu : MenuContextuel = MenuContextuel() # Décrit le menu contextuel ouvert ou précédemment ouvert.
        self.carte : Carte = None
        self.conditionsDeTransitionManuelles = False

        self.dialogue_jeu_temps_début :float = 0.0

        self.tkracine = tk.Tk()
        self.tkracine.geometry("1024x1024")
        self.tkracine.configure(bg="#191a1e")
        menu.initialiserMenus(self.tkracine)
        self.tkracine.bind("<Configure>",menu.surModificationFenêtre)
        self.peintre = Peintre(self.tkracine)

        self.vieille_taille : Vec2 = Vec2(self.tkracine.winfo_width(),self.tkracine.winfo_height())

        self.tkracine.protocol("WM_DELETE_WINDOW",self.surFenêtreFermée)

        self.frame_actuelle : TkFenetre = None

        self.case_sélectionnée : Vec2 = None
        self.entité_sélectionnée : Vec2 = None
    
    def avoirJeu():
        if Jeu.jeu == None:
            Jeu.jeu = Jeu()
        return Jeu.jeu

    def miseÀJour(self):
        import menu
        res = GestionnaireRessources.Ressources.avoirRessources()

        if self.état.v == ÉtatJeu.MENU:
            menu.menuPrincipal()
        elif self.état.v == ÉtatJeu.MENU_CONTEXTUEL:
            menu.menu_contextuel()
        elif self.état.v in [ÉtatJeu.JEU,ÉtatJeu.DÉBUT,ÉtatJeu.SUCCÈS,ÉtatJeu.ÉCHEC,ÉtatJeu.SCÈNE]:
            menu.jeu()
        
        if self.état.v in [ÉtatJeu.DÉBUT,ÉtatJeu.SUCCÈS,ÉtatJeu.ÉCHEC,ÉtatJeu.SCÈNE]:
            for i in range(len(self.carte.entités)):
                self.carte.entités[i].MiseÀJour()

        # os.system("cls" if os.name == 'nt' else "clear")
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
                self.tkracine.after_idle(lambda: self.peintre.surModificationFenetre(None))
                if self.carte.estScène:
                    self.état.v = ÉtatJeu.SCÈNE
                else:
                    self.état.v = ÉtatJeu.DÉBUT
                for e in self.carte.entités:
                    e.MiseÀJour()

                self.entité_sélectionnée = None
                self.case_sélectionnée = None
            else:
                self.état.v = ÉtatJeu.TERMINÉ

        if self.carte.script != None:
            GestionnaireScripts.MettreÀJourScript(self.carte.script)

        if self.peintre.estVisible:
            self.tkracine.after_idle(self.peintre._display)
        self.tkracine.update_idletasks()
        self.tkracine.update()
        # self.tkracine.mainloop()

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

        if res.joueur == None:
            res.joueur = Joueur()

        joueur = copy.deepcopy(res.joueur)
        joueur.pos = self.carte.joueur_pos_init
        joueur.carte = self.carte
        self.carte.entités.append(joueur)

        if self.carte.script != None:
            GestionnaireScripts.InitialiserScript(self.carte.script)
        
        self.peintre.changerCarte(self.carte)
    
    def surFenêtreFermée(self):
        self.état.v = ÉtatJeu.TERMINÉ

    def déselectionner(self):
        self.case_sélectionnée = None
        self.entité_sélectionnée = None
        self.carte.déselectionner()