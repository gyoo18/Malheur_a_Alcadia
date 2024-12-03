from Ressources import Ressources
from Jeu import Jeu, ÉtatJeu
import dialogue
import menu

def miseÀJour(jeu : Jeu):
    res = Ressources.avoirRessources()

    if i == "N":
        print("Sortie du jeu.")
        jeu.état.v = ÉtatJeu.TERMINÉ

    if jeu.état.v == ÉtatJeu.MENU:
        menu.displayUI(res.cartes[0],jeu)
    else:
        menu.ingameUI(res.cartes[0],jeu)

    if i == "O":
        print("Mise à jour des entitées.")
        for i in range(len(res.entités)):
            res.entités[i]._MiseÀJourIA()
        print("Entitées mises à jours.")
        res.cartes[0].dessiner()