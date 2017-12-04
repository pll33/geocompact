import shapefile

from matplotlib import pyplot
from shapely.geometry import MultiPoint
from shapely.geometry import Polygon

from descartes.patch import PolygonPatch

import math

GM = (math.sqrt(5)-1.0)/2.0
H = 8.0*GM
SIZE = (8.0, H)

fig = pyplot.figure(1, figsize=SIZE, dpi=90)
fig.set_frameon(True)
ax = fig.add_subplot(111)

r = shapefile.Reader("./tl_2017_us_cd115/tl_2017_us_cd115")

pa, ca = 0.0, 0.0
for shapeRec in r.iterShapeRecords():
    poly = Polygon(shapeRec.shape.points)
    hull = Polygon(poly.convex_hull)
    pa = poly.area
    ca = hull.area
    if (pa > ca):
        break

if (pa > ca):

    print('WARNING: found polygon with larger base area than convex hull area')
    print('polygon_area: ', pa, '\tconvex_area: ', ca

    patch_poly = PolygonPatch(poly, facecolor='#999999', edgecolor='#999999', alpha=0.3, zorder=3)
    ax.add_patch(patch_poly)
    patch_hull = PolygonPatch(hull, facecolor='#6699cc', edgecolor='#6699cc', alpha=0.5, zorder=2)
    ax.add_patch(patch_hull)

    ax.set_title('Polygon with greater base area')

    minx, miny, maxx, maxy = hull.bounds

    xrange = [int(math.floor(minx)), int(math.ceil(maxx))]
    yrange = [int(math.floor(miny)), int(math.ceil(maxy))]

    #print minx, miny, maxx, maxy
    #print xrange, yrange

    ax.set_xlim(*xrange)
    ax.set_xticks(range(*xrange) + [xrange[-1]])
    ax.set_ylim(*yrange)
    ax.set_yticks(range(*yrange) + [yrange[-1]])
    ax.set_aspect(1)

    pyplot.show()

else:
    print('no districts found with larger base area than convex hull area')


