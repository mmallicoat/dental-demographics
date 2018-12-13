import pandas as pd
import json
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
    # Convert codes in integers
    convert = lambda x: x if x == 'NA' else int(x)
    df.state_code = df.state_code.apply(convert)
    df.puma_code = df.puma_code.apply(convert)

    # Aggregate by state and PUMA
    group_vars = ['state_code', 'puma_code']
    measure = ['practice_name']
    df_grouped = df.groupby(group_vars)[measure].count()

    # Format and write out results
    df_grouped.columns = ['Practice Count']
    df_grouped.to_csv(outfile, index_label=['State', 'PUMA'])

if __name__ == '__main__':
    main(sys.argv)



