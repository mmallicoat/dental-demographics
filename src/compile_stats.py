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

    # Read in state files, with index fields set
    ks_df = pd.read_csv(ks_file, index_col=['State', 'PUMA'])
    mo_df = pd.read_csv(mo_file, index_col=['State', 'PUMA'])

    # Read in practice file, setting data types of index fields
    pract_df = pd.read_csv(practice_file)
    pract_df.dropna(inplace=True)
    # Pad PUMA code with zeros
    pract_df.PUMA = pract_df.PUMA.apply(lambda x: str(x).zfill(5))
    pract_df.set_index(['State', 'PUMA'], inplace=True)

    # Join statistics by State and PUMA code
    combined_df = pd.concat([ks_df, mo_df], axis=0)
    combined_df = combined_df.join(pract_df, on=['State', 'PUMA'])

    # Add UID
    values = combined_df.index.values
    concat = np.vectorize(lambda x: str(x[0]) + x[1])
    UID = concat(values)
    combined_df['UID'] = UID

    # Write out combined stats
    combined_df.to_csv(os.path.join(outdir, 'combined_stats.csv'))

if __name__ == '__main__':
    main(sys.argv)
