import math as math

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.magnitude = math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    def __str__(self):
        return '[' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) + ']'
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar, self.z / scalar)
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
    def GetUnitNormalLeft(self):
        return Vector(-self.y / self.magnitude, self.x / self.magnitude, 0)
    def GetUnitNormalRight(self):
        return Vector(self.y / self.magnitude, -self.x / self.magnitude, 0)

def DotP(a, b):
    return a.x * b.x + a.y * b.y + a.z * b.z

def CrossP(a, b):
    return Vector(a.y * b.z - b.y * a.z,
                  a.z * b.x - b.z * a.x,
                  a.x * b.y - b.x * a.y)

def GetVectorAtoB(a, b):
    return b - a
