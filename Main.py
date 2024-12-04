from Ressources import Ressources
from Carte.class_carte import Carte
from Entités.Paysan import *
from Entités.Golem import *
from Jeu import Jeu, ÉtatJeu
from random import randrange

jeu : Jeu = None

def Constructeur():
    res = Ressources.avoirRessources()
    carte = Carte(5,5)
    carte.creation()
    paysan = Gosse()
    paysan.pos = Vec2(randrange(0,4),randrange(0,4))
    golem = GolemTerre()
    golem.pos = Vec2(randrange(0,4),randrange(0,4))
    golem.carte = carte
    paysan.carte = carte
    carte.entités.append(paysan)
    carte.entités.append(golem)
    res.cartes.append(carte)
    res.entités.append(paysan)
    res.entités.append(golem)

    global jeu
    jeu = Jeu.avoirJeu()
    jeu.état.v = ÉtatJeu.MENU
    jeu.carte = carte
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