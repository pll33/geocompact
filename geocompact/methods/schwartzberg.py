'''

Schwartzberg
    A ratio of the perimeter of the district to the circumference of a circle
    whose area is equal to the area of the district [1]

    Formulas: r = sqrt(A/pi), C_circle = 2pi*r, ratio = 1/(P_district/C_circle)

'''

import math


def schwartzberg(polygon_perimeter, polygon_area):

    r = math.sqrt(polygon_area / math.pi)
    circumference = 2 * r * math.pi

    return circumference / polygon_perimeter
