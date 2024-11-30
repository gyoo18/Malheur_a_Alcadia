#premier test de UI
import os
import time
from Carte.class_carte import Carte
from Ressources import Ressources
from Jeu import *
import message

def clearScreen():
    os.system("cls" if os.name == 'nt' else "clear")
    pass
def ingameUI(game_map : Carte, jeu : Jeu):
    """Display the in-game UI."""
    clearScreen()

    res = Ressources.avoirRessources()
    print("Mise à jour des entitées.")
    for i in range(len(res.cartes[0].entités)):
        res.cartes[0].entités[i]._MiseÀJourIA()
    print("Entitées mises à jours.")

    # Header
    header = "=" * 50
    header2 = "Insérez Titre".center(50)
    header3 = "=" * 50

    print(header)
    print(header2)
    print(header3)

    # Display game map
    print(game_map.dessiner())
    
    # Footer
    footer = "=" * 50
    controls = "Y va avoir le dialogue ici".center(50)
    footer_end = "=" * 50

    print(footer)
    #print(controls)
    match jeu.état.v:
        case ÉtatJeu.INTRODUCTION:
            message.script("Introduction",None,None)
        case ÉtatJeu.ZONE1:
            message.script("Prairie","Debut",jeu)
        case ÉtatJeu.ZONE2:
            message.script("Cite","Debut",jeu)
        case ÉtatJeu.ZONE3:
            message.script("Chateau","Debut",jeu)
    print(footer_end)
    g = input("Tapez G : ").capitalize() == "G"
    match jeu.état.v:
        case ÉtatJeu.INTRODUCTION:
            jeu.état.v = ÉtatJeu.ZONE1
        case ÉtatJeu.ZONE1:
            if g:
                message.script("Prairie","Success",jeu)
            else:
                message.script("Prairie","Failure",jeu)
            if jeu.état.v != ÉtatJeu.TERMINÉ:
                jeu.état.v = ÉtatJeu.ZONE2
        case ÉtatJeu.ZONE2:
            if g:
                message.script("Cite","Success",jeu)
            else:
                message.script("Cite","Failure",jeu)
            if jeu.état.v != ÉtatJeu.TERMINÉ:
                jeu.état.v = ÉtatJeu.ZONE3
        case ÉtatJeu.ZONE3:
            if g:
                message.script("Chateau","Success",jeu)
            else:
                message.script("Chateau","Failure",jeu)
            if jeu.état.v != ÉtatJeu.TERMINÉ:
                jeu.état.v = ÉtatJeu.TERMINÉ

    res = Ressources.avoirRessources()
    print("Mise à jour des entitées.")
    for i in range(len(res.entités)):
        res.entités[i]._MiseÀJourIA()
    print("Entitées mises à jours.")
    res.cartes[0].dessiner()

def displayUI(game_map, jeu : Jeu):
    clearScreen()

    header = "=" * 50
    header2 = "inserez titre".center(50)
    header3 = "=" * 50

    print(header)
    print(header2)
    print(header3)

    menu = "menu".center(50)
    inputs = "S = commencer, T = tutoriel, Q = quitter".center(50)

    print(menu)
    print(inputs)


    footer = "=" * 50
    print(footer)

    # while True:
    key = input("Que voulez-vous faire? ").strip().lower()
    if key == "s":
        # ingameUI(game_map)  # Pass the game map to the in-game UI
        jeu.état.v = ÉtatJeu.INTRODUCTION
    elif key == "t":
        print("W (haut), S (bas), A (gauche), D (droite)")
        time.sleep(2)
    elif key == "q":
        print("Goodbye!")
        time.sleep(1)
        jeu.état.v = ÉtatJeu.TERMINÉ
        # break
    else:
        print("Choix invalide, veuillez choisir une option : S, T ou Q")
        time.sleep(1)


def main():
    width, eight = 20, 10

    game_map = [["." for _ in range(width)] for _ in range(eight)]

    while True:
        displayUI(game_map)
        break

if __name__ == "__main__":
    main()# exemple de premiere page comme menu
