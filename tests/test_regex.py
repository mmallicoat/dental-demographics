import pandas as pd
import re
import pdb

df = pd.read_csv('./docs/address_test_cases.csv')

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

# Two top-level regexes
addr_plain = re.compile(r'^\W*(\d+)\W+(.*)\W*$')
addr_unit = re.compile(r'^\W*(\d+)\W+(.*)\W+(STE|Ste|Suite|Apt|#)\W+(\w+)\W*$')

for i in df.index:
    addr_dict = dict()
    address = df.loc[i].Address
    addr_match = addr_unit.match(address)
    if addr_match:  # address has unit type and number
        addr_set = addr_match.groups()
        addr_dict['number'] = addr_set[0]
        addr_dict['street'] = addr_set[1]
        addr_dict['unit_type'] = addr_set[2]
        addr_dict['unit_id'] = addr_set[3]
    else:  # try plain format
        addr_match = addr_plain.match(address)
        if addr_match:  # address is plain format
            addr_set = addr_match.groups()
            addr_dict['number'] = addr_set[0]
            addr_dict['street'] = addr_set[1]
        else:  # regex does not match
            pass
    print(address)
    print(addr_dict)
    
