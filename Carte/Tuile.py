class Tuiles:
    
    TYPE_TERRE ="0"
    TYPE_EAU ="~"
    TYPE_FEUX ="*"
    TYPE_MUR ="#"

    def __init__(self,type):
        self.type : str = type

    



plat = Tuiles.TYPE_FEUX
droit = Tuiles(Tuiles.TYPE_EAU)


print(plat)


