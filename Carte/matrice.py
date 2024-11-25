

def matrice(ligne,colonne,tuile):
        carte = []
        for ligne in range(ligne):
            ligne_donnee = []
        for colonne in range(colonne):
            ligne_donnee.append(tuile)
            carte.append(ligne_donnee)
        return carte





carte1= matrice(10,10,"0")
print(carte1)




"""
carte2 = matrice(10,10,"~")

carte3 = matrice (10,10,"*")

"""