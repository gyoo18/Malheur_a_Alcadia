import interface
from Ressources import Ressources
from Carte.class_carte import Carte
from Entités.Entité import Entité
from Jeu import Jeu, ÉtatJeu

jeu : Jeu = None

def Constructeur():
    res = Ressources.avoirRessources()
    carte = Carte(5,5)
    entité = Entité(carte)
    res.cartes.append(carte)
    res.entités.append(entité)

    global jeu
    jeu = Jeu()
    jeu.état.v = ÉtatJeu.MENU
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