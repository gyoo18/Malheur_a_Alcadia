from __future__ import annotations
from InclusionsCirculaires.Scripts_Jeu import *
from Entités.Personnages import Joueur,Personnage
from Maths.Vec2 import Vec2

jeu : Jeu = None
joueur : Joueur = None
fils : Personnage = None

def initialiser():
    from Jeu import Jeu
    global jeu
    global joueur
    global fils
    jeu = Jeu.avoirJeu()
    for e in jeu.carte.entités:
        if type(e) == Joueur:
            joueur = e
        if e.animID == "Fils":
            fils = e
    jeu.conditionsDeTransitionManuelles = True

def mettreÀJour():
    from Jeu import ÉtatJeu
    global jeu
    global joueur
    global fils

    if not jeu.état.v in [ÉtatJeu.ÉCHEC,ÉtatJeu.SUCCÈS,ÉtatJeu.TRANSITION,ÉtatJeu.TERMINÉ]:
        if Vec2.distance(joueur.pos,fils.pos) <= 1:
            jeu.état.v = ÉtatJeu.ÉCHEC
        if not fils.estVivant:
            jeu.état.v = ÉtatJeu.SUCCÈS

def Terminer():
    jeu.conditionsDeTransitionManuelles = False