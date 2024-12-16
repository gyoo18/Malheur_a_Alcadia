from GestionnaireRessources import Ressources
from Jeu import Jeu, ÉtatJeu
from random import randrange

import tkinter

jeu : Jeu = None

def Constructeur():
    res = Ressources.avoirRessources()
    carte = res.chargerCarte("Intro")

    global jeu
    jeu = Jeu.avoirJeu()
    jeu.état.v = ÉtatJeu.MENU
    jeu.peintre.pack()
    jeu.tkracine.update_idletasks()
    jeu.tkracine.update()
    jeu.peintre.pack_forget()
    jeu.tkracine.update_idletasks()
    jeu.tkracine.update()
    jeu.changerCarte(carte)

def Boucle():
    global jeu
    jeu.miseÀJour()
    return jeu.état.v != ÉtatJeu.TERMINÉ

def Destructeur():
    Ressources.avoirRessources().détruire()
    pass

def main():
    Constructeur()

    continuer = True
    while continuer:
        continuer = Boucle()
    
    Destructeur()

if __name__ == "__main__":
    main()