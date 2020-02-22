import matplotlib.pyplot as plt
import math as math
from vector import *

# Two points in space that form a line
class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    def Draw(self):
        x_list = [self.start.x, self.end.x]
        y_list = [self.start.y, self.end.y]
        plt.plot(x_list, y_list)
    def GetVector(self):
        return GetVectorAtoB(self.start, self.end)
    def GetUnitNormalLeft(self):
        return self.GetVector().GetUnitNormalLeft()
    def GetUnitNormalRight(self):
        return self.GetVector().GetUnitNormalRight()

def GetPointDistanceFromLine(point, line):
    numerator = abs((line.end.x - line.start.x) * (point.y - line.start.y) -
                    (point.x - line.start.x) * (line.end.y - line.start.y))
    denominator = math.sqrt((line.end.x - line.start.x) ** 2 +
                            (line.end.y - line.start.y) ** 2)
    return numerator / denominator
