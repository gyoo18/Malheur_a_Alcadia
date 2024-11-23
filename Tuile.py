class Tuiles:
    
    TYPE_TERRE = "0"
    TYPE_EAU ="~"
    TYPE_FEUX ="*"
    type : str
    def __init__(self,type):
        self.type = type

    



plat = Tuiles.TYPE_FEUX

print(plat)


