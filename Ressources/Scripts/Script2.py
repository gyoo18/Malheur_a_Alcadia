from __future__ import annotations
from InclusionsCirculaires.Scripts_Jeu import *
from Entités.Personnages import Joueur
from Maths.Vec2 import Vec2

jeu : Jeu = None
joueur : Joueur = None
roi : Personnage = None
delain : Personnage = None
exécuté : bool = False

def initialiser():
    from Jeu import Jeu
    global jeu
    global joueur
    global roi
    global delain

    jeu = Jeu.avoirJeu()
    jeu.conditionsDeTransitionManuelles = True
    for e in jeu.carte.entités:
        if e.animID == "Mélios":
            joueur = e
        if e.animID == "Delain":
            delain = e
        if e.animID == "Roi":
            roi = e

def mettreÀJour():
    from Jeu import ÉtatJeu
    global jeu
    global joueur
    global roi
    global delain
    global exécuté

    if not jeu.état.v in [ÉtatJeu.ÉCHEC,ÉtatJeu.SUCCÈS,ÉtatJeu.TRANSITION,ÉtatJeu.TERMINÉ]:
        if Vec2.distance(joueur.pos,delain.pos) <= 1:
            jeu.état.v = ÉtatJeu.ÉCHEC
        if not delain.estVivant or not roi.estVivant:
            jeu.état.v = ÉtatJeu.SUCCÈS

    if jeu.état.v == ÉtatJeu.SUCCÈS:
        if not delain.estVivant:
            jeu.état.scène_étape = 1
        if not roi.estVivant and not exécuté:
            exécuté = True
        elif not roi.estVivant and exécuté:
            jeu.état.v = ÉtatJeu.TERMINÉ

def Terminer():
    jeu.conditionsDeTransitionManuelles = False