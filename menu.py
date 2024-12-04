#premier test de UI
import os
import time
from Carte.class_carte import Carte
from Ressources import Ressources
from Jeu import *
import dialogue
from TFX import *
from Entités.Golem import *

def clearScreen():
    # os.system("cls" if os.name == 'nt' else "clear")
    pass

def effaceCommande():
    """Efface la commande invalide et son message d'erreur précédent.

    Bouge le curseur d'une ligne vers le haut, efface, bouge le curseur d'une ligne vers le haut, efface de nouveau.
    """
    bgcr(Vec2(0,1)) # Efface bouge le curseur vers la ligne précédente
    print(EFL+'\r',end='')      # Efface la ligne et place le curseur au début
    bgcr(Vec2(0,1)) # Efface bouge le curseur vers la ligne précédente
    print(EFL+'\r',end='')      # Efface la ligne et place le curseur au début

def ingameUI():
    """Display the in-game UI."""
    jeu = Jeu.avoirJeu()
    game_map = jeu.carte

    clearScreen()

    # Header
    header = "=" * 50
    header2 = ""
    match jeu.chapitre.v:
        case Chapitre.INTRODUCTION:
            header2 = gras("Malheur à Alcadia!")
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
        controls = "Tapez « ? » ou « aide » pour obtenir les contrôles"
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
    elif jeu.état.v == ÉtatJeu.JEU:
        continuer = True
        while continuer:
            continuer = False
            commande = input("> ").upper().split(" ")
            
            if commande[0] == '':
                jeu.état.v = ÉtatJeu.FIN_TOUR
            elif commande[0] == 'S' or commande[0] == "SELECT":
                trouvé = False
                if len(commande) > 1:
                    nom = commande[1]
                    for e in jeu.carte.entités:
                        if e.nom.upper() == nom:
                            jeu.menu.menu_historique.append(jeu.état.v)
                            jeu.état.v = ÉtatJeu.MENU_CONTEXTUEL
                            jeu.menu.v = MenuContextuel.SELECT
                            jeu.menu.menu_select_entité = e
                            trouvé = True
                            break
                if not trouvé:
                    print("Veuillez entrer un nom qui se trouve dans la liste.")
                    time.sleep(1.5)
                    effaceCommande()
                else:
                    break
            elif commande[0] == 'C' or commande[0] == "COMBAT":
                jeu.menu.menu_historique.append(jeu.état.v)
                jeu.état.v = ÉtatJeu.MENU_CONTEXTUEL
                jeu.menu.v = MenuContextuel.COMBAT
            elif commande[0] == '?' or commande[0] == "AIDE":
                jeu.menu.menu_historique.append(jeu.état.v)
                jeu.état.v = ÉtatJeu.MENU_CONTEXTUEL
                jeu.menu.v = MenuContextuel.AIDE
            else:
                print("Veuillez entrer une commande valide ou taper entré pour finir le tour.")
                time.sleep(1.5)
                effaceCommande()
                continuer = True
    else:
        input("")

def displayUI():
    jeu = Jeu.avoirJeu()

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

def menu_contextuel():

    menu = Jeu.avoirJeu().menu

    match menu.v:
        case MenuContextuel.AIDE:
            menu_aide()
        case MenuContextuel.COMBAT:
            menu_combat()
        case MenuContextuel.INFO:
            menu_info()
        case MenuContextuel.SELECT:
            menu_select()
        case _:
            raise ValueError("Le menu : " + str(menu.v) + " n'est pas un menu reconnus.")


def menu_aide():
    res = Ressources.avoirRessources()
    jeu = Jeu.avoirJeu()

    clearScreen()
    print("="*50)
    print("Menu d'aide".center(50))
    print("="*50)
    print(
        "\n"+
        "Tapez « P » ou « Précédent » pour revenir au menu précédent.\n"
        "Tapez « Q » ou « Quitter » pour quitter.\n"+
        "\n"
        )
    print("="*50)
    
    while True:
        commande = input("> ").upper().split(' ')
        if commande[0] == 'Q' or commande[0] == "QUITTER":
            jeu.état.v = jeu.menu.menu_historique[0]
            jeu.menu.menu_historique.clear()
            break
        if commande[0] == 'P' or commande[0] == "PRÉCÉDENT":
            if len(jeu.menu.menu_historique) > 1:
                jeu.menu.v = jeu.menu.menu_historique.pop(-1)
                break
            elif len(jeu.menu.menu_historique) > 0:
                jeu.état.v = jeu.menu.menu_historique.pop(-1)
                break
        else:
            print("Veuillez entrer une commande valide.")
            time.sleep(1.5)
            effaceCommande()

def menu_combat():
    jeu = Jeu.avoirJeu()

    print("="*50)
    print("Menu de statistiques du combat".center(50))
    print("="*50)

    camps = []

    for e in jeu.carte.entités:
        if not e.camp in camps:
            camps.append(e.camp)
    
    for c in camps:
        print("\n" + soul(c) + " : \n")
        for e in jeu.carte.entités:
            if e.camp == c:
                print(gras(e.nom) + " > PV : " + str(int(e.vie)))
    
    print("="*50)
    
    while True:
        commande = input("> ").upper().split(' ')
        if commande[0] == 'I' or commande[0] == "INFO":
            trouvé = False
            if len(commande) > 1:
                nom = commande[1]
                for e in jeu.carte.entités:
                    if e.nom.upper() == nom:
                        jeu.menu.menu_historique.append(MenuContextuel.COMBAT)
                        jeu.menu.v = MenuContextuel.INFO
                        jeu.menu.menu_entité_entité = e
                        trouvé = True
                        break
            if not trouvé:
                print("Veuillez entrer un nom qui se trouve dans la liste.")
                time.sleep(1.5)
                effaceCommande()
            else:
                break
        elif commande[0] == 'S' or commande[0] == "SELECT":
            trouvé = False
            if len(commande) > 1:
                nom = commande[1]
                for e in jeu.carte.entités:
                    if e.nom.upper() == nom:
                        jeu.menu.menu_historique.append(MenuContextuel.COMBAT)
                        jeu.menu.v = MenuContextuel.SELECT
                        jeu.menu.menu_select_entité = e
                        trouvé = True
                        break
            if not trouvé:
                print("Veuillez entrer un nom qui se trouve dans la liste.")
                time.sleep(1.5)
                effaceCommande()
            else:
                break
        elif commande[0] == '?' or commande[0] == "AIDE":
            jeu.menu.menu_historique.append(MenuContextuel.COMBAT)
            jeu.menu.v = MenuContextuel.AIDE
            break
        elif commande[0] == 'Q' or commande[0] == "QUITTER":
            jeu.état.v = jeu.menu.menu_historique[0]
            jeu.menu.menu_historique.clear()
            break
        elif commande[0] == 'P' or commande[0] == "PRÉCÉDENT":
            if len(jeu.menu.menu_historique) > 1:
                jeu.menu.v = jeu.menu.menu_historique.pop(-1)
                break
            elif len(jeu.menu.menu_historique) > 0:
                jeu.état.v = jeu.menu.menu_historique.pop(-1)
                break
        else:
            print("Veuillez entrer une commande valide.")
            time.sleep(1.5)
            effaceCommande()

def menu_info():
    jeu = Jeu.avoirJeu()

    print("="*50)
    print("Menu de statistiques du combat".center(50))
    print("="*50)

    print(jeu.menu.menu_entité_entité.avoirInfoStr())
    
    print("="*50)

    while True:
        commande = input("> ").upper().split(' ')
        if commande[0] == 'S' or commande[0] == "SELECT":
            trouvé = False
            if len(commande) > 1:
                nom = commande[1]
                for e in jeu.carte.entités:
                    if e.nom.upper() == nom:
                        jeu.menu.menu_historique.append(MenuContextuel.INFO)
                        jeu.menu.v = MenuContextuel.SELECT
                        jeu.menu.menu_select_entité = e
                        trouvé = True
                        break
            if not trouvé:
                print("Veuillez entrer un nom qui se trouve dans la liste.")
                time.sleep(1.5)
                effaceCommande()
            else:
                break
        elif commande[0] == '?' or commande[0] == "AIDE":
            jeu.menu.menu_historique.append(MenuContextuel.INFO)
            jeu.menu.v = MenuContextuel.AIDE
        elif commande[0] == 'Q' or commande[0] == "QUITTER":
            jeu.état.v = jeu.menu.menu_historique[0]
            jeu.menu.menu_historique.clear()
            break
        elif commande[0] == 'P' or commande[0] == "PRÉCÉDENT":
            if len(jeu.menu.menu_historique) > 1:
                jeu.menu.v = jeu.menu.menu_historique.pop(-1)
                break
            elif len(jeu.menu.menu_historique) > 0:
                jeu.état.v = jeu.menu.menu_historique.pop(-1)
                break
        else:
            print("Veuillez entrer une commande valide.")
            time.sleep(1.5)
            effaceCommande()

def menu_select():
    jeu = Jeu.avoirJeu()

    print("="*50)
    print(("Donnez un ordre à " + jeu.menu.menu_select_entité.nom).center(50))
    print("="*50)

    print(jeu.carte.dessiner())

    print("="*50)
    print("Tapez « ? » ou « Aide » pour obtenir la liste des commandes.".center(50))
    print("="*50)

    while True:
        commande = input("> ").upper().split(' ')
        if commande[0] == "DP" or commande[0] == "DÉPLACEMENT":
            if len(commande) < 3:
                print("La commande Déplacement nécessite les arguements X et Y.")
                time.sleep(1.5)
                effaceCommande()
                continue
            try:
                x = int(commande[1])
                y = int(commande[2])
            except:
                print("Veuillez préciser deux entiers positifs décrivant la destination de " + jeu.menu.menu_select_entité.nom)
                time.sleep(1.5)
                effaceCommande()
                continue
            
            if x < 0 or x > jeu.carte.colonnes or y < 0 or y > jeu.carte.lignes:
                print("Veuillez entrer des nombres entre 0 et " + str(int(jeu.carte.colonnes)) + " pour les X et entre 0 et " + str(int(jeu.carte.lignes)) + " pour les Y.")
                time.sleep(1.5)
                effaceCommande()
                continue

            objetCommande = Commande()
            objetCommande.faireCommandeDéplacement(Vec2(x,y))
            jeu.menu.menu_select_entité.commande(objetCommande)
                
        elif commande[0] == "A" or commande[0] == "ATTAQUE":
            if len(commande) < 2:
                print("Veuillez préciser le nom de la cible à attaquer.")
                time.sleep(1.5)
                effaceCommande()
                continue

            nom = commande[1]
            entité = None
            for e in jeu.carte.entités:
                if e.nom.upper() == nom:
                    entité = e
            
            if entité == None:
                print("Veuillez utiliser le nom d'une entité sur le champ de bataille.")
                time.sleep(1.5)
                effaceCommande()
                continue

            objetCommande = Commande()
            objetCommande.faireCommandeAttaque(entité)
            jeu.menu.menu_select_entité.commande(objetCommande)

        elif commande[0] == "AS" or commande[0] == "ATTAQUE-SPÉCIALE":
            try:
                attaque = jeu.menu.menu_select_entité.ATTAQUE_SPÉCIALE
            except:
                print(jeu.menu.menu_select_entité.nom + " n'a pas d'attaque spéciale.")
                time.sleep(1.5)
                effaceCommande()
                continue
            
            objetCommande = Commande()
            objetCommande.faireCommandeAttaqueSpéciale(attaque)
            jeu.menu.menu_select_entité.commande(objetCommande)

        elif commande[0] == "DF" or commande[0] == "DÉFENSE":
            objetCommande = Commande()
            objetCommande.faireCommandeDéfense()
            jeu.menu.menu_select_entité.commande(objetCommande)
            
        elif commande[0] == "L" or commande[0] == "LIBÉRER":
            objetCommande = Commande()
            objetCommande.faireCommandeLibérer()
            jeu.menu.menu_select_entité.commande(objetCommande)

        elif commande[0] == "CA" or commande[0] == "CHARGER-ATTAQUE":
            objetCommande = Commande()
            objetCommande.faireCommandeCharger()
            jeu.menu.menu_select_entité.commande(objetCommande)

        elif commande[0] == "AC" or commande[0] == "ATTAQUER-CHARGE":
            if len(commande) < 2:
                print("Veuillez préciser le nom de la cible à attaquer.")
                time.sleep(1.5)
                effaceCommande()
                continue

            nom = commande[1]
            entité = None
            for e in jeu.carte.entités:
                if e.nom.upper() == nom:
                    entité = e
            
            if entité == None:
                print("Veuillez utiliser le nom d'une entité sur le champ de bataille.")
                time.sleep(1.5)
                effaceCommande()
                continue

            objetCommande = Commande()
            objetCommande.faireCommandeAttaquerCharge(entité)
            jeu.menu.menu_select_entité.commande(objetCommande)

        elif commande[0] == '?' or commande[0] == "AIDE":
            jeu.menu.menu_historique.append(MenuContextuel.SELECT)
            jeu.menu.v = MenuContextuel.AIDE
        elif commande[0] == 'Q' or commande[0] == "QUITTER":
            jeu.état.v = jeu.menu.menu_historique[0]
            jeu.menu.menu_historique.clear()
            break
        elif commande[0] == 'P' or commande[0] == "PRÉCÉDENT":
            if len(jeu.menu.menu_historique) > 1:
                jeu.menu.v = jeu.menu.menu_historique.pop(-1)
                break
            elif len(jeu.menu.menu_historique) > 0:
                jeu.état.v = jeu.menu.menu_historique.pop(-1)
                break
        else:
            print("Veuillez taper une commande valide.")
            time.sleep(1.5)
            effaceCommande()

def main():
    width, eight = 20, 10

    game_map = [["." for _ in range(width)] for _ in range(eight)]

    while True:
        displayUI(game_map)
        break

if __name__ == "__main__":
    main()# exemple de premiere page comme menu
