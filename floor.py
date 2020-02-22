import matplotlib.pyplot as plt
import math as math
from vector import *
from line import *

# Floor is used as a collision surface
class Floor:
    def __init__(self, line):
        self.line = Line(Vector(0,0,0), Vector(0,0,0))
        
        # Make sure the floors start position is always to the left of its end
        if (line.start.x < line.end.x):
            self.line.start = line.start
            self.line.end = line.end
        else:
            self.line.start = line.end
            self.line.end = line.start

        # Slope
        dx = self.line.end.y - self.line.start.y
        dy = self.line.end.x - self.line.start.x
        self.slope = dx / dy
    def Draw(self):
        self.line.Draw()
    def GetUnitNormal(self):
        return self.line.GetUnitNormalLeft()

def IsPointBelowFloor(point, floor):
    # Point x position is between line min and max x values
    if (floor.line.start.x <= point.x and point.x <= floor.line.end.x):
        # Calculate the point where the line cuts y axis
        cut_y_axis = floor.slope * (-floor.line.start.x) + floor.line.start.y
        # Is below slope/line
        if (point.y < floor.slope * point.x + cut_y_axis):
            return True
    return False
