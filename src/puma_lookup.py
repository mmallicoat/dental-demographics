# See: https://gis.stackexchange.com/questions/208546/check-if-a-point-falls-within-a-multipolygon-with-python

from shapely.geometry import Polygon, Point
import fiona
import json
import os
import sys
import pdb

    # TODO
    # Read in dentist_loc.json
    # For each record, run through polygons and check if interior
    # (Need to check Missouri PUMAs, too)
    # If found, add puma code to the dictionary
    # At end, write out modified json file
    
def main(argv):

    datadir = os.path.abspath(argv[1])
    outdir = os.path.abspath(argv[2])

    ks_shp = os.path.join(datadir, 'cb_2016_20_puma10_500k', 'cb_2016_20_puma10_500k.shp')
    mo_shp = os.path.join(datadir, 'cb_2016_29_puma10_500k', 'cb_2016_29_puma10_500k.shp')
    locfile = os.path.join(datadir, 'dentist_loc.json')
    outfile = os.path.join(outdir, 'dentist_loc.json')

    # Read in files
    locs = json.load(open(locfile, 'r'))
    ks_shape = fiona.open(ks_shp)
    mo_shape = fiona.open(mo_shp)

    # Prepare polygon objects for PUMAs
    pumas = list()

    # value['geometry'] is a dictionary
    # value['geometry']['coordinates'] is a list of list of tuples
    for value in ks_shape.values():
        # TODO: need state code, too
        polygon = Polygon(value['geometry']['coordinates'][0])
        pumas.append({'polygon': polygon,
                      'state_code': value['properties']['STATEFP10'],
                      'puma_code': value['properties']['PUMACE10'],
                     })
    for value in mo_shape.values():
        polygon = Polygon(value['geometry']['coordinates'][0])
        pumas.append({'polygon': polygon,
                      'state_code': value['properties']['STATEFP10'],
                      'puma_code': value['properties']['PUMACE10'],
                     })

    # Assign PUMAs to each location
    for loc in locs:
        if 'lat' not in loc.keys() or 'lon' not in loc.keys():
            # lat and long are not available for the location
            loc['state_code'] = 'NA'
            loc['puma_code'] = 'NA'
        else:
            # search for lat and long in PUMAs
            point = Point(float(loc['lon']), float(loc['lat']))
            for puma in pumas:
                if puma['polygon'].contains(point):
                    loc['state_code'] = puma['state_code']
                    loc['puma_code'] = puma['puma_code']
        # NOTE: There is an edge case where the location has lat and long
        #       but is not found in any PUMA in KS or MO.
        
    # Write out modified location file
    json.dump(locs, open(outfile, 'w'))
    
if __name__ == '__main__':
    main(sys.argv)
