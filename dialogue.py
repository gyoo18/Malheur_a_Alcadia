def combat_simple():
    return input("Tapez 'gagner' pour simuler une victoire, sinon vous perdez : ").lower() == "gagner"

def combat_complexe():
    return input("Tapez 'gagner' pour simuler une victoire, sinon, vous perdez : ").lower() == "gagner"

def combat_final():
    return input("Tatpez 'gagner' pour simuler une vicoire, sinon vous perdez : ").lower() == "gagner"

def zone_1(): 
    print("Le château est attaqué par une menace extérieure ! Une multitude de créature ont émergées de la montagne sacrée, ravageant tout sur leur passage.")
    print("Le roi ordonne au bataillon d'alchimistes de défendre la plaine.")
    print("________ Plaine ________")
    success  = combat_simple()
    if success :
        print("Félicitation ! Vous avez réussi à protéger la plaine ! Néanmoins, les ennemis sont de plus en plus nombreux, vous devez faire marche arrière dans la cité.")
        return "success"
    else:
        dialogue("Peut-être que je n'étais jamais destiné à être un guerrier, pardonnez-moi, j'ai échoué...", "Melios")
        return "failure"
    
def zone_2():
    print("________ Cité ________")
    print("Les monstres se sont infiltré dans nos remparts.")
    dialogue("Soldat ! Défendez la cité.", "Guildart")
    dialogue("Votre expérience de combat vous permet d'utilise un nouveau golem !")
    dialogue("Le sol a une composition différente. Je pense que ça ferait un résultat intéréssant.", "Melios")
    success = combat_complexe()
    if success:
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
        else:
            print("D'un geste bref, votre golem abbat le Petit Monstre. Il est inutile de prendez pitié pour l'ennemi.")
            print("Ils ont tués le chef du bataillon, Guildart, il ne méritait pas ce destin.")
            return "success"
    else: 
            dialogue("J'espère que ma famille est en sécurité... Je suis désolé de ne pas avoir pu vous protéger...","Melios")
            return"failure"
    
def zone_3(fin_zone_2):
    print("________ Château, Salle du trône ________")
    print("Après l'annonce de la mort de Guildart. Vous êtes désigné pour devenir le nouveau chef du bataillon ...")
    print("Le roi compte sur vous pour le protéger. Il n'y a plus que vous.")
    
    if fin_zone_2 == "fuir":
        print("Vous êtes tourmenté par votre décision de fuir les monstres. Vous ne pouvez plus partir.")
    else:
        print("Votre rage vous pousse à accepter et à combatre avec tout ce qui vous reste.")
        dialogue("Je vous protègerais au péril de ma vie, Majestée.", "Melios")
    success = combat_final()
    if success:
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
        return choix
    else:
        dialogue("J'aurais voulu faire plus... Mais je ne peux pas... Pardon... Pardon...","Melios")
        return "failure"
    

def dialogue(texte, personnage) :
    #Mettre image de personnage
    # Melios = protag / # Guildart / # Roi / #Enfant / #Partenaire
    print(f"{personnage} : {texte}")

def jeu_principal():
    print("Vous êtes Melios, un alchimiste atteint de Glaucoma, un type de malvoyance, chargé de protéger le roi.")
    print("Très tôt ce matin, l'alarme d'invasion avait retentie dans l'enceinte de la paisible ville d'Alcadia.")

    resultat_zone_1 = zone_1()
    if resultat_zone_1 == "failure":
        print("Fin_01 : Vous êtes tombé en défendant la plaine.")
        return
    else : 
        print("Félicitation ! Vous avez réussi à protéger la plaine ! Néanmoins, les ennemis sont de plus en plus nombreux, vous devez faire marche arrière dans la cité.")
        dialogue("Soldat ! Défendez la cité.", "Guildart")
       
    resultat_zone_2 = zone_2()
    if resultat_zone_2 == "failure":
        print("Fin_02 : Vous êtes tombé en défendant la cité.")
        return
    resultat_zone_3 = zone_3(resultat_zone_2)
    if resultat_zone_3 == "failure":
        print("Fin_04 : Vous êtes tombé en défendant le château.")
    elif resultat_zone_3 == "assassiner":
        print("Fin_06 : Vous tuez le roi, prenez le trône. Vous et Delain reignez sur la ville pour réparer les erreurs du Roi précédent.")
    elif resultat_zone_3 == "tuer":
        print("Fin_05 : Vous tuez le monstre et vivez dans le luxe. Chaque verre de vin ingurgité vous rappelle que vous étiez à deux doigts de mourir, maintes fois. Vous aimez la sensation d'oublier une fois saoul.")
    else :
        print("Fin_07 : Vous attrapez la main du monstre, Delain, votre partenaire. En un instant vous fuyez les ruines de la ville, vous vous précipiter dans les décombres, trébuchez sur les cadavres pour sortir jusque dans la forêt. Là bas, vous construirez un chalet et vivrez calmement pour le reste de vos vies.")

