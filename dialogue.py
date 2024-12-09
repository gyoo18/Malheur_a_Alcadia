from Jeu import Chapitre, ÉtatJeu, Jeu
from GestionnaireRessources import Ressources
from TFX import * # TFX pour TerminalFX
from Maths.Vec3 import Vec3

def dialogue(texte, personnage) :
    # Melios = protag / # Guildart / # Roi / #Enfant / #Partenaire
    return "\n" + (f"{personnage} : {texte}")

def titre(nombreZone):
    if(nombreZone == 1):
        return "Prairie"
    elif(nombreZone == 2):
        return "Cite"
    elif(nombreZone == 3):
        return "Chateau"
    else:
        return "Il faut retourner un numero entre 1 et 3"

#Le jeu a été enlevé parce qu'on ne peut plus cloturer le jeu après un return :) ni avant, 
# vu que ca fermerait le jeu avant l'aparition du message
def script(Zone : str, Timing : str, choix : str, jeu : Jeu) : 
    message = ""
    if(Zone == Chapitre.INTRODUCTION) :
        
        jeu.état.v = ÉtatJeu.TRANSITION
    elif(Zone == Chapitre.CHAPITRE1):
        if(Timing == ÉtatJeu.DÉBUT):
            message += ("\nLe château est attaqué par une menace extérieure ! Une multitude de créature ont émergées de la montagne sacrée, ravageant tout sur leur passage.")
            message += ("\nLe roi ordonne au bataillon d'alchimistes de défendre la plaine.")
            message += ("\n________ Plaine ________")
        elif(Timing == ÉtatJeu.SUCCÈS):
            message += ("\nFélicitation !") 
            message += ("\nVous avez réussi à protéger la plaine ! Néanmoins, les ennemis sont de plus en plus nombreux, vous devez faire marche arrière dans la cité.")
            message += dialogue("Soldat ! Défendez la cité.", "Guildart")
            jeu.état.v = ÉtatJeu.TRANSITION
        elif(Timing == ÉtatJeu.ÉCHEC):
            message += dialogue("Peut-être que je n'étais jamais destiné à être un guerrier, pardonnez-moi, j'ai échoué...", "Melios")
            message += ("\nFin_01 : Vous êtes tombé en défendant la plaine.")
            jeu.état.v = ÉtatJeu.TERMINÉ
    elif(Zone == Chapitre.CHAPITRE2):
        if(Timing == ÉtatJeu.DÉBUT):
            message += ("\n________ Cité ________")
            message += ("\nLes monstres se sont infiltré dans nos remparts.")
            message += dialogue("Soldat ! Défendez la cité.", "Guildart")
            message += ("Votre expérience de combat vous permet d'utilise un nouveau golem !")
            message += dialogue("Le sol a une composition différente. Je pense que ça ferait un résultat intéréssant.", "Melios")
        elif(Timing == ÉtatJeu.SUCCÈS):
            message += ("\nVous avez réussi ! Néanmoins le corps d'un ami gis au sol. Guildart s'est sacrifié pour protéger sa ville.")
            message += ("\nMais pas le temps de le pleurer : un nouvel ennemis s'approche, mais au lieu d'attaquer, il se mit à parler.")
            message += ("\nSa voix était rauque, à peine audible, mais emprunte de tristesse.")
            message += dialogue("S'il vous plait, cessez cette folie... Rentrons à la maison...","Petit Monstre")
            message += ("\nQue faites-vous ? (fuir : Fuir avec le monstre / tuer : Tuer le monstre)")
            jeu.état.v = ÉtatJeu.CHOIX
            #IL FAUT METTRE UN INPUT "reponse" DE VOTRE COTE !!!! Puis faire script("Cite", "Choix", reponse)
        elif(Timing == ÉtatJeu.CHOIX):
            if choix == "fuir":
                message += ("\nVous lachez vos armes, prenez la main du petit monstre et traversez les ruines de la cité pour partir.")
                message += ("\nUn regard en arrière vous retient, était-ce vraiment la bonne décision de fuir ses responsabilités ?")
                message += ("\nLe petit monstre n'a rien de dangereux, il est même frêle, ces monstres ont détruit leur ville, mais envoyait également leurs enfants ?")
                message += ("\nEt la question vous hante ; Pourquoi ?")
                message += ("\nFin_03 : Vous vous êtes enfui avec le petit monstre.")   
                jeu.état.v = ÉtatJeu.TERMINÉ
            else:
                message += ("\nD'un geste bref, votre golem abbat le Petit Monstre. Il est inutile de prendez pitié pour l'ennemi.")
                message += ("\nIls ont tués le chef du bataillon, Guildart, il ne méritait pas ce destin.")
                jeu.état.v = ÉtatJeu.TRANSITION
        elif(Timing == ÉtatJeu.ÉCHEC):
                message += dialogue("J'espère que ma famille est en sécurité... Je suis désolé de ne pas avoir pu vous protéger...","Melios")
                message += ("\nFin_02 : Vous êtes tombé en défendant la cité.")
                jeu.état.v = ÉtatJeu.TERMINÉ
    elif(Zone == Chapitre.CHAPITRE3):
        if(Timing == ÉtatJeu.DÉBUT):
            message += ("\n________ Château, Salle du trône ________")
            message += ("\nAprès l'annonce de la mort de Guildart. Vous êtes désigné pour devenir le nouveau chef du bataillon ...")
            message += ("\nLe roi compte sur vous pour le protéger. Il n'y a plus que vous.")
            message += ("\nVotre rage vous pousse à accepter et à combatre avec tout ce qui vous reste.")
            message += dialogue("Je vous protègerais au péril de ma vie, Majestée.", "Melios")
        elif(Timing == ÉtatJeu.SUCCÈS):
            message += ("\nIl n'y a plus de monstres... Plus que des tas de chaire flous répendues sur le sol.")
            message += ("\nLe roi est vivant, sain et sauf. Vous avez réussi.")
            message += ("\nAlors que vous pensiez enfin pouvoir vous reposer, un ennemi apparu entre les immenses portes.")
            message += dialogue("Melios ! Qu'est ce que tu fais ?","Monstre (?)")
            message += dialogue("Monstre ! Comment connais-tu mon nom ?!","Melios")
            message += dialogue("Ce n'est pas important, tuez-le.","Roi")
            message += dialogue("Non Melios ! C'est moi, Delain, tu te rappelles ? Le roi nous avait tous enfermés dans la montagne sacrée mais nous avons réussit à sortir !","Monstre (?)")
            message += dialogue("Mensonges !","Roi")
            message += dialogue("Melios ! Je t'en conjure, arrêtons cette folie, tout le monde est mort...","Monstre (?)")
            message += dialogue("Soldat ! Tuez ce monstre !","Roi")
            message += ("\nQue faites vous ? (fuir : Fuir avec le monstre / tuer : Tuer le monstre / assassiner : Tuer le roi) : ")
            jeu.état.v = ÉtatJeu.CHOIX
            #IL FAUT METTRE UN INPUT "reponse" DE VOTRE COTE !!!! Puis faire script("Chateau", "Choix", reponse)
        elif(Timing == ÉtatJeu.ÉCHEC):
            message += dialogue("J'aurais voulu faire plus... Mais je ne peux pas... Pardon... Pardon...","Melios")
            message += ("Fin_04 : Vous êtes tombé en défendant le château.")
            jeu.état.v = ÉtatJeu.TERMINÉ
        elif(Timing == ÉtatJeu.CHOIX):
            if choix == "assassiner":
                message += ("\nFin_06 : Vous tuez le roi, prenez le trône. Vous et Delain reignez sur la ville pour réparer les erreurs du Roi précédent.")     
                jeu.état.v = ÉtatJeu.TERMINÉ            
            elif choix == "tuer":
                message += ("\nFin_05 : Vous tuez le monstre et vivez dans le luxe. Chaque verre de vin ingurgité vous rappelle que vous étiez à deux doigts de mourir, maintes fois. Vous aimez la sensation d'oublier une fois saoul.")        
                jeu.état.v = ÉtatJeu.TERMINÉ
            else :
                message += ("\nFin_07 : Vous attrapez la main du monstre, Delain, votre partenaire. En un instant vous fuyez les ruines de la ville, vous vous précipiter dans les décombres, trébuchez sur les cadavres pour sortir jusque dans la forêt. Là bas, vous construirez un chalet et vivrez calmement pour le reste de vos vies.")
                jeu.état.v = ÉtatJeu.TERMINÉ
    return message
