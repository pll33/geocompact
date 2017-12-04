'''

Polsby-Popper
    A ratio of the area of the district to the area of a circle whose
    circumference is equal to the perimeter of the district [1]

    Formula: ratio = 4pi * A_district/(P_district^2)

'''

import math


def polsbypopper(polygon_perimeter, polygon_area):
    return (math.pi * 4 * polygon_area) / math.pow(polygon_perimeter, 2)
