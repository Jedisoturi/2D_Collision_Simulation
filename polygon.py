import matplotlib.pyplot as plt
import math as math
from vector import *
from line import *
from constants import *

class Polygon:
    def __init__(self, cm, vertices, mass, speed, rotation, omega, rotational_inertia):
        self.m = mass
        self.cm = cm
        self.vertices = vertices
        self.speed = speed
        self.omega = omega
        self.Rotate(rotation)
        self.j = rotational_inertia
        self.collided = False
    def GetVerticesInGlobalSpace(self):
        vertices = []
        for i in range(len(self.vertices)):
            vertices.append(self.GetVertexInGlobalSpace(i))
        return vertices
    def GetVertexInGlobalSpace(self, n):
        return self.cm + self.vertices[n]
    def GetFaceVectors(self):
        faces = []
        for i in range(len(self.vertices)):
            faces.append(self.GetFaceVector(i))
        return faces
    def GetFaceVector(self, n):
        first_vertex = self.vertices[n]
        second_vertex = self.vertices[(n + 1) % len(self.vertices)]
        return GetVectorAtoB(first_vertex, second_vertex)
    def GetFaceLine(self, n):
        line_start = self.GetVertexInGlobalSpace(n)
        line_end = line_start + self.GetFaceVector(n)
        return Line(line_start, line_end)
    def Draw(self):
        x_list = []
        y_list = []
        global_space_vertices = self.GetVerticesInGlobalSpace()
        for v in global_space_vertices:
            x_list.append(v.x)
            y_list.append(v.y)
        x_list.append(global_space_vertices[0].x)
        y_list.append(global_space_vertices[0].y)
        plt.plot(x_list, y_list)
    def Rotate(self, rotation):
        for v in self.vertices:
            x_start = v.x
            y_start = v.y
            v.x = x_start * math.cos(rotation) - y_start * math.sin(rotation)
            v.y = x_start * math.sin(rotation) + y_start * math.cos(rotation)            
    def Update(self):
        # Nopeus
        if (self.collided):
            self.collided = False
        else:
            # Laske painovoiman vaikutus nopeuteen
            self.speed.y = self.speed.y - self.m * g * dt
            #self.speed.y = self.speed.y - 1/2 * 0.8 * self.speed.y ** 2 * dt
            #self.speed.x = self.speed.x - 1/2 * 0.8 * self.speed.x ** 2 * dt
        
        # Rotaatio
        d_rotation = self.omega * dt
        self.Rotate(d_rotation)

        # Paikka
        self.cm = self.cm + self.speed * dt

# Returns the speed of a point, if it were a part of a polygon
def GetVertexSpeed(l_vertex, poly):
    return poly.speed + CrossP(Vector(0,0,poly.omega), l_vertex)
