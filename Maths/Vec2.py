from __future__ import annotations
from math import sqrt

class Vec2:

    def __init__(self, x : float | int | Vec2, y : float = None):
        """__init__ _summary_

        Créé un vecteur 2D

        Args:
            Doit fournir soit x,y, soit xy, soit vec2, soit aucun.

            x (float, int, Vec2, optional): composante x du vecteur, composant x et y du vecteur ou Vec2 à copier. None par défaut.
            y (float, int, optional): composante y du vecteur, si spécifié. None par défaut.

        Raises:
            ValueError: Les paramètres doivent être spécifiés de l'une des manières suivante:
             - Vec2(x : float | int, y : float | int)
             - Vec2(x : float | int)
             - Vec2(x : Vec2)
        """
        self.x : float = 0
        self.y : float = 0
        if (type(x) == float or type(x) == int) and (type(y) == float or type(y) == int):
            self.x = x
            self.y = y
        elif (type(x) == float or type(x) == int) and y == None:
            self.x = x
            self.y = x
        elif type(x) == Vec2 and y == None:
            self.x = x.x
            self.y = x.y
        elif type(x) == None and type(y) == None:
            self.x = 0
            self.y = 0
        else:
            raise ValueError("Les paramètre d'entrés de Vec2 ne sont pas valides")
        
    def copie(self):
        """copie 
        Renvoie une copie du vecteur 

        Returns:
            Vec2 : copie du vecteur
        """
        return Vec2(self)
    
    def __eq__(a : Vec2,b : Vec2):
        if type(b) != Vec2:
            return False
        return a.x == b.x and a.y == b.y
    
    def __neq__(a : Vec2, b : Vec2):
        if type(b) != Vec2:
            return True
        return a.x != b.x or a.y != b.y
    
    def __neg__(a : Vec2):
        return Vec2(-a.x,-a.y)
    
    def __abs__(a : Vec2):
        return Vec2(abs(a.x),abs(a.y))
    
    def __invert__(a : Vec2):
        return Vec2(a.y,a.x)
    
    def distance(self, b : Vec2):
        """distance 
        
        Évalue la distance entre ce vecteur et le vecteur b

        Args:
            b (Vec2): Deuxième vecteur

        Raises:
            TypeError: b doit être Vec2

        Returns:
            float : distance entre self et b
        """
        if type(b) != Vec2:
            raise TypeError("Vec2.distance(b : Vec2) n'accepte pas d'argument de type " + str(type(b)) + ", seulement de type Vec2.")
        return Vec2.distance(self,b)
    
    def __add__(a : Vec2,b):
        if type(b) == Vec2:
            return Vec2(a.x+b.x, a.y+b.y)
        elif type(b) == int or type(b) == float :
            return Vec2(a.x + b, a.y + b)
        else :
            raise TypeError("b doit être de type Vec2, float ou int, pas " + str(type(b)) + ".")
    
    def __sub__(a : Vec2, b : Vec2):
        if type(b) == Vec2:
            return Vec2(a.x-b.x, a.y-b.y)
        elif type(b) == int or type(b) == float :
            return Vec2(a.x - b, a.y - b)
        else :
            raise TypeError("b doit être de type Vec2, float ou int, pas " + str(type(b)) + ".")
    
    def __mul__(a : Vec2, b):
        if type(b) == Vec2:
            return Vec2(a.x*b.x, a.y*b.y)
        elif type(b) == int or type(b) == float :
            return Vec2(a.x * b, a.y * b)
        else :
            raise TypeError("b doit être de type Vec2, float ou int, pas " + str(type(b)) + ".")
    
    def __truediv__(a : Self, b):
        if type(b) == Vec2:
            return Vec2(a.x/b.x, a.y/b.y)
        elif type(b) == int or type(b) == float :
            return Vec2(a.x / b, a.y / b)
        else :
            raise TypeError("b doit être de type Vec2, float ou int, pas " + str(type(b)) + ".")
    
    def __floordiv__(a : Vec2, b):
        if type(b) == Vec2:
            return Vec2(a.x//b.x, a.y//b.y)
        elif type(b) == int or type(b) == float :
            return Vec2(a.x // b, a.y // b)
        else :
            raise TypeError("b doit être de type Vec2, float ou int, pas " + str(type(b)) + ".")
    
    def __matmul__(a : Vec2, b : Vec2):
        """__matmul__ 
        
        Effectue un produit scalaire entre a et b
        S'écrit a@b et effectue l'opération a•b

        Args:
            a (Vec2): Vecteur a
            b (Vec2): Vecteur b

        Raises:
            TypeError: a et b doivent être des Vec2

        Returns:
            float : renvoie a•b
        """
        if type(b) != Vec2:
            raise TypeError("b doit être de type Vec2, pas " + str(type(b)) + ".")
        return a.x*b.x + a.y*b.y
    
    def __mod__(a : Vec2, b):
        if type(b) == Vec2:
            return Vec2(a.x%b.x, a.y%b.y)
        elif type(b) == float or type(b) == int:
            return Vec2(a.x%b, a.y%b)
        else:
            raise TypeError("b doit être de type Vec2, float ou int, pas " + str(type(b)) + ".")
    
    def __pow__(a : Vec2, b : Vec2):
        """__pow__ 
        
        Effectue un produit vectoriel entre a et b et renvoie son module
        S'écrit a**b et effectue ||a^b|| ou ||axb||

        Args:
            a (Vec2): Vecteur a
            b (Vec2): Vecteur b

        Raises:
            TypeError: a et b doivent être Vec2

        Returns:
            float : renvoie ||a^b||
        """
        if type(b) != Vec2:
            raise TypeError("b doit être de type Vec2, pas " + str(type(b)) + ".")
        return a.x*b.y - a.y*b.x
    

    def long(a : Vec2):
        """_long 

        Renvoie le module du vecteur a
        S'écrit long(a) ou a.long() et effectue ||a||

        Args:
            a (Vec2): Vecteur

        Returns:
            float : Renvoie ||a||
        """
        return sqrt(a.x * a.x + a.y * a.y)
    
    def norm(self):
        """norm 

        Normalise le vecteur
        S'écrit a.norm() et effectue (1/||a||)*a

        Returns:
            Vec2 : renvoie (1/||a||)*a
        """
        l = self.len()
        self.x /= l
        self.y /= l
        return self
    
    def __iadd__(self, b : Vec2):
        if type(b) == Vec2:
            self.x += b.x
            self.y += b.y
        elif type(b) == float or type(b) == int:
            self.x += b
            self.y += b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération +=")
    
    def __isub__(self, b : Vec2):
        if type(b) == Vec2:
            self.x -= b.x
            self.y -= b.y
        elif type(b) == float or type(b) == int:
            self.x -= b
            self.y -= b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération -=")
    
    def __imatmul__(self, b : Vec2):
        if type(b) == Vec2:
            self.x @= b.x
            self.y @= b.y
        elif type(b) == float or type(b) == int:
            self.x @= b
            self.y @= b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération @=")

    def __imult__(self, b : Vec2):
        if type(b) == Vec2:
            self.x *= b.x
            self.y *= b.y
        elif type(b) == float or type(b) == int:
            self.x *= b
            self.y *= b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération *=")

    def __itruediv__(self, b : Vec2):
        if type(b) == Vec2:
            self.x /= b.x
            self.y /= b.y
        elif type(b) == float or type(b) == int:
            self.x /= b
            self.y /= b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération /=")
    
    def __ifloordiv__(self, b : Vec2):
        if type(b) == Vec2:
            self.x //= b.x
            self.y //= b.y
        elif type(b) == float or type(b) == int:
            self.x //= b
            self.y //= b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération //=")
    
    def __imod__(self, b : Vec2):
        if type(b) == Vec2:
            self.x %= b.x
            self.y %= b.y
        elif type(b) == float or type(b) == int:
            self.x %= b
            self.y %= b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération %=")
    
    def __ipow__(self, b : Vec2):
        if type(b) == Vec2:
            self.x **= b.x
            self.y **= b.y
        elif type(b) == float or type(b) == int:
            self.x **= b
            self.y **= b
        else:
            raise TypeError("Type " + str(type(b)) + " n'est pas accepté pour l'opération **=")
    
    def norm(a : Vec2):
        """norm 

        Normalise le vecteur a
        S'écrit a.norm() et effectue (1/||a||)*a

        Args:
            a (Vec2) : Vecteur à normaliser

        Returns:
            Vec2 : renvoie (1/||a||)*a
        """
        return a.copie()/a.long()
        
    def distance(a : Vec2, b : Vec2):
        if type(a) != Vec2:
            raise TypeError("Vec2.distance(a : Vec2, b: Vec2) n'accepte pas d'arguement de type a : " + str(type(a)) + ", seulement de type Vec2.")
        if type(b) != Vec2:
            raise TypeError("Vec2.distance(a : Vec2, b: Vec2) n'accepte pas d'arguement de type b : " + str(type(b)) + ", seulement de type Vec2.")
        return sqrt((a.x-b.x)*(a.x-b.x) + (a.y-b.y)*(a.y-b.y))

    def __str__(self):
        return "("+str(self.x)+"; "+str(self.y)+")"
    
    def __repr__(self):
        return str(self)