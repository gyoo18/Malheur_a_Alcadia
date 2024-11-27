from Jeu import Jeu, ÉtatJeu
from Ressources import Ressources
from TFX import * # TFX pour TerminalFX

def dialogue(texte, personnage) :
    # Melios = protag / # Guildart / # Roi / #Enfant / #Partenaire
    print(f"{personnage} : {texte}")

def script(Zone, Timing, jeu : Jeu) :
    if(Zone == "Introduction") :
        print("Vous êtes Melios, un alchimiste atteint de Glaucoma, un type de malvoyance, chargé de protéger le roi.")
        print("Très tôt ce matin, l'alarme d'invasion avait retentie dans l'enceinte de la paisible ville d'Alcadia.")
        return
    elif(Zone == "Prairie"):
        if(Timing == "Debut"):
            print("Le château est attaqué par une menace extérieure ! Une multitude de créature ont émergées de la montagne sacrée, ravageant tout sur leur passage.")
            print("Le roi ordonne au bataillon d'alchimistes de défendre la plaine.")
            print("________ Plaine ________")
            return    
        elif(Timing == "Success"):
            print("Félicitation !") 
            print("Vous avez réussi à protéger la plaine ! Néanmoins, les ennemis sont de plus en plus nombreux, vous devez faire marche arrière dans la cité.")
            dialogue("Soldat ! Défendez la cité.", "Guildart")
            return 
        elif(Timing == "Failure"):
            dialogue("Peut-être que je n'étais jamais destiné à être un guerrier, pardonnez-moi, j'ai échoué...", "Melios")
            print("Fin_01 : Vous êtes tombé en défendant la plaine.")
            jeu.état.v = ÉtatJeu.TERMINÉ 
            return
    elif(Zone == "Cite"):
        if(Timing == "Introduction"):
            #res = Ressources.avoirRessources()
            print("________ Cité ________")
            print("Les monstres se sont infiltré dans nos remparts.")
            dialogue("Soldat ! Défendez la cité.", "Guildart")
            dialogue("Votre expérience de combat vous permet d'utilise un nouveau golem !")
            dialogue("Le sol a une composition différente. Je pense que ça ferait un résultat intéréssant.", "Melios")
        elif(Timing == "Success"):
            print("Vous avez réussi ! Néanmoins le corps d'un ami gis au sol. Guildart s'est sacrifié pour protéger sa ville.")
            print("Mais pas le temps de le pleurer : un nouvel ennemis s'approche, mais au lieu d'attaquer, il se mit à parler.")
            print("Sa voix était rauque, à peine audible, mais emprunte de tristesse.")
            dialogue("S'il vous plait, cessez cette folie... Rentrons à la maison...","Petit Monstre")
            choix = input("Que faites-vous ? (fuir : Fuir avec le monstre / tuer : Tuer le monstre)")
            if choix == "fuir":
                print("Vous lachez vos armes, prenez la main du petit monstre et traversez les ruines de la cité pour partir.")
                print("Un regard en arrière vous retient, était-ce vraiment la bonne décision de fuir ses responsabilités ?")
                print("Le petit monstre n'a rien de dangereux, il est même frêle, ces monstres ont détruit leur ville, mais envoyait également leurs enfants ?")
                print("Et la question vous hante ; Pourquoi ?")
                jeu.état.v = ÉtatJeu.TERMINÉ 
                return
            else:
                print("D'un geste bref, votre golem abbat le Petit Monstre. Il est inutile de prendez pitié pour l'ennemi.")
                print("Ils ont tués le chef du bataillon, Guildart, il ne méritait pas ce destin.")
                return
        elif(Timing == "Failure"):
                dialogue("J'espère que ma famille est en sécurité... Je suis désolé de ne pas avoir pu vous protéger...","Melios")
                jeu.état.v = ÉtatJeu.TERMINÉ 
                return
        return
    elif(Zone == "Chateau"):
        if(Timing == "Introduction"):
            print("________ Château, Salle du trône ________")
            print("Après l'annonce de la mort de Guildart. Vous êtes désigné pour devenir le nouveau chef du bataillon ...")
            print("Le roi compte sur vous pour le protéger. Il n'y a plus que vous.")
            print("Votre rage vous pousse à accepter et à combatre avec tout ce qui vous reste.")
            dialogue("Je vous protègerais au péril de ma vie, Majestée.", "Melios")
        if(Timing == "Success"):
            print("Il n'y a plus de monstres... Plus que des tas de chaire flous répendues sur le sol.")
            print("Le roi est vivant, sain et sauf. Vous avez réussi.")
            print("Alors que vous pensiez enfin pouvoir vous reposer, un ennemi apparu entre les immenses portes.")
            dialogue("Melios ! Qu'est ce que tu fais ?","Monstre (?)")
            dialogue("Monstre ! Comment connais-tu mon nom ?!","Melios")
            dialogue("Ce n'est pas important, tuez-le.","Roi")
            dialogue("Non Melios ! C'est moi, Delain, tu te rappelles ? Le roi nous avait tous enfermés dans la montagne sacrée mais nous avons réussit à sortir !","Monstre (?)")
            dialogue("Mensonges !","Roi")
            dialogue("Melios ! Je t'en conjure, arrêtons cette folie, tout le monde est mort...","Monstre (?)")
            dialogue("Soldat ! Tuez ce monstre !","Roi")
            choix = input("Que faites vous ? (fuir : Fuir avec le monstre / tuer : Tuer le monstre / assassiner : Tuer le roi)")
            if choix == "assassiner":
                print("Fin_06 : Vous tuez le roi, prenez le trône. Vous et Delain reignez sur la ville pour réparer les erreurs du Roi précédent.")
                jeu.état.v = ÉtatJeu.TERMINÉ 
            elif choix == "tuer":
                print("Fin_05 : Vous tuez le monstre et vivez dans le luxe. Chaque verre de vin ingurgité vous rappelle que vous étiez à deux doigts de mourir, maintes fois. Vous aimez la sensation d'oublier une fois saoul.")
                jeu.état.v = ÉtatJeu.TERMINÉ 
            else :
                print("Fin_07 : Vous attrapez la main du monstre, Delain, votre partenaire. En un instant vous fuyez les ruines de la ville, vous vous précipiter dans les décombres, trébuchez sur les cadavres pour sortir jusque dans la forêt. Là bas, vous construirez un chalet et vivrez calmement pour le reste de vos vies.")
                jeu.état.v = ÉtatJeu.TERMINÉ 
        if(Timing == "Failure"):
            dialogue("J'aurais voulu faire plus... Mais je ne peux pas... Pardon... Pardon...","Melios")
            print("Fin_04 : Vous êtes tombé en défendant le château.")
            jeu.état.v = ÉtatJeu.TERMINÉ 
            return

