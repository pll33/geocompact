'''

Reock
    A ratio of the area of the district to the area of the minimum bounding
    circle that encloses the district's geometry [1]

    Formula: A/(Area of MinimumBoundingCircle)

'''

import math
import lib


def reock(polygon_area, polygon_pts):
    circle_cx, circle_cy, radius = lib.make_circle(polygon_pts)
    circle_area = math.pi * math.pow(radius, 2)

    return polygon_area / circle_area
