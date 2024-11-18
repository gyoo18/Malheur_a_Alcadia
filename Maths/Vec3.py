from typing_extensions import Self

class Vec3:
    x : float
    y : float
    z : float

    def __init__(self, x = None, y = None, z = None, xyz = 0, vec3 = None):
        if vec3 == None and xyz == None and not (x == None or y == None or z == None) and ((type(x) and type(y) and type(z)) == int or float ):
            self.x = x
            self.y = y
            self.z = z
        elif (x == None or y == None or z == None) and vec3 == None and xyz != None and (type(xyz) == int or float):
            self.x = xyz
            self.y = xyz
            self.z = xyz
        elif (x == None or y == None or z == None) and xyz == None and vec3 != None and type(vec3) == Self:
            self.x = vec3.x
            self.y = vec3.y
            self.z = vec3.z
        elif (x == None or y == None or z == None) and xyz == None and vec3 == None:
            self.x = 0
            self.y = 0
            self.z = 0
        else:
            raise ValueError("Les paramètre d'entrés de Vec3 ne sont pas valides")
        
    def copie(self):
        return Vec3(vec3=self)
    
    