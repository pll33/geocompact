import math


def area_perimeter(polygon_pts):
    area = 0.0
    perimeter = 0.0

    len_pts = len(polygon_pts)
    if (len_pts > 0):
        if (len_pts % 2 == 1):
            polygon_pts.append(polygon_pts[0])

        for i in range(len_pts):
            pt0 = polygon_pts[i]
            pt1 = polygon_pts[(i+1) % len_pts]
            area += (pt0[0]*pt1[1] - pt0[1]*pt1[0])
            perimeter += math.sqrt(math.pow(pt1[0]-pt0[0], 2) + math.pow(pt1[1]-pt0[1], 2))

        area /= 2
    return abs(area), perimeter
