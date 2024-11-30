#premier test de UI
import os
import time
from Carte.class_carte import Carte
from Ressources import Ressources

def clearScreen():
    os.system("cls" if os.name == 'nt' else "clear")
    pass
def ingameUI(game_map : Carte):
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
    print(controls)
    print(footer_end)

def displayUI(game_map):
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

    while True:
        key = input("Que voulez-vous faire? ").strip().lower()
        if key == "s":
            ingameUI(game_map)  # Pass the game map to the in-game UI
        elif key == "t":
            print("W (haut), S (bas), A (gauche), D (droite)")
            time.sleep(2)
        elif key == "q":
            print("Goodbye!")
            time.sleep(1)
            break
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
