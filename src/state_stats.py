import pandas as pd
import numpy as np
import os
import sys
import pdb

def main(argv):
    datafile = os.path.abspath(argv[1])  # ACS CSV
    outfile = os.path.abspath(argv[2])
    
    # Person Records of ACS
    df = pd.read_csv(datafile)
    # Inflation-adjust income to 2016 dollars
    df.PINCP = df.PINCP * df.ADJINC * 10 ** -6

    # Calc median household income by PUMA
    group_vars = ['PUMA', 'SERIALNO']
    measures = ['PINCP']
    df_grouped = df.groupby(group_vars)[measures].sum()
    PUMA_levels = df_grouped.index.get_level_values(0)
    median_hhi = df_grouped.groupby(PUMA_levels).median()
    # State level
    group_vars.remove('PUMA')
    df_grouped = df.groupby(group_vars)[measures].sum()
    series = pd.Series({'PINCP': df_grouped.PINCP.median()},
                       name='State')
    median_hhi = median_hhi.append(series)
    # Rename columns
    median_hhi.columns = ['Median Household Income']

    # Calc population by PUMA
    group_vars = ['PUMA']
    measures = ['PWGTP']
    df_grouped = df.groupby(group_vars)[measures].sum()
    # State level
    series = pd.Series({'PWGTP': df_grouped.PWGTP.sum()}, name='State')
    population = df_grouped.append(series)
    # Rename columns
    population.columns = ['Population']


    # Calc median age by PUMA
    # and percent of population at age threshold or older
    threshold = 60
    group_vars = ['PUMA', 'AGEP']
    measures = ['PWGTP']
    df_grouped = df.groupby(group_vars)[measures].sum()
    PUMA_levels = np.unique(df_grouped.index.get_level_values(0))

    median_age = dict()
    old_percent = dict()
    state_total = 0
    for PUMA in PUMA_levels:
        age_counts = df_grouped.loc[PUMA]
        puma_pop = age_counts.sum()
        old_count = age_counts[age_counts.index >= threshold].sum()
        state_total += old_count
        old_percent[PUMA] = float(old_count / puma_pop)
        median_age[PUMA] = median_grouped(age_counts.PWGTP)
    median_age = pd.DataFrame.from_dict(median_age, orient='index',
                                        columns=['Age']).sort_index()
    old_percent = pd.DataFrame.from_dict(old_percent, orient='index',
                                         columns=['Percent']).sort_index()
    # State level
    # Old percent
    state_percent = float(state_total) / df_grouped.PWGTP.sum()
    series = pd.Series({'Percent': state_percent}, name='State')
    old_percent = old_percent.append(series)
    # Median
    group_vars.remove('PUMA')
    df_grouped = df.groupby(group_vars)[measures].sum()
    series = pd.Series({'Age': median_grouped(df_grouped.PWGTP)},
                       name='State')
    median_age = median_age.append(series)

    # Rename columns
    median_age.columns = ['Median Age']
    old_percent.columns = ['Percent Age %s or Older' % threshold]

    # Join results
    stats = pd.concat([population, median_hhi, median_age, old_percent], axis=1)

    # Write out results
    stats.to_csv(outfile, index_label='PUMA')


# Calculate median from Series of counts in sample, with values as index
def median_grouped(counts):
    # TODO: add interpolation
    total = counts.sum()
    target = .5 * np.float(total)  # convert from Series to float
    x = 0
    for ix in counts.index:
        x += counts.loc[ix]
        if x >= target:
            return ix

if __name__ == '__main__':
    main(sys.argv)
