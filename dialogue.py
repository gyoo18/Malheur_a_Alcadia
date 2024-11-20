from Jeu import Jeu, ÉtatJeu
from Ressources import Ressources

def zone_1(): 
    print("Le château se fait attaquer par une menace extérieure,l'attaque est donnée du côté de la porte condamnée qui se trouve sur la montagne sacrée.")
    print("Le roi donne l'ordre au bataillon d'alchimistes de défendre le château.")
    success  = combat_simple()
    if success :
        print("Il y a beaucoup trop de monstres, nous devons nous replier vers la cité!")
        return "success"
    else:
        print("Je n'était sûrement pas destiné à la vie d'alchimiste, j'aimerais revoir une seule fois avant de mourir.")
        return "failure"
    
def zone_2():
    print("Vous êtes dans la cité. Les monstres attaquent également de ce côté")
    # TODO #2 Compléter la phrase
    print("Chef Alchimiste : « Vous avez maintenant une très grande expérience de combat réel, vous êtes de ce fait suffisamment près pour utiliser le nouveau ... »")
    print("Le sol a une composition différente. Je pense que ça ferait un résultat intéréssant.")
    print("Le Cher Alchimiste explique comment invoquer un golem.")
    input("Appuyez sur entrée pour invoquer un golem.")
    success = combat_complexe()
    if success:
        print("Vous avez repoussé les monstres, mais un monstre paralant approche.")
        choix = input("Le monstre vous supplie d'arrêter. Que faites-vous?(1: fuir avec le monstre, 2: le tuer)")
        if choix == "1":
            print("Le protagoniste s'enfuit avec l'enfant du monstre non genré, mais ne sait pas si sa décision est la bonne.")
            return "fuir"
        else:
            print("Il tue le monstre et une alarme retenti en sommant toute la population de retourner à l'intérieur du château.")
            return "success"
    else: 
            print("J'espère que ma famille est en sécurité et que le chef pourra exterminer tout ces monstres.")
            return"failure"
    
def zone_3(fin_zone_2):
    print("Vous arrivez au château. Le roi compte sur vous pour le protéger.")
    # TODO #3 Compléter la phrase
    print("Le chef est mort et le bataillon est réduit de son effectif de départ, il est informé et on le désigne pour devenir le nouveau chef du batillon ...")
    if fin_zone_2 == "fuir":
        print("Vous êtes tourmenté par votre décision de fuir les monstres.")
    else:
        print("Votre rage vous pousse à accepter et à combatre avec tout ce qui vous reste.")
        combat = combat_final()
        if combat:
            print("Vous avez vaincus tous les monstres. Mais un choix difficile vous attend.")
            choix = input("Le roi vous demande de tuer votre épouse [1/2/3]")
            return choix
        else:
            print("Vous êtes tombés au combat, soulagé de mourir après tant de sacrifices.")
            return "failure"
    
def combat_simple():
    return input("Tapez 'gagner' pour simuler une victoire, sinon vous perdez : ").lower() == "gagner"

def combat_complexe():
    return input("Tapez 'gagner' pour simuler une victoire, sinon, vous perdez : ").lower() == "gagner"

def combat_final():
    return input("Tatpez 'gagner' pour simuler une vicoire, sinon vous perdez : ").lower() == "gagner"

def jeu_principal(jeu : Jeu):
    match jeu.état.v:
        case ÉtatJeu.ZONE1:
            print("Introduction : Vous êtes un alchimiste malvoyant chargé de protéger le roi.")
            resultat_zone_1 = zone_1()
            if resultat_zone_1 == "failure":
                print("Fin_01 : vous êtes tombé lors du premier combat.")
                jeu.état.v = ÉtatJeu.TERMINÉ
        case ÉtatJeu.ZONE2:
            res = Ressources.avoirRessources()
            res.resultat_zone_2 = zone_2()
            if res.resultat_zone_2 == "failure":
                print("Fin_02 : vous êtes tombé en défendant la cité.")
                jeu.état.v = ÉtatJeu.TERMINÉ
        case ÉtatJeu.ZONE3:
            res = Ressources.avoirRessources()
            resultat_zone_3 = zone_3(res.resultat_zone_2)
            if resultat_zone_3 == "failure":
                print("Fin_04 : vous êtes mort en défendant le château.")
                jeu.état.v = ÉtatJeu.TERMINÉ
            elif resultat_zone_3 == "1":
                print("Fin_06 : vous tuez le roi et prenez le trône.")
                jeu.état.v = ÉtatJeu.TERMINÉ
            elif resultat_zone_3 == "2":
                print("Fin_05 : vous tuez votre épouse transformée en monstre et vivez dans le luxe et la tourmente.")
                jeu.état.v = ÉtatJeu.TERMINÉ
            elif resultat_zone_3 == "3":
                print("Fin_07 : vous partez vivre dans la montagne avec votre épouse trasformée en monstre.")
                jeu.état.v = ÉtatJeu.TERMINÉ
