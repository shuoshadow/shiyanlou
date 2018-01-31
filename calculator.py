#!/usr/bin/env python3

import sys

try:
    wages = int(sys.argv[1])
except:
    print("Parameter Error")
    sys.exit(1)

b_wages = wages - 3500
if b_wages <= 0:
    taxes = 0 
elif b_wages > 0 and b_wages <= 1500:
    taxes = b_wages * 0.03 - 0
elif b_wages > 1500 and b_wages <= 4500:
    taxes = b_wages * 0.1 - 105
elif b_wages > 4500 and b_wages <= 9000:
    taxes = b_wages * 0.2 - 555
elif b_wages > 9000 and b_wages <= 35000:
    taxes = b_wages * 0.25 - 1005
elif b_wages > 35000 and b_wages <= 55000:
    taxes = b_wages * 0.3 - 2755
elif b_wages > 55000 and b_wages <= 80000:
    taxes = b_wages * 0.35 - 5505
elif b_wages > 80000:
    taxes = b_wages * 0.45 - 13505

taxes = format(taxes, ".2f")
print(taxes)
