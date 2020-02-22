import matplotlib.pyplot as plt
import matplotlib as matplot
import math as math
import time as time
from vector import *
from line import *
from floor import *
from polygon import *
from collision import *
from constants import *

e = 0.8
tMax = 30
pauseTime = 0.001
drawInterval = 150
axScale = 30

# Create polygons
polygons = []
# TEST 1
polygons.append(Polygon(Vector(30,11,0), [Vector(-3,-3,0),Vector(-3,3,0),Vector(3,3,0),Vector(3,-3,0)], 1, Vector(-15,0,0), 0, 0, 9.6))
polygons.append(Polygon(Vector(-30,10,0), [Vector(-3,-3,0),Vector(-3,3,0),Vector(3,3,0),Vector(3,-3,0)], 1, Vector(15,0,0), 0, 0, 9.6))

# TEST 2
#polygons.append(Polygon(Vector(20,11,0), [Vector(-3,-3,0),Vector(-3,3,0),Vector(3,3,0),Vector(3,-3,0)], 4, Vector(-15,0,0), 0, 0, 38))
#polygons.append(Polygon(Vector(-20,10,0), [Vector(-2,-2,0),Vector(-2,2,0),Vector(2,2,0),Vector(2,-2,0)], 2, Vector(15,0,0), 0, 0, 9))
#polygons.append(Polygon(Vector(0,20,0), [Vector(-3,-3,0),Vector(0,3,0),Vector(3,-3,0)], 3, Vector(0,0,0), 0, 0, 27))

# TEST 3
#polygons.append(Polygon(Vector(20,21,0), [Vector(-3,-3,0),Vector(-3,2,0),Vector(0,5,0),Vector(3,2,0),Vector(3,-3,0)], 5, Vector(-15,0,0), 0, 0, 60))
#polygons.append(Polygon(Vector(-20,20,0), [Vector(-2,-4,0),Vector(-2,4,0),Vector(2,4,0),Vector(2,-4,0)], 5, Vector(15,0,0), 0, -1, 45))
#polygons.append(Polygon(Vector(5,30,0), [Vector(-3,-3,0),Vector(0,3,0),Vector(3,-3,0)], 6, Vector(0,0,0), 0, 3.14, 50))

# Create floors to collide with
floors = []
floors.append(Floor(Line(Vector(0,-12,0), Vector(50,15,0))))
floors.append(Floor(Line(Vector(0,-12,0), Vector(-60,15,0))))

currentTime = 0
loopIteration = 0
while (currentTime < tMax):
    # Collision detection and calculation
    for i in range(len(polygons)):
        for floor in floors:
            CalculatePolygonWithFloorCollision(polygons[i], floor, e)
        for j in range(i + 1, len(polygons)):
            CalculatePolygonCollision(polygons[i], polygons[j], e)

    # Updating polygon transform and speeds            
    for p in polygons:
        p.Update()

    # Drawing 
    if (loopIteration % drawInterval == 0):
        plt.cla()
        plt.axis([-axScale, axScale, -axScale, axScale])
        for p in polygons:
            p.Draw()
        for f in floors:
            f.Draw()
        plt.pause(pauseTime)
            
    loopIteration += 1
    currentTime += dt


