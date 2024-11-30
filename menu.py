#premier test de UI
import os
import time
from Carte.class_carte import Carte
from Ressources import Ressources
from Jeu import *
import dialogue

def clearScreen():
    # os.system("cls" if os.name == 'nt' else "clear")
    pass
def ingameUI(game_map : Carte, jeu : Jeu):
    """Display the in-game UI."""
    clearScreen()

    # Header
    header = "=" * 50
    header2 = ""
    match jeu.chapitre.v:
        case Chapitre.INTRODUCTION:
            header2 = "Titre du jeu"
        case Chapitre.CHAPITRE1:
            header2 = dialogue.titre(1)
        case Chapitre.CHAPITRE2:
            header2 = dialogue.titre(2)
        case Chapitre.CHAPITRE3:
            header2 = dialogue.titre(3)
        case _:
            raise ValueError("Le chapitre " + str(jeu.chapitre.v) + " n'est pas un chapitre valide.")
    header2 = header2.center(50)
    header3 = "=" * 50

    print(header)
    print(header2)
    print(header3)

    # Display game map
    print(game_map.dessiner())
    
    # Footer
    footer = "=" * 50
    controls = ""
    #print(controls)
    if jeu.état.v == ÉtatJeu.JEU:
        controls = "Y va avoir les contrôles ici"
    else :
        controls = dialogue.script(jeu.chapitre.v,jeu.état.v,jeu.choix,jeu)
    controls = controls.center(50)
    footer_end = "=" * 50

    print(footer)
    print(controls)
    print(footer_end)
    if jeu.état.v == ÉtatJeu.CHOIX:
        jeu.choix = input("Melios > ")
    elif jeu.état.v == ÉtatJeu.DÉBUT:
        jeu.état.v = ÉtatJeu.JEU
        input("")
    else:
        input("")

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
        jeu.état.v = ÉtatJeu.DÉBUT
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
