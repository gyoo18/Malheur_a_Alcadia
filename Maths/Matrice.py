import numpy
from typing_extensions import Self
import copy
import math
from Maths.Vec3 import Vec3

class MROrdre:
    XYZ = 0
    XZY = 1
    YXZ = 2
    YZX = 3
    ZXY = 4
    ZYX = 5

    valeur : int

    def __init__(self,valeur = 0):
        self.valeur = valeur
    
    def obtenirNom(self):
        match self.valeur:
            case self.XYZ:
                return "XYZ"
            case self.XZY:
                return "XZY"
            case self.YXZ:
                return "YXZ"
            case self.YZX:
                return "YZX"
            case self.ZXY:
                return "ZXY"
            case self.ZYX:
                return "ZYX"


class Matrice:
    mat : numpy.array

    def __init__(self, matrice = None):
        if type(matrice) == Self:
            self.mat = copy.deepcopy(matrice.mat)
        elif type(matrice) == list and len(matrice) == 16:
            self.mat = numpy.array(matrice)
        elif matrice == None:
            self.mat = numpy.array([
                1.0, 0.0, 0.0, 0.0,
                0.0, 1.0, 0.0, 0.0,
                0.0, 0.0, 1.0, 0.0,
                0.0, 0.0, 0.0, 1.0
            ])
        elif type(matrice) == list and len(matrice) != 16:
            raise TypeError("Matrice. liste de longueur " + str(len(matrice)) + " n'est pas de longueur 16.")
        else:
            raise TypeError("Matrice ne peut pas interpréter " + str(type(matrice)))
        
    def __mul__(self,mat):
        if type(mat) == Matrice:
            a = mat
            b = self
            mat_v  = [
                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0
            ]
            for i in range(len(mat_v)):
                ax = 0
                ay = i//4
                bx = i%4
                by = 0
                cx = bx
                cy = ay
                mat_v[cx + 4*cy] = (  a.mat[0 + ay*4]*b.mat[bx + 0*4]
                                    + a.mat[1 + ay*4]*b.mat[bx + 1*4] 
                                    + a.mat[2 + ay*4]*b.mat[bx + 2*4] 
                                    + a.mat[3 + ay*4]*b.mat[bx + 3*4])
            return Matrice(mat_v)
        
    def fairePerspective(self, plan_proche : float, plan_loin : float, FOV : float, ratio : float):
        n = plan_proche
        f = plan_loin
        return Matrice([
            1.0, 0.0,   0.0,             0.0,
            0.0, ratio, 0.0,             0.0,
            0.0, 0.0,   2.0/(f-n),       math.tan(FOV*math.pi/180.0),
            0.0, 0.0,  -2.0*n/(f-n)-1.0, 1.0
        ])
    
    def positionner(self, position : Vec3):
        self.mat[12] = position.x
        self.mat[13] = position.y
        self.mat[14] = position.z
        return self

    def translation(self,translation : Vec3):
        self.mat[12] += translation.x
        self.mat[13] += translation.y
        self.mat[14] += translation.z
        return self

    def définirÉchelle(self, échelle : Vec3):
        self.mat[0] = échelle.x
        self.mat[5] = échelle.y
        self.mat[10] = échelle.z
        return self

    def écheloner(self, échelle : Vec3):
        self.mat[0] *= échelle.x
        self.mat[5] *= échelle.y
        self.mat[10] *= échelle.z
        return self

    def obtenirRotation(self, rotation : Vec3, ordre  = MROrdre()):
        from math import cos, sin
        x = rotation.x
        y = rotation.y
        z = rotation.z
        matX = []
        match ordre.valeur:
            case MROrdre.XYZ:
                matX = [
                    cos(y)*cos(z), -sin(x)*sin(y)*cos(z)-cos(x)*sin(z), -cos(x)*sin(y)*cos(z)+sin(x)*sin(z), 0,
                    cos(y)*sin(z), -sin(x)*sin(y)*sin(z)+cos(x)*cos(z), -cos(x)*sin(y)*sin(z)-sin(x)*cos(z), 0,
                    sin(y), sin(x)*cos(y), cos(x)*cos(y), 0,
                    0,0,0,1
                ]
            case MROrdre.XZY:
                matX = [
                    cos(y)*cos(z), -cos(x)*cos(y)*sin(z)-sin(x)*sin(y), sin(x)*cos(y)*sin(z)-cos(x)*sin(y),0,
                    sin(z), cos(x)*cos(z), -sin(x)*cos(z), 0,
                    sin(y)*cos(z), -cos(x)*sin(y)*sin(z)+sin(x)*cos(y), sin(x)*sin(y)*sin(z)+cos(x)*cos(y), 0,
                    0,0,0,1
                ]
            case MROrdre.YXZ:
                matX = [
                    cos(y)*cos(z)+sin(x)*sin(y)*sin(z), -cos(x)*sin(z), -sin(y)*cos(z)+sin(x)*cos(y)*sin(z),0,
                    cos(y)*sin(z)-sin(x)*sin(y)*cos(z), cos(x)*cos(z), -sin(y)*sin(z)-sin(x)*cos(y)*cos(z),0,
                    cos(x)*sin(y), sin(x), cos(x)*cos(y),0,
                    0,0,0,1
                ]
            case MROrdre.YZX:
                matX = [
                    cos(y)*cos(z), -sin(z), -sin(y)*cos(z),0,
                    cos(x)*cos(y)*sin(z)-sin(x)*sin(y), cos(x)*cos(z), -cos(x)*sin(y)*sin(z)-sin(x)*cos(y),0,
                    sin(x)*cos(y)*sin(z)+cos(x)*sin(y), sin(x)*cos(z), -sin(x)*sin(y)*sin(z)+cos(x)*cos(y),0,
                    0,0,0,1
                ]
            case MROrdre.ZXY:
                matX = [
                    cos(y)*cos(z)-sin(x)*sin(y)*sin(z), -cos(y)*sin(z)-sin(x)*sin(y)*cos(z), -cos(x)*sin(y),0,
                    cos(x)*sin(z), cos(x)*cos(z), -sin(x),0,
                    sin(y)*cos(z)+sin(x)*cos(y)*sin(z), -sin(y)*sin(z)+sin(x)*cos(y)*cos(z), cos(x)*cos(y),0,
                    0,0,0,1
                ]
            case MROrdre.ZYX:
                matX = [
                    cos(y)*cos(z), -cos(y)*sin(z), -sin(y),0,
                    cos(x)*sin(z)-sin(x)*sin(y)*cos(z), cos(x)*cos(z)+sin(x)*sin(y)*sin(z), -sin(x)*cos(y),0,
                    sin(x)*sin(z)+cos(x)*sin(y)*cos(z), sin(x)*cos(z)-cos(x)*sin(y)*sin(z), cos(x)*cos(y),0,
                    0,0,0,1
                ]
        return Matrice(matX)
    
    def tourner(self, rotation : Vec3):
        matrice = self.obtenirRotation(rotation)*self
        self.mat = matrice.mat
        return self
