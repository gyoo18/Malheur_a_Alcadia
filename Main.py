from GestionnaireRessources import Ressources
from Jeu import Jeu, ÉtatJeu
from random import randrange

import tkinter


def Constructeur():
    res = Ressources.avoirRessources()  # Initialiser le gestionnaire de ressources
    carte = res.chargerCarte("Intro")   # Charger la première carte

    jeu = Jeu.avoirJeu()        # Initialiser le jeu
    jeu.état.v = ÉtatJeu.MENU   # Démarrer avec le menu principal
    # Initialiser OpenGL
    jeu.peintre.pack()
    jeu.tkracine.update_idletasks()
    jeu.tkracine.update()
    jeu.peintre.pack_forget()
    jeu.tkracine.update_idletasks()
    jeu.tkracine.update()

    jeu.changerCarte(carte) # Assigner la carte au jeu

def Boucle():
    jeu = Jeu.avoirJeu()
    # Boucle principale
    while jeu.état.v != ÉtatJeu.TERMINÉ:
        jeu.miseÀJour()

def Destructeur():
    Ressources.avoirRessources().détruire()
    pass

def main():
    Constructeur()
    Boucle()
    Destructeur()

if __name__ == "__main__":
    main()