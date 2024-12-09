#premier test de UI
import os
import time
from Carte.Carte import Carte
from Carte.Tuile import Tuile
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
            header2 = gras("Malheur à Alcadia!") # TODO #21 Envoyer les titres dans dialogue
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
    print(game_map.dessiner().center(50))
    
    # Footer
    footer = "=" * 50
    controls = ""
    #print(controls)
    if jeu.état.v == ÉtatJeu.JEU:
        controls = "Tapez « ? » ou « aide » pour obtenir les contrôles ou entré pour terminer votre tour"
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
        while True:
            commande = input("> ").upper().split(" ")
            
            if commande[0] == '':
                jeu.état.v = ÉtatJeu.FIN_TOUR
                break
            elif commande[0] == 'I' or commande[0] == "INFO":
                if commande_menu_info(jeu.état.v,commande):
                    break
            elif commande[0] == 'S' or commande[0] == "SELECT":
                if commande_menu_select(jeu.état.v,commande):
                    break
            elif commande[0] == 'C' or commande[0] == "COMBAT":
                commande_menu_combat(jeu.état.v)
                break
            elif commande[0] == '?' or commande[0] == "AIDE":
                commande_menu_aide(jeu.état.v)
                break
            else:
                print(coul("Veuillez entrer une commande valide ou taper")+TFX("entré",gras=True,Pcoul=ROUGE)+coul(" pour finir le tour.",ROUGE))
                time.sleep(1.5)
                effaceCommande()
    else:
        input("")

def displayUI():
    jeu = Jeu.avoirJeu()

    clearScreen()

    header = "=" * 50
    header2 = gras("Malheur à Alcadia!").center(50)
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


def commande_menu_aide(historique):
    jeu = Jeu.avoirJeu()
    jeu.menu.menu_historique.append(historique)
    jeu.état.v = ÉtatJeu.MENU_CONTEXTUEL
    jeu.menu.v = MenuContextuel.AIDE

def commande_menu_combat(historique):
    jeu = Jeu.avoirJeu()
    jeu.menu.menu_historique.append(historique)
    jeu.état.v = ÉtatJeu.MENU_CONTEXTUEL
    jeu.menu.v = MenuContextuel.COMBAT

def commande_menu_select(historique, commande : list[str]):
    jeu = Jeu.avoirJeu()
    if len(commande) > 1:
        nom = commande[1]
        for e in jeu.carte.entités:
            if e.nom.upper() == nom:

                if e.camp == "Paysans":
                    print(coul("Vous ne pouvez pas donner d'ordres aux paysans.",ROUGE))
                    time.sleep(1.5)
                    effaceCommande()
                    return False

                for i in range(len(jeu.menu.menu_historique)):
                    if jeu.menu.menu_historique[i] == MenuContextuel.SELECT:
                        jeu.menu.menu_historique.pop(i)
                        break

                jeu.menu.menu_historique.append(historique)
                jeu.état.v = ÉtatJeu.MENU_CONTEXTUEL
                jeu.menu.v = MenuContextuel.SELECT
                jeu.menu.menu_select_entité = e
                return True
    print(coul("Veuillez entrer un nom qui se trouve dans la liste.",ROUGE))
    time.sleep(1.5)
    effaceCommande()
    return False

def commande_menu_info(historique, commande : list[str]):
    jeu = Jeu.avoirJeu()
    if len(commande) > 1:
        nom = commande[1]
        for e in jeu.carte.entités:
            if e.nom.upper() == nom:
                jeu.menu.menu_historique.append(historique)
                jeu.menu.v = MenuContextuel.INFO
                jeu.menu.menu_entité_entité = e
                return True
    print(coul("Veuillez entrer un nom qui se trouve dans la liste.",ROUGE))
    time.sleep(1.5)
    effaceCommande()
    return False

def commande_quitter():
    jeu = Jeu.avoirJeu()
    jeu.état.v = jeu.menu.menu_historique[0]
    jeu.menu.menu_historique.clear()

def commande_précédent():
    jeu = Jeu.avoirJeu()
    if len(jeu.menu.menu_historique) > 1:
        jeu.menu.v = jeu.menu.menu_historique.pop(-1)
    elif len(jeu.menu.menu_historique) > 0:
        jeu.état.v = jeu.menu.menu_historique.pop(-1)

def menu_aide():
    res = Ressources.avoirRessources()
    jeu = Jeu.avoirJeu()

    clearScreen()
    print("="*50)
    print("Menu d'aide".center(50))
    print("="*50)
    print(
        "\n"+
        "Tapez « "+gras("C")+" » ou « "+gras("Combat")+" » pour voir les informations relatives au unitées et au combat\n" +
        "Tapez « "+gras("I")+" » ou « "+gras("Info")+" », suivit de "+gras("<NomUnité>")+" pour voir les information relatives à une unité.\n"
        "Tapez « "+gras("S")+" » ou « "+gras("Select")+" » suivit de "+gras("<NomUnité>")+" pour sélectionner une unité et lui donner un ordre\n"+
        "\n"+
        gras(soul("En mode Select (ces commandes ne sont disponibles que lorsque vous avez sélectionné une unité) :\n"))+
        "\n"+
        "  Tapez « "+gras("DP")+" » ou « "+gras("Déplacement")+" » suivit de "+gras("<X>")+" et "+gras("<Y>")+" pour déplacer le golem vers une destination\n"+
        "\n"+
        "  "+soul("Golems :\n")+
        "  Tapez « "+gras("A")+" »  ou « "+gras("Attaque")+" » suivit de "+gras("<NomCible>")+" pour déplacer le golem vers une cible et l'attaquer\n"+
        "  Tapez « "+gras("AS")+" » ou « "+gras("Attaque-Spéciale")+" » pour activer l'attaque spéciale du golem\n"+
        "  Tapez « "+gras("DF")+" » ou « "+gras("Défense")+" » pour activer le mode défense du golem\n"+
        "  Tapez « "+gras("L")+" »  ou « "+gras("Libérer")+" » pour libérer le golem des ordres qui lui ont été donnés\n"+
        "  Tapez « "+gras("CA")+" » ou « "+gras("Charger-Attaque")+" » pour commencer à charger pour une attaque plus puissante\n"+
        "  Tapez « "+gras("AC")+" » ou « "+gras("Attaquer-Charge")+" », suivit de "+gras("<NomCible>")+" pour frapper un ennemi avec une attaque plus puissante\n"+
        "\n"+
        "  "+soul("Mélios :\n")+
        "  Tapez « "+gras("CG")+" » ou « "+gras("Créer-Golem")+" », suivit de "+gras("<X>")+" et "+gras("<Y>")+" pour créer un golem à l'endroit spécifié.\n"
        "\n" +
        "Tapez « "+gras("?")+" » ou « "+gras("Aide")+" » pour afficher cette liste à tout moment\n"+
        "Tapez « "+gras("P")+" » ou « "+gras("Précédent")+" » pour revenir au menu précédent.\n"
        "Tapez « "+gras("Q")+" » ou « "+gras("Quitter")+" » pour quitter.\n"+
        "\n"
        )
    print("="*50)
    
    while True:
        commande = input("> ").upper().split(' ')
        if commande[0] == 'C' or commande[0] == "COMBAT":
            if commande_menu_combat(MenuContextuel.AIDE,commande):
                break
        elif commande[0] == 'S' or commande[0] == "SELECT":
            if commande_menu_select(MenuContextuel.AIDE,commande):
                break
        elif commande[0] == 'I' or commande[0] == "INFO":
            if commande_menu_info(MenuContextuel.AIDE,commande):
                break
        elif commande[0] == 'Q' or commande[0] == "QUITTER":
            commande_quitter()
            break
        if commande[0] == 'P' or commande[0] == "PRÉCÉDENT":
            commande_précédent()
            break
        else:
            print(coul("Veuillez entrer une commande valide.",ROUGE))
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
                print(gras(e.nom) + " > PV : " + str(int(e.PV)))
    
    print("="*50)
    
    while True:
        commande = input("> ").upper().split(' ')
        if commande[0] == 'I' or commande[0] == "INFO":
            if commande_menu_info(MenuContextuel.COMBAT,commande):
                break
        elif commande[0] == 'S' or commande[0] == "SELECT":
            if commande_menu_select(MenuContextuel.COMBAT,commande):
                break
        elif commande[0] == '?' or commande[0] == "AIDE":
            commande_menu_aide(MenuContextuel.COMBAT)
            break
        elif commande[0] == 'Q' or commande[0] == "QUITTER":
            commande_quitter()
            break
        elif commande[0] == 'P' or commande[0] == "PRÉCÉDENT":
            commande_précédent()
            break
        else:
            print(coul("Veuillez entrer une commande valide.",ROUGE))
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
           if commande_menu_select(MenuContextuel.INFO,commande):
               break
        elif commande[0] == 'C' or commande[0] == "COMBAT":
           if commande_menu_combat(MenuContextuel.INFO,commande):
               break
        elif commande[0] == '?' or commande[0] == "AIDE":
            commande_menu_aide(MenuContextuel.INFO)
            break
        elif commande[0] == 'Q' or commande[0] == "QUITTER":
            commande_quitter()
            break
        elif commande[0] == 'P' or commande[0] == "PRÉCÉDENT":
            commande_précédent()
            break
        else:
            print(coul("Veuillez entrer une commande valide.",ROUGE))
            time.sleep(1.5)
            effaceCommande()

def menu_select():
    jeu = Jeu.avoirJeu()

    print("="*50)
    print(("Donnez un ordre à " + jeu.menu.menu_select_entité.nom).center(50))
    print("="*50)

    print(jeu.carte.dessiner().center(50))

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

        elif commande[0] == 'CG' or commande[0] == "CRÉER-GOLEM":
            if len(commande) < 3:
                print("La commande Créer-Golem nécessite les arguements X et Y.")
                time.sleep(1.5)
                effaceCommande()
                continue
            try:
                x = int(commande[1])
                y = int(commande[2])
            except:
                print("Veuillez préciser deux entiers positifs décrivant la l'emplacement de la création du Golem.")
                time.sleep(1.5)
                effaceCommande()
                continue
            
            if x < 0 or x > jeu.carte.colonnes or y < 0 or y > jeu.carte.lignes:
                print("Veuillez entrer des nombres entre 0 et " + str(int(jeu.carte.colonnes)) + " pour les X et entre 0 et " + str(int(jeu.carte.lignes)) + " pour les Y.")
                time.sleep(1.5)
                effaceCommande()
                continue

            if jeu.carte.matrice[x][y].type == Tuile.TYPE_MUR:
                print(coul("Impossible de placer un golem à " + str(x) + ',' + str(y) + ", il y a un mur dans le chemin!",ROUGE))
                time.sleep(1.5)
                effaceCommande()
                continue


            objetCommande = Commande()
            objetCommande.faireCommandeCréerGolem(Vec2(x,y))
            jeu.menu.menu_select_entité.commande(objetCommande)

        elif commande[0] == 'P' or commande[0] == "PRÉCÉDENT":
            commande_précédent()
            break

        elif commande[0] == '?' or commande[0] == "AIDE":
            commande_menu_aide(MenuContextuel.SELECT,commande)
            break
        
        elif commande[0] == 'Q' or commande[0] == "QUITTER":
            commande_quitter()
            break
        
        else:
            print(coul("Veuillez entrer une commande valide.",ROUGE))
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
