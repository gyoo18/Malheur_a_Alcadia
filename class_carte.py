class Carte:
    ligne : int
    colonne : int
    
    def __init__(self,ligne : int ,colonne :int):
        self.ligne = ligne
        self.colonne= colonne

    

    def creation(self):
        matrice = []
        for ligne in range(self.ligne):
            ligne_donnee = []
            for colonne in range(self.colonne):
                ligne_donnee.append("0")
            matrice.append(ligne_donnee)
        return matrice
    
            
    

carte_1 = Carte(10,10) 

mape = carte_1.creation()
print(mape)

for ligne,colonne in enumerate(mape):
    print(ligne,colonne)
