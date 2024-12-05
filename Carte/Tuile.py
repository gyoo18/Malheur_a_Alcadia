class Tuile:
    
    TYPE_TERRE ="0"
    TYPE_EAU ="~"
    TYPE_FEUX ="*"
    TYPE_MUR ="#"

    def __init__(self,type):
        self.type : str = type

    



plat = Tuile.TYPE_FEUX
droit = Tuile(Tuile.TYPE_EAU)


print(plat)


