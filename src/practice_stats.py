import pandas as pd
import numpy as np
import json
import re
import os
import sys
import pdb

def main(argv):
    
    datadir = os.path.abspath(argv[1])
    outdir = os.path.abspath(argv[2])

    locfile = os.path.join(datadir, 'dentist_loc.json')
    outfile = os.path.join(outdir, 'practice_stats.csv')

    # Read in dental practice data from JSON
    locs = json.load(open(locfile, 'r'))
    df = pd.DataFrame.from_dict(locs)

    # Extract information from street address field
    df['street_number'] = np.nan
    df['street_name'] = ''
    df['unit_type'] = ''
    df['unit_id'] = ''
    for i in df.index:
        addr_dict = address_regex(df.loc[i]['street_address'])
        if addr_dict:
            df.at[i, 'street_number'] = addr_dict['street_number']
            df.at[i, 'street_name'] = addr_dict['street_name']
            if 'unit_type' in addr_dict.keys():
                df.at[i, 'unit_type'] = addr_dict['unit_type']
                df.at[i, 'unit_id'] = addr_dict['unit_id']

    # Drop depulicate addresses for counting practices
    keys = ['street_number', 'street_name', 'unit_id', 'zip_code']
    df.drop_duplicates(subset=keys, keep='first', inplace=True)

    # Aggregate by state and PUMA
    group_vars = ['state_code', 'puma_code']
    measure = ['practice_name']
    df_grouped = df.groupby(group_vars)[measure].count()

    # Format and write out results
    df_grouped.columns = ['Practice Count']
    df_grouped.to_csv(outfile, index_label=['State', 'PUMA'])

def address_regex(address):  # takes string, returns dict
    # Two top-level regexes
    addr_plain = re.compile(r'^\W*(\d+)\W+(.*)\W*$')
    addr_unit = re.compile(r'^\W*(\d+)\W+(.*)\W+(STE|Ste|Suite|Apt|#)\W+(\w+)\W*$')
    
    # Beginning of address
    # ^\W*                          Any amount of non-word chars at beginning
    # (\d+)                         Street address digits
    # \W+                           Non-word chars between sections
    # (.*)                          Street name, including any non-word characters
    
    # Optional section for addresses with unit numbers
    # \W+                           Non-word chars between sections
    # (STE|Ste|Suite|Apt|#)         Unit type
    # \W+                           Non-word chars between sections
    # (\w+)                         Unit number/letter (generally "ID")
    
    # Ending section
    # \W*$                          Possible non-word chars at end
    
    addr_dict = dict()
    addr_match = addr_unit.match(address)
    if addr_match:  # address has unit type and number
        addr_set = addr_match.groups()
        addr_dict['street_number'] = addr_set[0]
        addr_dict['street_name'] = addr_set[1]
        addr_dict['unit_type'] = addr_set[2]
        addr_dict['unit_id'] = addr_set[3]
    else:  # try plain format
        addr_match = addr_plain.match(address)
        if addr_match:  # address is plain format
            addr_set = addr_match.groups()
            addr_dict['street_number'] = addr_set[0]
            addr_dict['street_name'] = addr_set[1]
        else:  # regex does not match
            pass

    return addr_dict
        
if __name__ == '__main__':
    main(sys.argv)
