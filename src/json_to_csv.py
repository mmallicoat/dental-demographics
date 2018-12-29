import pandas as pd
import json
import os
import sys

def main(argv):
    
    infile = os.path.abspath(argv[1])
    outfile = os.path.abspath(argv[2])

    json_file = json.load(open(infile, 'r'))
    df = pd.DataFrame.from_dict(json_file)
    df.to_csv(outfile, index=False)

if __name__ == '__main__':
    main(sys.argv)
