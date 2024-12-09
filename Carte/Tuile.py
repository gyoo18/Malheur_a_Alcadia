class Tuile:
    
    TYPE_TERRE ="0"
    TYPE_EAU ="~"
    TYPE_FEUX ="*"
    TYPE_OR = "$"
    TYPE_MUR ="#"

    def __init__(self,type):
        self.type : str = type
        self.dessin_atlas_indexe : int = -1

    



plat = Tuile.TYPE_FEUX
droit = Tuile(Tuile.TYPE_EAU)


print(plat)


