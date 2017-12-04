
import sys
import math
import shapefile
import csv
import us

import methods


def polygon_perimeter_area(polygon_pts):
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
    return perimeter, abs(area)

def fips_lookup_abbr(fips_code):
    return str(us.states.lookup(str(fips_code)).abbr)

def main():
    if (len(sys.argv) == 3):
        shp_file = sys.argv[1]
        dbf_file = sys.argv[2]
    else:
        print 'Please include shp and dbf file in arguments.'
        sys.exit()

    # open shapefile
    sf = shapefile.Reader(shp=open(shp_file, 'rb'), dbf=open(dbf_file, 'rb'))

    '''
    export new shapefile with compactness calculations
    export csv with compactness calculations on all rows/districts
        (fields: state, district, compactness stats)
    '''
    sf_new = shapefile.Writer()
    sf_new.fields = sf.fields[1:] + [
       ['AREA', 'N', '50', 15],
       ['PERIMETER', 'N', '50', 15],
       ['CONVEX_HULL', 'N', '50', 15],
       ['POLSBY_POPPER', 'N', '50', 15],
       ['REOCK', 'N', '50', 15],
       ['SCHWARTZBERG', 'N', '50', 15]
    ]

    # overwrite FROMCOUNTY record size (avoid ShapefileException L995 in shapefile.py)
    sf_new.fields[len(sf.fields)-2] = ['FROMCOUNTY', 'L', 1, 0]

    with open('export/calculations_export.csv', 'wb') as csvfile:
        csv_fields = ['state', 'STATEFP', 'CDFP', 'GEOID', 'NAMELSAD', 'LSAD',
                      'CDSESSN', 'area', 'perimeter', 'convex_hull', 'polsby_popper',
                      'reock', 'schwartzberg']
        csv_new = csv.DictWriter(csvfile, fieldnames=csv_fields)
        csv_new.writeheader()

        '''
        loop through each shape (district)
        make sure each district shapeType == 5 (shapeType == Polgyon
            according to ESRI shapefile technical description)
        '''
        for shapeRec in sf.iterShapeRecords():
            if (shapeRec.shape.shapeType == 5):

                s_perim, s_area = polygon_perimeter_area(shapeRec.shape.points)

                # apply each compactness calculation method
                #      add to shapefile record (district row)
                m_convexhull = methods.convexhull(s_area, shapeRec.shape.points)
                m_polsbypopper = methods.polsbypopper(s_perim, s_area)
                m_reock = methods.reock(s_area, shapeRec.shape.points)
                m_schwartzberg = methods.schwartzberg(s_perim, s_area)

                # create new shapefile record with compactness calculations 
                new_record = shapeRec.record + [
                             s_area, s_perim, m_convexhull, m_polsbypopper,
                             m_reock, m_schwartzberg]

                # write record and polygon shape to shapefile
                sf_new.record(*new_record)
                sf_new.poly(parts=[shapeRec.shape.points])

                # print shapeRec.record[1], s_area, s_perim, m_convexhull, m_polsbypopper, m_reock, m_schwartzberg
                state_abbr = fips_lookup_abbr(shapeRec.record[0])
                print '{0}-{1}\tperimeter: {2}\tarea: {3}'.format(state_abbr, shapeRec.record[1], s_perim, s_area)

                # write to csv
                csv_new.writerow({
                    'state': state_abbr,
                    'STATEFP': shapeRec.record[0],
                    'CDFP': shapeRec.record[1],
                    'GEOID': shapeRec.record[2],
                    'NAMELSAD': shapeRec.record[3],
                    'LSAD': shapeRec.record[4],
                    'CDSESSN': shapeRec.record[5],
                    'area': s_area,
                    'perimeter': s_perim,
                    'convex_hull': m_convexhull,
                    'polsby_popper': m_polsbypopper,
                    'reock': m_reock,
                    'schwartzberg': m_schwartzberg
                })

        print 'Saving export CSV...'
        print 'Saving export shapefiles...'
        sf_new.save('export/compactness_calc')

    sys.exit()

main()