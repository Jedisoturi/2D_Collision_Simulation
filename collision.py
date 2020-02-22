import matplotlib.pyplot as plt
import math as math
from vector import *
from line import *
from polygon import *
from constants import *
from floor import *

# It is presumed that a polygon is never below a floor.
# Rather it always collides with it from the top.
# This way we always know the orientation of the floor normal.
# Returns a vertex that is in collision with a line. Otherwise returns None.
def GetVertexInCollisionWithFloor(poly, floor):
    g_vertices = poly.GetVerticesInGlobalSpace()
    for g_vertex in g_vertices:
        if (IsPointBelowFloor(g_vertex, floor)):
            l_vertex = GetVectorAtoB(poly.cm, g_vertex)
            vertex_speed = GetVertexSpeed(l_vertex, poly)
            v_dot_n = DotP(vertex_speed, floor.GetUnitNormal())
            if (v_dot_n < 0):
                return l_vertex
    return None

# Calculate a collision with a polygon and a floor
def CalculatePolygonWithFloorCollision(poly, floor, e):
    l_vertex = GetVertexInCollisionWithFloor(poly, floor)

    # If no such vertex is found return without calculating collision
    if (l_vertex == None):
        return
    
    # Impulse formula
    floor_unit_normal = floor.GetUnitNormal()
    v_dot_n = DotP(GetVertexSpeed(l_vertex, poly), floor_unit_normal)
    inv_m = 1 / poly.m
    rp_x_n = CrossP(l_vertex, floor_unit_normal)
    denominator = inv_m + (rp_x_n.magnitude ** 2) / poly.j
    impulse = -(1 + e) * (v_dot_n / denominator)

    # Change polygon speed, rotational speed and flags
    poly.speed = poly.speed + floor_unit_normal * (impulse / poly.m)
    poly.omega = poly.omega + rp_x_n.z * (impulse / poly.j)
    poly.collided = True

# Detects if two polygons are inside each other
def SatDetection(p1, p2):
    # Get faces of both polygons
    faces = p1.GetFaceVectors()
    faces.extend(p2.GetFaceVectors())

    # Create projection normals from the faces
    proj_normals = []
    for face in faces:
        proj_normals.append(face.GetUnitNormalLeft())

    # Get vertices of both polygons
    p1_vertices = p1.GetVerticesInGlobalSpace()
    p2_vertices = p2.GetVerticesInGlobalSpace()

    # Calculate polygon projections for each normal and
    # check that there is overlap on every projection
    for normal in proj_normals:
        # Find the min and max projections of for both polygons
        p1_min = math.inf
        p1_max = -math.inf
        for vertex in p1_vertices:
            proj = DotP(vertex, normal)
            p1_min = min(proj, p1_min)
            p1_max = max(proj, p1_max)
        p2_min = math.inf
        p2_max = -math.inf
        for vertex in p2_vertices:
            proj = DotP(vertex, normal)
            p2_min = min(proj, p2_min)
            p2_max = max(proj, p2_max)

        # If there is no overlap even one projection, there is no collition
        if (p2_max < p1_min or p1_max < p2_min):
            return False

    # If there is overlap on every projection, a collition has happened
    return True

# Returns true if a point in space is inside a polygon
def IsPointInsidePolygon(point, poly):
    for i in range(len(poly.vertices)):
        face = poly.GetFaceVector(i)
        face_start = poly.GetVertexInGlobalSpace(i)
        face_start_to_point = GetVectorAtoB(face_start, point)
        if (0 < CrossP(face, face_start_to_point).z):
            return False
    return True

# Finds and returns a point that is inside a polygon
# p1 is the polygon that has the points and p2 is the polygon we compare
# those points to
def GetCollisionPoint(p1, p2):
    p1_vertices = p1.GetVerticesInGlobalSpace()
    for point in p1_vertices:
        if (IsPointInsidePolygon(point, p2)):
            return point
    return None 

# Finds the closest face to the point and returns the normal of that face
def GetCollisionNormal(point, poly):
    closest_face = poly.GetFaceLine(0)
    closest_face_distance = GetPointDistanceFromLine(point, closest_face)
    for i in range(1, len(poly.vertices)):
        face = poly.GetFaceLine(i)
        face_distance = GetPointDistanceFromLine(point, face)
        if (face_distance < closest_face_distance):
            closest_face = face
            closest_face_distance = face_distance
    return closest_face.GetUnitNormalLeft()

# Calculates a collision between two polygons
def CalculatePolygonCollision(p1, p2, e):
    if (not SatDetection(p1, p2)):
        return

    # Find the collision point and determine which is A and which is B
    poly_a = p1
    poly_b = p2
    point = GetCollisionPoint(p1, p2)
    if (point == None):
        point = GetCollisionPoint(p2, p1)
        poly_a = p2
        poly_b = p1

    # We didn't find a point inside either polygon
    # This seems to happen on point on point collisions
    if (point == None):
        #print("Could not find point inside polygon")
        return
    
    normal = GetCollisionNormal(point, poly_b)

    CalculatePolygonCollisionResults(poly_a, poly_b, point, normal, e)

# Calculates the impulse given collition values
# and assigns new speeds to the polygons that took part in the collition
def CalculatePolygonCollisionResults(poly_a, poly_b, point, normal, e):
    # Get the point's position and speed relative to polygons 
    rAP = GetVectorAtoB(poly_a.cm, point)
    rBP = GetVectorAtoB(poly_b.cm, point)
    vAP = GetVertexSpeed(rAP, poly_a)
    vBP = GetVertexSpeed(rBP, poly_b)

    # Final check that collision has truly happened
    vRel = vAP - vBP
    vRel_Dot_N = DotP(vRel, normal)
    if (0 <= vRel_Dot_N):
        return
    
    # Impulse formula
    inv_m_a = 1 / poly_a.m
    inv_m_b = 1 / poly_b.m   
    rAP_x_n = CrossP(rAP, normal)
    rBP_x_n = CrossP(rBP, normal)
    denominator = inv_m_a + inv_m_b + (rAP_x_n.magnitude ** 2) / poly_a.j + (rBP_x_n.magnitude ** 2) / poly_b.j
    impulse = -(1 + e) * (vRel_Dot_N / denominator)

    # Change the speed, rotational speed and flags of polygons
    poly_a.speed = poly_a.speed + (normal * (impulse / poly_a.m))
    poly_b.speed = poly_b.speed - (normal * (impulse / poly_b.m))
    poly_a.omega = poly_a.omega + rAP_x_n.z * (impulse / poly_a.j)
    poly_b.omega = poly_b.omega - rBP_x_n.z * (impulse / poly_b.j)
    poly_a.collided = True
    poly_b.collided = True
