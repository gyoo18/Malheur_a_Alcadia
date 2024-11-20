from typing_extensions import Self

class Vec2:
    x : float
    y : float

    def __init__(self, x = None, y = None, xy = 0, vec2 = None):
        if vec2 == None and xy == 0 and not (x == None or y == None) and ((type(x) and type(y)) == int or float ):
            self.x = x
            self.y = y
        elif (x == None or y == None) and vec2 == None and xy != None and (type(xy) == int or float):
            self.x = xy
            self.y = xy
        elif (x == None or y == None) and xy == None and vec2 != None and type(vec2) == Self:
            self.x = vec2.x
            self.y = vec2.y
        elif (x == None or y == None) and xy == None and vec2 == None:
            self.x = 0
            self.y = 0
        else:
            raise ValueError("Les paramètre d'entrés de Vec3 ne sont pas valides")
        
    def copie(self):
        return Vec2(vec2=self)
    
    