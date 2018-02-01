#!/usr/bin/env python3

import sys

def shebao(wages):
    shebao = wages * (0.08 + 0.02 + 0.005 + 0.06)
    return shebao

def geshui(wages):
    b_wages = wages - shebao(wages) - 3500
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
    return taxes

yuangong = {}
for wageinfo in sys.argv[1:]:
    num = wageinfo.split(':')[0]
    wages = wageinfo.split(':')[1]
    try:
        wages = int(wages)
    except:
        print("Parameter Error")
        sys.exit(1)
    af_wages = wages - shebao(wages) - geshui(wages)
    af_wages = format(af_wages, ".2f")
    yuangong[num] = af_wages

for num, af_wages in yuangong.items():
    re = num + ':' + af_wages
    print(re)
