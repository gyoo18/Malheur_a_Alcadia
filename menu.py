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
from tkinter.ttk import Frame,Button,Label, Style
from tkinter.font import Font
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

def surModificationFenêtre(event):
    jeu = Jeu.avoirJeu()

    if jeu.vieille_taille != Vec2(jeu.tkracine.winfo_width(),jeu.tkracine.winfo_height()):
        style = Style(jeu.tkracine)
        taille_police = min(jeu.tkracine.winfo_width(),jeu.tkracine.winfo_height())//21
        style.configure("TLabel",font=("Noto Sans CJK KR Black",taille_police),foreground="#f2b635",background="#191a1e")
        style.configure("TFrame",background="#191a1e")
        style.configure("TButton",font = ("Noto Sans CJK KR Black",taille_police//2),foreground = "#f7deb7",background="#4e89e8",borderwidth=5)
        style.map("TButton",relief=[("disabled","raised"),("active","sunken")],background=[("disabled","#314775"),("active","#44618c")])
        style.configure("Boutons_Combat.TButton",font=("Noto Sans CJK KR Black",taille_police//3))
        style.configure("conteneur_entité.TFrame",borderwidth=5,relief="ridge")

        Texte.surModificationFenêtre(jeu.tkracine)

        jeu.vieille_taille = Vec2(jeu.tkracine.winfo_width(),jeu.tkracine.winfo_height())

def effaceCommande():
    """Efface la commande invalide et son message d'erreur précédent.

    Bouge le curseur d'une ligne vers le haut, efface, bouge le curseur d'une ligne vers le haut, efface de nouveau.
    """
    bgcr(Vec2(0,1)) # Efface bouge le curseur vers la ligne précédente
    print(EFL+'\r',end='')      # Efface la ligne et place le curseur au début
    bgcr(Vec2(0,1)) # Efface bouge le curseur vers la ligne précédente
    print(EFL+'\r',end='')      # Efface la ligne et place le curseur au début

def jeu():
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

        grille_boutons = Frame(fenetre.frame)
        grille_boutons.pack(pady=10,side="bottom",expand=False)
        fenetre.enregistrerWidget(grille_boutons,"grille_boutons")

        dialogue = Texte(fenetre.frame,background="#191a1e",foreground="#f7deb7",relief="flat",wrap="word",highlightthickness=0,height=5)
        dialogue.pack(padx=100,pady=10,side="bottom",fill="both",expand=False)
        fenetre.enregistrerWidget(dialogue,"dialogue")

        conteneur_peintre = Frame(fenetre.frame)
        conteneur_peintre.pack(fill="both",expand=True)
        fenetre.enregistrerWidget(conteneur_peintre,"conteneur_peintre")

        fenetre.initialisé = True
    if jeu.frame_actuelle != fenetre:
        conteneur_peintre = fenetre.obtenirWidget("conteneur_peintre")

        jeu.peintre.pack_forget()
        jeu.peintre.pack(in_=conteneur_peintre,fill="both",expand=True)
        jeu.peintre.estVisible = True

        jeu.frame_actuelle.frame.pack_forget()
        fenetre.frame.pack(fill="both",expand=True)
        jeu.frame_actuelle = fenetre

    dialogue = fenetre.obtenirWidget("dialogue")
    if jeu.état.v == ÉtatJeu.JEU and time.time()-jeu.dialogue_jeu_temps_début >= 3.0:
        dialogue.delete('1.0',"end")
        dialogue.markdownFormattage(random.choice(séquence.plans).dialogues[jeu.état.scène_animation_étape],retirerNL=False)
        dialogue.markdownFormattage("Tapez « ? » ou « aide » pour obtenir la liste des commandes.\n",retirerNL=False)
        jeu.dialogue_jeu_temps_début = time.time()
    elif jeu.état.v != ÉtatJeu.JEU:
        dialogue.delete('1.0',"end")
        dialogue.markdownFormattage(plan.dialogues[jeu.état.scène_animation_étape],retirerNL=False)

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
                def commande():
                    jeu = Jeu.avoirJeu()
                    jeu.état.scène_étape+=1

                bouton_continuer = Button(grille_boutons,text="Continuer",command=commande)
                bouton_continuer.pack(pady=10)
                fenetre.état = 0
        else:
            if fenetre.état != 1:
                for w in grille_boutons.winfo_children():
                    w.destroy()
                def commande():
                    jeu = Jeu.avoirJeu()
                    jeu.état.scène_étape = 0
                    jeu.état.scène_animation_étape = 0
                    jeu.état.v = ÉtatJeu.TRANSITION
                bouton_continuer = Button(grille_boutons,text="Continuer",command=commande)
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
                    def commande():
                        jeu = Jeu.avoirJeu()
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
                    bouton_continuer = Button(grille_boutons,text="Continuer",command=commande)
                    bouton_continuer.pack(pady=10)
                    fenetre.état = 2
            else:
                if fenetre.état != 3:
                    for w in grille_boutons.winfo_children():
                        w.destroy()
                    def commande():
                        jeu = Jeu.avoirJeu()
                        jeu.état.scène_étape += 1
                    bouton_continuer = Button(grille_boutons,text="Continuer",command=commande)
                    bouton_continuer.pack(pady=10)
                    fenetre.état = 3
    elif jeu.état.v == ÉtatJeu.JEU:
        if fenetre.état != 4:
            for w in grille_boutons.winfo_children():
                w.destroy()
            def fin_tour():
                jeu = Jeu.avoirJeu()
                jeu.état.v=ÉtatJeu.FIN_TOUR
            boutton_fin_tour = Button(grille_boutons,text="Terminer le tour",command=fin_tour)
            boutton_fin_tour.grid(column=2,row=0,padx=5,pady=5,sticky="ew")

            boutton_info = Button(grille_boutons,text="Info",command=lambda: commande_menu_info(jeu.état.v,["INFO",jeu.entité_sélectionnée.nom.upper()]))
            boutton_info.grid(column=0,row=0,padx=5,pady=5,sticky="ew")

            boutton_select = Button(grille_boutons,text="Sélectionner",command=lambda: commande_menu_select(jeu.état.v,["SELECT",jeu.entité_sélectionnée.nom.upper()]))
            boutton_select.grid(column=1,row=0,padx=5,pady=5,sticky="ew")

            boutton_combat = Button(grille_boutons,text="Combat",command=lambda: commande_menu_combat(jeu.état.v))
            boutton_combat.grid(column=0,row=1,padx=5,pady=5,sticky="ew")

            boutton_aide = Button(grille_boutons,text="Aide",command=lambda: commande_menu_aide(jeu.état.v))
            boutton_aide.grid(column=1,row=1,padx=5,pady=5,sticky="ew")

            def commande_réussir():
                jeu = Jeu.avoirJeu()
                for e in jeu.carte.entités:
                    if e.camp == Entité.CAMP_PAYSANS or e.camp == Entité.CAMP_PERSONNAGES:
                        e.estVivant = False
                jeu.état.v = ÉtatJeu.FIN_TOUR
            boutton_aide = Button(grille_boutons,text="Réussir",command=commande_réussir)
            boutton_aide.grid(column=2,row=1,padx=5,pady=5,sticky="ew")

            fenetre.état = 4
    elif jeu.état.v == ÉtatJeu.SUCCÈS:
        if carte.estScène:
            pass
        else:
            if jeu.état.scène_étape == len(séquence.plans)-1:
                if fenetre.état != 5:
                    for w in grille_boutons.winfo_children():
                        w.destroy()
                    def commande():
                        jeu = Jeu.avoirJeu()
                        jeu.état.v = ÉtatJeu.TRANSITION
                        jeu.état.scène_étape = 0
                        jeu.état.scène_animation_étape = 0
                    bouton_continuer = Button(grille_boutons,text="Continuer",command=commande)
                    bouton_continuer.pack(pady=10)
                    fenetre.état = 5
            else:
                if fenetre.état != 6:
                    for w in grille_boutons.winfo_children():
                        w.destroy()
                    def commande():
                        jeu = Jeu.avoirJeu()
                        jeu.état.scène_étape += 1
                    bouton_continuer = Button(grille_boutons,text="Continuer",command=commande)
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
                    def commande():
                        jeu = Jeu.avoirJeu()
                        jeu.état.v = ÉtatJeu.TERMINÉ
                        jeu.état.scène_étape = 0
                        jeu.état.scène_animation_étape = 0
                    bouton_continuer = Button(grille_boutons,text="Continuer",command=commande)
                    bouton_continuer.pack(pady=10)
                    fenetre.état = 7
            else:
                if fenetre.état != 8:
                    for w in grille_boutons.winfo_children():
                        w.destroy()
                    def commande():
                        jeu = Jeu.avoirJeu()
                        jeu.état.scène_étape += 1
                    bouton_continuer = Button(grille_boutons,text="Continuer",command=commande)
                    bouton_continuer.pack(pady=10)
                    fenetre.état = 8
    else:
        print(coul(gras("[menu.jeu] L'état du jeu n'est pas reconnus."),ROUGE))

def menuPrincipal():
    res = Ressources.avoirRessources()
    jeu = Jeu.avoirJeu()

    
    fenetre = res.obtenirMenu("menu_principal")

    if not fenetre.initialisé:
        
        titre = Label(fenetre.frame,text="Malheur à Alcadia!")
        titre.pack(pady=10)

        boutons = Frame(fenetre.frame)
        boutons.pack(anchor="center",expand=True)

        def bouton_commencer():
            jeu = Jeu.avoirJeu()
            if jeu.carte.estScène:
                jeu.état.v = ÉtatJeu.SCÈNE
            else:
                jeu.état.v = ÉtatJeu.DÉBUT
        commencer = Button(boutons,text="Commencer",command=bouton_commencer)
        commencer.pack(pady=5)

        def bouton_Quitter():
            jeu = Jeu.avoirJeu()
            jeu.état.v = ÉtatJeu.TERMINÉ
        quitter = Button(boutons,text="Quitter",command=bouton_Quitter)
        quitter.pack(pady=5)

        fenetre.frame.pack(fill="both",expand=True,anchor="center")
        jeu.frame_actuelle = fenetre
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
    print(gras("Aide!"))
    jeu = Jeu.avoirJeu()
    jeu.menu.menu_historique.append(historique)
    jeu.état.v = ÉtatJeu.MENU_CONTEXTUEL
    jeu.menu.v = MenuContextuel.AIDE
    jeu.déselectionner()

def commande_menu_combat(historique):
    jeu = Jeu.avoirJeu()
    jeu.menu.menu_historique.append(historique)
    jeu.état.v = ÉtatJeu.MENU_CONTEXTUEL
    jeu.menu.v = MenuContextuel.COMBAT
    jeu.déselectionner()

def commande_menu_select(historique, commande : list[str]):
    jeu = Jeu.avoirJeu()
    if len(commande) > 1:
        nom = commande[1]
        for e in jeu.carte.entités:
            if e.nom.upper() == nom:

                if e.camp == Entité.CAMP_PAYSANS:
                    print(coul("Vous ne pouvez pas donner d'ordres aux paysans.",ROUGE))
                    return False

                for i in range(len(jeu.menu.menu_historique)):
                    if jeu.menu.menu_historique[i] == MenuContextuel.SELECT:
                        jeu.menu.menu_historique.pop(i)
                        break

                jeu.menu.menu_historique.append(historique)
                jeu.état.v = ÉtatJeu.MENU_CONTEXTUEL
                jeu.menu.v = MenuContextuel.SELECT
                jeu.menu.menu_select_entité = e
                jeu.déselectionner()
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
                jeu.état.v = ÉtatJeu.MENU_CONTEXTUEL
                jeu.menu.v = MenuContextuel.INFO
                jeu.menu.menu_entité_entité = e
                jeu.déselectionner()
                return True
    print(coul("Veuillez entrer un nom qui se trouve dans la liste.",ROUGE))
    time.sleep(1.5)
    effaceCommande()
    return False

def commande_quitter():
    jeu = Jeu.avoirJeu()
    jeu.état.v = jeu.menu.menu_historique[0]
    jeu.menu.menu_historique.clear()
    jeu.déselectionner()

def commande_précédent():
    jeu = Jeu.avoirJeu()
    if len(jeu.menu.menu_historique) > 1:
        jeu.menu.v = jeu.menu.menu_historique.pop(-1)
    elif len(jeu.menu.menu_historique) > 0:
        jeu.état.v = jeu.menu.menu_historique.pop(-1)
    jeu.déselectionner()

def menu_aide():
    res = Ressources.avoirRessources()
    jeu = Jeu.avoirJeu()

    fenetre = res.obtenirMenu("menu_aide")
    jeu.peintre.estVisible = False

    if not fenetre.initialisé:
        titre = Label(fenetre.frame,text="Menu d'aide")
        titre.pack(pady=10)

        aide = Texte(fenetre.frame,background="#191a1e",foreground="#f7deb7",highlightthickness=0,relief="flat",wrap="word")

        aide.markdownFormattage("\n"+
             "Tapez « **C** » ou « **Combat** » pour voir les informations relatives au unitées et au combat\n"+
             "Tapez « **I** » ou « **Info** », suivit de **<NomUnité>** pour voir les information relatives à une unité.\n"+
             "Tapez « **S** » ou « **Select** » suivit de **<NomUnité>** pour sélectionner une unité et lui donner un ordre\n"+
             "\n"+
             "__En mode Select__ *(ces commandes ne sont disponibles que lorsque vous avez sélectionné une unité)* :\n"+
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
             "Tapez « **?** » ou « **Aide** » pour afficher cette liste à tout moment\n"+
             "Tapez « **P** » ou « **Précédent** » pour revenir au menu précédent.\n"
             "Tapez « **Q** » ou « **Quitter** » pour quitter.\n"+
             "\n",retirerNL=False)
        aide.pack(anchor="center",expand=True,fill="both",pady=10,padx=10)

        boutons = Frame(fenetre.frame)
        bouton_retour = Button(boutons,text="Retour",command=commande_précédent)
        bouton_retour.pack(side="left",padx=5,fill="both",expand=True)
        bouton_quitter = Button(boutons,text="Quitter",command=commande_quitter)
        bouton_quitter.pack(side="left",padx=5,fill="both",expand=True)
        boutons.pack(pady=10)

        fenetre.initialisé = True
    if jeu.frame_actuelle != fenetre:
        jeu.frame_actuelle.frame.pack_forget()
        fenetre.frame.pack(side="top",expand=True,fill="both")
        jeu.frame_actuelle = fenetre

def menu_combat():
    jeu = Jeu.avoirJeu()
    res = Ressources.avoirRessources()

    fenetre = res.obtenirMenu("menu_combat")

    if not fenetre.initialisé:
        titre = Label(fenetre.frame,text="Menu combat")
        titre.pack(pady=10,padx=10)

        conteneur_descritptions = Frame(fenetre.frame)
        conteneur_descritptions.pack(pady=10)
        fenetre.enregistrerWidget(conteneur_descritptions,"descriptions")

        boutton_retour = Button(fenetre.frame,text="Retour",command=commande_précédent)
        boutton_retour.pack(pady=10)
        boutton_quitter = Button(fenetre.frame,text="Quitter",command=commande_quitter)
        boutton_quitter.pack(pady=10)
        bouton_aide = Button(fenetre.frame,text="Aide",command=lambda: commande_menu_aide(MenuContextuel.COMBAT))
        bouton_aide.pack(pady=10)

        fenetre.initialisé = True

    if jeu.frame_actuelle != fenetre:

        conteneur_descritptions = fenetre.obtenirWidget("descriptions")
         
        for w in conteneur_descritptions.winfo_children():
            w.destroy()
        
        camps = []
        
        for e in jeu.carte.entités:
            if not e.camp in camps:
                camps.append(e.camp)

        for c in camps:
            texte = Texte(conteneur_descritptions,height=int(2*Texte.police_taille_scalaire),background="#191a1e",foreground="#f7deb7",highlightthickness=0,relief="flat",wrap="word")
            texte.insérerFormatté(c,soul=True,niveau_Titre=5)
            texte.pack(side="top",fill="x",expand=True,pady=0)
            for e in jeu.carte.entités:
                if e.camp == c:
                    conteneur_entité = Frame(conteneur_descritptions,style="conteneur_entité.TFrame")
                    texte = Texte(conteneur_entité,height=1,background="#191a1e",foreground="#f7deb7",highlightthickness=0,relief="flat",wrap="word")
                    texte.markdownFormattage("**"+e.nomAffichage+"** > PV : " +  str(int(e.PV)))
                    texte.pack(side="left",fill="x")
                    bouton_info = Button(conteneur_entité, text="Info",command=lambda e=e: commande_menu_info(MenuContextuel.COMBAT,["INFO",e.nom.upper()]), style="Boutons_Combat.TButton")
                    bouton_info.pack(side="left",padx=10)
                    if e.camp in [Entité.CAMP_JOUEUR,Entité.CAMP_GOLEMS]:
                        bouton_select = Button(conteneur_entité, text="Sélectionner", command=lambda e=e: commande_menu_select(MenuContextuel.COMBAT,["select",e.nom.upper()]), style="Boutons_Combat.TButton")
                        bouton_select.pack(side = "left",padx=10)
                    conteneur_entité.pack(side="top",pady=0,fill="x",expand=True,ipadx=5,ipady=5)

        jeu.frame_actuelle.frame.pack_forget()
        fenetre.frame.pack(fill="both",expand=True)
        jeu.frame_actuelle = fenetre

def menu_info():
    jeu = Jeu.avoirJeu()
    res = Ressources.avoirRessources()

    fenetre = res.obtenirMenu("menu_info")

    if not fenetre.initialisé:
        titre = Label(fenetre.frame,text="Menu de statistique du combat")
        titre.pack()

        texte = Texte(fenetre.frame)
        texte.pack()
        fenetre.enregistrerWidget(texte,"texte")

        boutton_select = Button(fenetre.frame,text="Sélectionner",command=lambda: commande_menu_select(MenuContextuel.INFO,["SELECT",jeu.menu.menu_entité_entité.nom.upper()]))
        boutton_select.pack()
        boutton_aide = Button(fenetre.frame,text="Aide",command=lambda: commande_menu_aide(MenuContextuel.INFO))
        boutton_aide.pack()
        boutton_retour = Button(fenetre.frame,text="Précédent",command=commande_précédent)
        boutton_retour.pack()
        boutton_quitter = Button(fenetre.frame,text="Quitter",command=commande_quitter)
        boutton_quitter.pack()
        
        fenetre.initialisé = True
    if jeu.frame_actuelle != fenetre:
        texte = fenetre.obtenirWidget("texte")
        texte.delete('1.0',"end")
        texte.markdownFormattage(jeu.menu.menu_entité_entité.avoirInfoStr())

        jeu.frame_actuelle.frame.pack_forget()
        fenetre.frame.pack()
        jeu.frame_actuelle = fenetre

def menu_select():
    jeu = Jeu.avoirJeu()
    res = Ressources.avoirRessources()

    fenetre = res.obtenirMenu("menu_select")

    if not fenetre.initialisé:
        titre = Label(fenetre.frame,text="Donnez un ordre à " + jeu.menu.menu_select_entité.nomAffichage)
        titre.pack()

        peintre_conteneur = Frame(fenetre.frame, width=100,height=100,style="conteneur_entité.TFrame")
        peintre_conteneur.pack(fill="both",expand=True)
        fenetre.enregistrerWidget(peintre_conteneur,"peintre")

        grille_bouttons = Frame(fenetre.frame)
        grille_bouttons.pack(side="bottom")
        fenetre.enregistrerWidget(grille_bouttons,"bouttons")

        boutton_aide = Button(fenetre.frame,text="Aide",command=lambda: commande_menu_aide(MenuContextuel.SELECT))
        boutton_aide.pack(side="bottom")
        boutton_retour = Button(fenetre.frame,text="Précédent",command=commande_précédent)
        boutton_retour.pack(side="bottom")
        boutton_quitter = Button(fenetre.frame,text="Quitter",command=commande_quitter)
        boutton_quitter.pack(side="bottom")

        fenetre.initialisé = True
    if jeu.frame_actuelle != fenetre:
        peintre_conteneur = fenetre.obtenirWidget("peintre")
        jeu.peintre.pack_forget()
        jeu.peintre.pack(in_=peintre_conteneur,fill="both",expand=True)
        jeu.peintre.estVisible = True

        grille_bouttons = fenetre.obtenirWidget("bouttons")

        for w in grille_bouttons.winfo_children():
            w.destroy()

        def commande_déplacer():
            jeu = Jeu.avoirJeu()
            if jeu.case_sélectionnée != None:
                commande = Commande()
                commande.faireCommandeDéplacement(jeu.case_sélectionnée)
                jeu.menu.menu_select_entité.commande(commande)
                jeu.déselectionner()

        if type(jeu.menu.menu_select_entité) == Joueur:

            def commande_créer_gollem():
                jeu = Jeu.avoirJeu()
                if jeu.case_sélectionnée != None:
                    commande = Commande()
                    commande.faireCommandeCréerGolem(jeu.case_sélectionnée)
                    jeu.menu.menu_select_entité.commande(commande)
                    jeu.déselectionner()
            boutton_cg = Button(grille_bouttons,text="Créer Golem",command=commande_créer_gollem)
            boutton_cg.pack(side="right")

            boutton_dp = Button(grille_bouttons,text="Déplacer",command=commande_déplacer)
            boutton_dp.pack(side="left")
        else:
            boutton_dp = Button(grille_bouttons,text="Déplacer",command=commande_déplacer)
            boutton_dp.pack(side="left")

            def commande_attaque():
                jeu = Jeu.avoirJeu()
                if jeu.entité_sélectionnée != None:
                    commande = Commande()
                    commande.faireCommandeAttaque(jeu.entité_sélectionnée)
                    jeu.menu.menu_select_entité.commande(commande)
            boutton_a = Button(grille_bouttons,text="Attaquer",command=commande_attaque)
            boutton_a.pack(side="left")

            def commande_attaque_spéciale():
                jeu = Jeu.avoirJeu()
                try:
                    commande = Commande()
                    commande.faireCommandeAttaqueSpéciale(jeu.menu.menu_select_entité.ATTAQUE_SPÉCIALE)
                    jeu.menu.menu_select_entité.commande(commande)
                except:
                    print("HuHo...")
            boutton_as = Button(grille_bouttons,text="Attaque Spéciale",command=commande_attaque_spéciale)
            boutton_as.pack(side="left")
        
            def commande_défense():
                jeu = Jeu.avoirJeu()
                commande = Commande()
                commande.faireCommandeDéfense()
                jeu.menu.menu_select_entité.commande(commande)
            boutton_df = Button(grille_bouttons,text="Défense",command=commande_défense)
            boutton_df.pack(side="left")

            def commande_charger_attaque():
                jeu = Jeu.avoirJeu()
                commande = Commande()
                commande.faireCommandeCharger()
                jeu.menu.menu_select_entité.commande(commande)
            boutton_ca = Button(grille_bouttons,text="Charger Attaque",command=commande_charger_attaque)
            boutton_ca.pack(side="left")

            def commande_attaquer_charge(jeu : Jeu):
                jeu = Jeu.avoirJeu()
                if jeu.entité_sélectionnée != None:
                    commande = Commande()
                    commande.faireCommandeAttaquerCharge(jeu.entité_sélectionnée)
                    jeu.menu.menu_select_entité.commande(commande)
            boutton_ac = Button(grille_bouttons,text="Attaquer Charge",command=commande_attaquer_charge)
            boutton_ac.pack(side="left")

            def commande_libérer(jeu : Jeu):
                jeu = Jeu.avoirJeu()
                commande = Commande()
                commande.faireCommandeLibérer()
                jeu.menu.menu_select_entité.commande(commande)
            boutton_l = Button(grille_bouttons,text="Libérer",command=commande_libérer)
            boutton_l.pack(side="left")

        jeu.frame_actuelle.frame.pack_forget()
        fenetre.frame.pack()
        jeu.frame_actuelle = fenetre
    
    """
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
            commande_menu_aide(MenuContextuel.SELECT)
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
    """


def main():
    width, eight = 20, 10

    game_map = [["." for _ in range(width)] for _ in range(eight)]

    while True:
        menuPrincipal(game_map)
        break

if __name__ == "__main__":
    main()# exemple de premiere page comme menu
