import pandas as pd
import numpy as np
import os
import sys
import pdb

def main(argv):

    exe_dir = os.path.basename(__file__)
    root_dir = os.path.abspath(os.path.join(exe_dir, '..'))
    data_dir = os.path.join(root_dir, 'data', 'ACS')

    # Person Records
    df = pd.read_csv(os.path.join(data_dir, 'csv_pks', 'ss16pks.csv'))

    age_counts = df.groupby('AGEP')['PWGTP'].sum()
    median = median_grouped(age_counts)
    print("Median age is %d" % median)

    stats = std_error(df, ['SEX'])
    print_tup('SEX', stats)

    stats = std_error(df, ['RELP'])
    print_tup('RELP', stats)

    df['AGE_BUCKET'] = df.AGEP.apply(bucket_age)
    stats = std_error(df, ['AGE_BUCKET'])
    print_tup('AGE_BUCKET', stats)

    

# Calculate median from Series of counts in sample
def median_grouped(counts):
    # TODO: add interpolation
    total = counts.sum()
    target = .5 * total
    x = 0
    for ix in counts.index:
        x += counts.loc[ix]
        if x >= target:
            return ix

def bucket_age(age):
    rounded = 5 * int(age / 5)
    if  rounded < 85:
        age_bucket = 'Age %s-%s' % (rounded, rounded + 4)
    else:
        age_bucket = 'Age 85 and over'
    return age_bucket

def print_tup(var, tuples):
    print("%s\t\tMean\t\tStandard Error" % var)
    for tup in tuples:
        print("%s\t\t%.0f\t\t%.0f" % tup)


# Calculate standard error for variable using replicate weights
def std_error(df, group_var):
    rep_cols = ['PWGTP' + str(i) for i in range(1, 81)]
    rep_est = df.groupby(group_var)[rep_cols].sum()
    est = df.groupby(group_var)['PWGTP'].sum()

    # Calculate error of estimate for each level in group_var
    result = []
    for ix in rep_est.index:
        error = 0
        for col in rep_cols:
            # Error for group with value 1 (e.g. males) only
            error += (rep_est[col].loc[ix] - est.loc[ix]) ** 2
        error *= 0.05  # 4 / 80
        se = np.sqrt(error)
        result.append((ix, est.loc[ix], se))

    # Return list of tuples containing level name, mean est., and standard error
    return result
        

if __name__ == '__main__':
    main(sys.argv)
