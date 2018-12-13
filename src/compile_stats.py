import pandas as pd
import numpy as np
import os
import sys
import pdb

def main(argv):
    
    datadir = os.path.abspath(argv[1])
    outdir = os.path.abspath(argv[2])

    ks_file = os.path.join(datadir, 'ks_puma_stats.csv')
    mo_file = os.path.join(datadir, 'mo_puma_stats.csv')
    practice_file = os.path.join(datadir, 'practice_stats.csv')
    outfile = os.path.join(outdir, 'combined_stats.csv')

    # Read in state files, with index fields set
    ks_df = pd.read_csv(ks_file, index_col=['State', 'PUMA'])
    mo_df = pd.read_csv(mo_file, index_col=['State', 'PUMA'])
    
    # Read in practice file, setting data types of index fields
    pract_df = pd.read_csv(practice_file)
    pract_df.dropna(inplace=True)
    pract_df.State = pract_df.State.apply(int)
    convert = lambda x: str(int(x))
    pract_df.PUMA = pract_df.PUMA.apply(convert)
    pract_df.set_index(['State', 'PUMA'], inplace=True)

    # Join statistics by State and PUMA code
    state_df = pd.concat([ks_df, mo_df], axis=0)
    combined_df = state_df.join(pract_df, on=['State', 'PUMA'])

    # Write out combined stats
    combined_df.to_csv(outfile)


if __name__ == '__main__':
    main(sys.argv)