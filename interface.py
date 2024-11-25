from Ressources import Ressources
from Jeu import Jeu, ÉtatJeu
import dialogue

def miseÀJour(jeu : Jeu):
    res = Ressources.avoirRessources()
    i = input("Continuer? [O/N] : ").capitalize()

    if i == "N":
        print("Sortie du jeu.")
        jeu.état.v = ÉtatJeu.TERMINÉ

    match jeu.état.v:
        case ÉtatJeu.ZONE1:
            dialogue.jeu_principal(jeu)
            if jeu.état.v != ÉtatJeu.TERMINÉ:
                jeu.état.v = ÉtatJeu.ZONE2
        case ÉtatJeu.ZONE2:
            dialogue.jeu_principal(jeu)
            if jeu.état.v != ÉtatJeu.TERMINÉ:
                jeu.état.v = ÉtatJeu.ZONE3
        case ÉtatJeu.ZONE3:
            dialogue.jeu_principal(jeu)
            if jeu.état.v != ÉtatJeu.TERMINÉ:
                jeu.état.v = ÉtatJeu.TERMINÉ
        case ÉtatJeu.MENU:
            i = input("Voici le menu.\n Quitter : [Q]\n Poursuivre : [P]\n").capitalize()
            if i == "Q":
                jeu.état.v = ÉtatJeu.TERMINÉ
            if i == "P":
                jeu.état.v = ÉtatJeu.ZONE1
        case ÉtatJeu.TERMINÉ:
            return

    if i == "O":
        print("Mise à jour des entitées.")
        for i in range(len(res.entités)):
            res.entités[i]._MiseÀJourIA()
        print("Entitées mises à jours.")
        res.cartes[0].dessiner()