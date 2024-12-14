#premier test de UI
import os
import time
from Carte.Carte import Carte
from Carte.Tuile import Tuile
from GestionnaireRessources import Ressources
from Jeu import *
import dialogue
from TFX import *
from Entités.Golem import *
from tkinter import Frame,Button,Label,Text
from GUI.TkFenetre import TkFenetre
from GUI.Texte import Texte

def initialiserMenus(tkracine : tkinter.Tk):
    res = Ressources.avoirRessources()
    
    menu_principal = TkFenetre(Frame(tkracine))
    jeu_principal = TkFenetre(Frame(tkracine))
    menu_aide = TkFenetre(Frame(tkracine))
    menu_info = TkFenetre(Frame(tkracine))
    menu_combat = TkFenetre(Frame(tkracine))
    menu_select = TkFenetre(Frame(tkracine))

    res.enregistrerMenu(menu_principal,"menu_principal")
    res.enregistrerMenu(jeu_principal,"jeu_principal")
    res.enregistrerMenu(menu_aide,"menu_aide")
    res.enregistrerMenu(menu_info,"menu_info")
    res.enregistrerMenu(menu_combat,"menu_combat")
    res.enregistrerMenu(menu_select,"menu_select")

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
    res = Ressources.avoirRessources()
    jeu = Jeu.avoirJeu()
    carte = jeu.carte
    séquence : Séquence = None
    if carte.estScène:
        séquence = carte.séquences
    else:
        séquence = carte.séquences[jeu.état.v]
    plan = séquence.plans[jeu.état.scène_étape]

    fenetre = res.obtenirMenu("jeu_principal")
    
    if not fenetre.initialisé:
        jeu.peintre.pack_forget()

        titre = Label(fenetre.frame,text=plan.titres[jeu.état.scène_animation_étape])
        titre.pack(pady=10)

        jeu.peintre.pack(in_=fenetre.frame,pady=10)
        jeu.peintre.estVisible = True

        dialogue = Label(fenetre.frame,text="Dialogue")
        dialogue.pack(pady=10)
        fenetre.enregistrerWidget(dialogue,"dialogue")

        grille_boutons = Frame(fenetre.frame)
        grille_boutons.pack(pady=10)
        fenetre.enregistrerWidget(grille_boutons,"grille_boutons")

        jeu.frame_actuelle.pack_forget()
        fenetre.frame.pack()
        jeu.frame_actuelle = fenetre
        fenetre.initialisé = True
    elif jeu.frame_actuelle != fenetre:
        jeu.peintre.pack_forget()
        jeu.peintre.pack(in_=fenetre.frame,pady=10)
        jeu.peintre.estVisible = True

        jeu.frame_actuelle.pack_forget()
        fenetre.frame.pack()
        jeu.frame_actuelle = fenetre.frame

    dialogue = fenetre.obtenirWidget("dialogue")
    if jeu.état.v == ÉtatJeu.JEU and time.time()-jeu.dialogue_jeu_temps_début >= 3.0:
        dialogue["text"] = random.choice(séquence.plans).dialogues[jeu.état.scène_animation_étape]
        dialogue["text"] += "Tapez « ? » ou « aide » pour obtenir la liste des commandes.\n"
        jeu.dialogue_jeu_temps_début = time.time()
    elif jeu.état.v != ÉtatJeu.JEU:
        dialogue["text"] = plan.dialogues[jeu.état.scène_animation_étape]

    grille_boutons = fenetre.obtenirWidget("grille_boutons")
    
    # construire les bouttons
    if jeu.état.v == ÉtatJeu.SCÈNE:
        if plan.estAnimation and jeu.état.scène_animation_étape < len(plan.titres)-1:
            jeu.état.scène_animation_étape += 1
            time.sleep(plan.temps[jeu.état.scène_animation_étape-1])    # TODO trouver un moyen de ne pas bloquer le jeu
        elif not plan.estAnimation and jeu.état.scène_étape < len(séquence.plans)-1:
            if fenetre.état != 0:
                for w in grille_boutons.winfo_children():
                    w.destroy()
                def commande(jeu : Jeu):
                    jeu.état.scène_étape+=1

                bouton_continuer = Button(grille_boutons,text="Continuer",command=lambda: commande(jeu))
                bouton_continuer.pack(pady=10)
                fenetre.état = 0
        else:
            if fenetre.état != 1:
                for w in grille_boutons.winfo_children():
                    w.destroy()
                def commande(jeu : Jeu):
                    jeu.état.scène_étape = 0
                    jeu.état.scène_animation_étape = 0
                    jeu.état.v = ÉtatJeu.TRANSITION
                bouton_continuer = Button(grille_boutons,text="Continuer",command=lambda: commande(jeu))
                bouton_continuer.pack(pady=10)
                fenetre.état = 1
    elif jeu.état.v != ÉtatJeu.JEU and plan.estAnimation and jeu.état.scène_animation_étape < len(plan.titres)-1:
        jeu.état.scène_animation_étape += 1
        time.sleep(plan.temps[jeu.état.scène_animation_étape-1]) # TODO trouver un moyen de ne pas bloquer le jeu
    elif jeu.état.v == ÉtatJeu.DÉBUT:
        if carte.estScène:
            pass    # TODO Implémenter cette ligne
        else:
            if jeu.état.scène_étape == len(séquence.plans)-1:
                if fenetre.état != 2:
                    for w in grille_boutons.winfo_children():
                        w.destroy()
                    def commande(jeu:Jeu):
                        jeu.état.v = ÉtatJeu.JEU
                        jeu.état.scène_étape = 0
                        jeu.état.scène_animation_étape = 0
            
                        décalage = 0
                        for i in range(len(carte.entités)):
                            if type(carte.entités[i]) != Joueur:
                                carte.entités[i].pos = carte.entités_préchargement[i + décalage][1].copie()
                            else:
                                carte.entités[i].pos = carte.joueur_pos_init
                                décalage = -1
                    bouton_continuer = Button(grille_boutons,text="Continuer",command=lambda: commande(jeu))
                    bouton_continuer.pack(pady=10)
                    fenetre.état = 2
            else:
                if fenetre.état != 3:
                    for w in grille_boutons.winfo_children():
                        w.destroy()
                    def commande(jeu:Jeu):
                        jeu.état.scène_étape += 1
                    bouton_continuer = Button(grille_boutons,text="Continuer",command=lambda: commande(jeu))
                    bouton_continuer.pack(pady=10)
                    fenetre.état = 3
    elif jeu.état.v == ÉtatJeu.JEU:
        if fenetre.état != 4:
            for w in grille_boutons.winfo_children():
                w.destroy()
            def fin_tour(jeu:Jeu):
                jeu.état.v=ÉtatJeu.FIN_TOUR
            boutton_fin_tour = Button(grille_boutons,text="Terminer le tour",command=lambda: fin_tour(jeu))
            boutton_fin_tour.pack(pady=10)

            # TODO implémenter les contrôles pour le menu info

            # TODO implémenter les contrôles pour le menu select

            boutton_combat = Button(grille_boutons,text="Combat",command=lambda: commande_menu_combat(jeu.état.v))
            boutton_combat.pack(pady=10)

            boutton_aide = Button(grille_boutons,text="Aide",command=lambda: commande_menu_aide(jeu.état.v))
            boutton_aide.pack(pady=10)

            def commande_réussir(jeu:Jeu):
                for e in jeu.carte.entités:
                    if e.camp == Entité.CAMP_PAYSANS or e.camp == Entité.CAMP_PERSONNAGES:
                        e.estVivant = False
                jeu.état.v = ÉtatJeu.FIN_TOUR
            boutton_aide = Button(grille_boutons,text="Réussir",command=lambda: commande_réussir(jeu))
            boutton_aide.pack(pady=10)

            fenetre.état = 4
    elif jeu.état.v == ÉtatJeu.SUCCÈS:
        if carte.estScène:
            pass
        else:
            if jeu.état.scène_étape == len(séquence.plans)-1:
                if fenetre.état != 5:
                    for w in grille_boutons.winfo_children():
                        w.destroy()
                    def commande(jeu):
                        jeu.état.v = ÉtatJeu.TRANSITION
                        jeu.état.scène_étape = 0
                        jeu.état.scène_animation_étape = 0
                    bouton_continuer = Button(grille_boutons,text="Continuer",command=lambda: commande(jeu))
                    bouton_continuer.pack(pady=10)
                    fenetre.état = 5
            else:
                if fenetre.état != 6:
                    for w in grille_boutons.winfo_children():
                        w.destroy()
                    def commande(jeu):
                        jeu.état.scène_étape += 1
                    bouton_continuer = Button(grille_boutons,text="Continuer",command=lambda: commande(jeu))
                    bouton_continuer.pack(pady=10)
                    fenetre.état = 6
    elif jeu.état.v == ÉtatJeu.ÉCHEC:
        if carte.estScène:
            pass
        else:
            if jeu.état.scène_étape == len(séquence.plans)-1:
                if fenetre.état != 7:
                    for w in grille_boutons.winfo_children():
                        w.destroy()
                    def commande(jeu):
                        jeu.état.v = ÉtatJeu.TERMINÉ
                        jeu.état.scène_étape = 0
                        jeu.état.scène_animation_étape = 0
                    bouton_continuer = Button(grille_boutons,text="Continuer",command=lambda: commande(jeu))
                    bouton_continuer.pack(pady=10)
                    fenetre.état = 7
            else:
                if fenetre.état != 8:
                    for w in grille_boutons.winfo_children():
                        w.destroy()
                    def commande(jeu):
                        jeu.état.scène_étape += 1
                    bouton_continuer = Button(grille_boutons,text="Continuer",command=lambda: commande(jeu))
                    bouton_continuer.pack(pady=10)
                    fenetre.état = 8
    else:
        print(coul(gras("[inGameUI] L'état du jeu n'est pas reconnus."),ROUGE))

def displayUI():
    res = Ressources.avoirRessources()
    jeu = Jeu.avoirJeu()

    fenetre = res.obtenirMenu("menu_principal")

    if not fenetre.initialisé:
        titre = Label(fenetre.frame,text="Malheu à Alcadia!")
        titre.pack(pady=10)


        def bouton_commencer(jeu:Jeu):
            if jeu.carte.estScène:
                jeu.état.v = ÉtatJeu.SCÈNE
            else:
                jeu.état.v = ÉtatJeu.DÉBUT
        commencer = Button(fenetre.frame,text="Commencer",command=lambda: bouton_commencer(jeu))
        commencer.pack(pady=10)

        def bouton_Quitter(jeu : Jeu):
            jeu.état.v = ÉtatJeu.TERMINÉ
        quitter = Button(fenetre.frame,text="Quitter",command=lambda: bouton_Quitter(jeu))
        quitter.pack(pady=10)

        fenetre.frame.pack()
        jeu.frame_actuelle = fenetre.frame
        fenetre.initialisé = True

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

                if e.camp == Entité.CAMP_PAYSANS:
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

    fenetre = res.obtenirMenu("menu_aide")
    jeu.peintre.estVisible = False

    if not fenetre.initialisé:
        titre = Label(fenetre.frame,text="Menu d'aide")
        titre.pack(pady=10)

        aide = Texte(fenetre.frame)

        aide.markdownFormattage("\n"+
             "Tapez « **C** » ou « **Combat** » pour voir les informations relatives au unitées et au combat\n\n"+
             "Tapez « **I** » ou « **Info** », suivit de **<NomUnité>** pour voir les information relatives à une unité.\n\n"+
             "Tapez « **S** » ou « **Select** » suivit de **<NomUnité>** pour sélectionner une unité et lui donner un ordre\n\n"+
             "\n"+
             "__En mode Select__ *(ces commandes ne sont disponibles que lorsque vous avez sélectionné une unité)* :\n\n"+
             "\n"+
             "    - Tapez « **DP** » ou « **Déplacement** » suivit de **<X>** et **<Y>** pour déplacer le golem vers une destination\n"+
             "\n"+
             "    - Golems :\n"+
             "    - Tapez « **A** »  ou « **Attaque** » suivit de **<NomCible>** pour déplacer le golem vers une cible et l'attaquer\n"+
             "    - Tapez « **AS** » ou « **Attaque-Spéciale** » pour activer l'attaque spéciale du golem\n"+
             "    - Tapez « **DF** » ou « **Défense** » pour activer le mode défense du golem\n"+
             "    - Tapez « **L** »  ou « **Libérer** » pour libérer le golem des ordres qui lui ont été donnés\n"+
             "    - Tapez « **CA** » ou « **Charger-Attaque** » pour commencer à charger pour une attaque plus puissante\n"+
             "    - Tapez « **AC** » ou « **Attaquer-Charge** », suivit de **<NomCible>** pour frapper un ennemi avec une attaque plus puissante\n"+
             "\n"+
             "    - Mélios :\n"+
             "    - Tapez « **CG** » ou « **Créer-Golem** », suivit de **<X>** et **<Y>** pour créer un golem à l'endroit spécifié.\n"
             "\n" +
             "Tapez « **?** » ou « **Aide** » pour afficher cette liste à tout moment\n\n"+
             "Tapez « **P** » ou « **Précédent** » pour revenir au menu précédent.\n\n"
             "Tapez « **Q** » ou « **Quitter** » pour quitter.\n\n"+
             "\n")
        aide.pack(anchor="center",expand=True,fill="both",pady=10)
        jeu.frame_actuelle.frame.pack_forget()
        fenetre.frame.pack(side="top",expand=True,fill="both")
        jeu.frame_actuelle = fenetre
        fenetre.initialisé = True

    # clearScreen()
    # print("="*50)
    # print("Menu d'aide".center(50))
    # print("="*50)
    # print(
    #     "\n"+
    #     "Tapez « "+gras("C")+" » ou « "+gras("Combat")+" » pour voir les informations relatives au unitées et au combat\n" +
    #     "Tapez « "+gras("I")+" » ou « "+gras("Info")+" », suivit de "+gras("<NomUnité>")+" pour voir les information relatives à une unité.\n"
    #     "Tapez « "+gras("S")+" » ou « "+gras("Select")+" » suivit de "+gras("<NomUnité>")+" pour sélectionner une unité et lui donner un ordre\n"+
    #     "\n"+
    #     gras(soul("En mode Select (ces commandes ne sont disponibles que lorsque vous avez sélectionné une unité) :\n"))+
    #     "\n"+
    #     "  Tapez « "+gras("DP")+" » ou « "+gras("Déplacement")+" » suivit de "+gras("<X>")+" et "+gras("<Y>")+" pour déplacer le golem vers une destination\n"+
    #     "\n"+
    #     "  "+soul("Golems :\n")+
    #     "  Tapez « "+gras("A")+" »  ou « "+gras("Attaque")+" » suivit de "+gras("<NomCible>")+" pour déplacer le golem vers une cible et l'attaquer\n"+
    #     "  Tapez « "+gras("AS")+" » ou « "+gras("Attaque-Spéciale")+" » pour activer l'attaque spéciale du golem\n"+
    #     "  Tapez « "+gras("DF")+" » ou « "+gras("Défense")+" » pour activer le mode défense du golem\n"+
    #     "  Tapez « "+gras("L")+" »  ou « "+gras("Libérer")+" » pour libérer le golem des ordres qui lui ont été donnés\n"+
    #     "  Tapez « "+gras("CA")+" » ou « "+gras("Charger-Attaque")+" » pour commencer à charger pour une attaque plus puissante\n"+
    #     "  Tapez « "+gras("AC")+" » ou « "+gras("Attaquer-Charge")+" », suivit de "+gras("<NomCible>")+" pour frapper un ennemi avec une attaque plus puissante\n"+
    #     "\n"+
    #     "  "+soul("Mélios :\n")+
    #     "  Tapez « "+gras("CG")+" » ou « "+gras("Créer-Golem")+" », suivit de "+gras("<X>")+" et "+gras("<Y>")+" pour créer un golem à l'endroit spécifié.\n"
    #     "\n" +
    #     "Tapez « "+gras("?")+" » ou « "+gras("Aide")+" » pour afficher cette liste à tout moment\n"+
    #     "Tapez « "+gras("P")+" » ou « "+gras("Précédent")+" » pour revenir au menu précédent.\n"
    #     "Tapez « "+gras("Q")+" » ou « "+gras("Quitter")+" » pour quitter.\n"+
    #     "\n"
    #     )
    # print("="*50)
    #  
    # while True:
    #     commande = input("> ").upper().split(' ')
    #     if commande[0] == 'C' or commande[0] == "COMBAT":
    #         if commande_menu_combat(MenuContextuel.AIDE,commande):
    #             break
    #     elif commande[0] == 'S' or commande[0] == "SELECT":
    #         if commande_menu_select(MenuContextuel.AIDE,commande):
    #             break
    #     elif commande[0] == 'I' or commande[0] == "INFO":
    #         if commande_menu_info(MenuContextuel.AIDE,commande):
    #             break
    #     elif commande[0] == 'Q' or commande[0] == "QUITTER":
    #         commande_quitter()
    #         break
    #     if commande[0] == 'P' or commande[0] == "PRÉCÉDENT":
    #         commande_précédent()
    #         break
    #     else:
    #         print(coul("Veuillez entrer une commande valide.",ROUGE))
    #         time.sleep(1.5)
    #         effaceCommande()

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
                print(gras(e.nomAffichage) + " > PV : " + str(int(e.PV)))
    
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
    print(("Donnez un ordre à " + jeu.menu.menu_select_entité.nomAffichage).center(50))
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
                print("Veuillez préciser deux entiers positifs décrivant la destination de " + jeu.menu.menu_select_entité.nomAffichage)
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
        
        elif commande[0] == 'C' or commande[0] == "COMBAT":
            commande_menu_combat(MenuContextuel.SELECT,commande)
            break
        
        elif commande[0] == 'S' or commande[0] == "SELECT":
            if commande_menu_select(MenuContextuel.SELECT,commande):
                break
        
        elif commande[0] == 'I' or commande[0] == "INFO":
            if commande_menu_info(MenuContextuel.SELECT,commande):
                break
        
        elif commande[0] == '?' or commande[0] == "AIDE":
            commande_menu_aide(MenuContextuel.SELECT,commande)
            break

        elif commande[0] == 'P' or commande[0] == "PRÉCÉDENT":
            commande_précédent()
            break
        
        elif commande[0] == 'Q' or commande[0] == "QUITTER":
            commande_quitter()
            break
        
        else:
            print(coul("Veuillez entrer une commande valide.",ROUGE))
            time.sleep(1.5)
            effaceCommande()

def scène():
    # jeu = Jeu.avoirJeu()
    # carte = jeu.carte
    # 
    # match carte.séquence.v:
    #     case _:
    #         raise ValueError("Élément de séquence : " + carte.séquence.v +)
    pass

def main():
    width, eight = 20, 10

    game_map = [["." for _ in range(width)] for _ in range(eight)]

    while True:
        displayUI(game_map)
        break

if __name__ == "__main__":
    main()# exemple de premiere page comme menu
