# exemple de premiere page comme menu
import os
import time

def clearScreen():
    os.system("cls" if os.name == 'nt' else CLEAR)

def game():
    #inserez jeux avec map ici
    print("pas encore de jeux lol")
def displayUI(menu):
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
        key = input("que voulez vous faire? ")
        if key == "s" or key == "S":
            game()
        elif key == "t" or key == "T":
            print("w (up), s (down), a (right), d (left)")
        elif key == "q" or key == "Q":
            print("goodbye!")
            time.sleep(1)
            break
        else:
            print("choix invalide, svp choisire une option: S, T ou Q")
            time.sleep(1)

    return key


def main():
    width, eight = 20, 10

    menu = [["." for _ in range(width)] for _ in range(eight)]

    while True:
        displayUI(menu)
        break

if __name__ == "__main__":
    main()
