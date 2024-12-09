from Ressources import Ressources
from Carte.Carte import Carte
from Entités.Paysan import *
from Entités.Golem import *
from Entités.Personnages import *
from Jeu import Jeu, ÉtatJeu
from random import randrange

jeu : Jeu = None

def Constructeur():
    res = Ressources.avoirRessources()
    carte = res.chargerCarte("Chapitre3")

    global jeu
    jeu = Jeu.avoirJeu()
    jeu.état.v = ÉtatJeu.MENU
    jeu.changerCarte(carte)
    pass

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