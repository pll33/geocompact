'''

Convex Hull
    A ratio of the area of the district to the area of the minimum convex
    polygon that can enclose the district's geometry [1]

    Formula: A/(Area of MinimumBoundingPolygon)

'''

from scipy.spatial import ConvexHull


def convexhull(polygon_area, polygon_pts):
    # get area of minimum bounding polygon with scipy.spatial.ConvexHull
    # ConvexHull: hull.volume = 2D area, hull.area = 2D perimeter
    hull = ConvexHull(polygon_pts)
    hull_area = hull.volume

    return polygon_area / hull_area
