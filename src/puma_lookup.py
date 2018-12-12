# See: https://gis.stackexchange.com/questions/208546/check-if-a-point-falls-within-a-multipolygon-with-python

from shapely.geometry import Polygon, Point
import fiona
import os
import pdb

# TODO: pass shapefile location
datadir = '/Users/user/Code/demographics/data/raw/cb_2016_20_puma10_500k'
filename = 'cb_2016_20_puma10_500k.shp'

shp = os.path.join(datadir, filename)

shape = fiona.open(shp)

# Point in middle of Kansas
# latitude 38 N, longitude 98 W -- but reversed for (x, y) !
point = Point(-98.1, 38.1)
# "lat": "38.971186", "street_address": "12136 W 87th Street Pkwy", "zip_code": "66215"}, {"phone_number": "(913) 888-0403", "city": "Lenexa", "lon": "-94.7249356",
point = Point(-94.7249356, 38.971186 )

# TODO
# Read in dentist_loc.json
# For each record, run through polygons and check if interior
# (Need to check Missouri PUMAs, too)
# If found, add puma code to the dictionary
# At end, write out modified json file

for value in shape.values():
    # value['geometry'] is a dictionary
    # value['geometry']['coordinates'] is a list of list of tuples
    geometry = value['geometry']
    polygon = Polygon(geometry['coordinates'][0])
    if polygon.contains(point):
        puma = value['properties']['PUMACE10']
        name = value['properties']['NAME10']
        print('Point is as %.3f, %.3f' % (point.y, point.x))
        print('Point is in PUMA %s' % puma)
        print(name)

#coordinates = [(0,0), (10, 0), (10, 10), (0, 10)]
#polygon = Polygon(coordinates)
#point = Point(5, 5)
#print(polygon.contains(point))

