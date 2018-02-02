#!/usr/bin/env python3

import sys
import os

class Args(object):
    def __init__(self):
        self.args = sys.argv[1:]
        if len(sys.argv) != 7:
            print('Param Error')
            sys.exit(1)
        if not '-c' in sys.argv or not '-d' in sys.argv or not '-o' in sys.argv:
            print('Param Error')
            sys.exit(1)
    def get_args(self):
        c_index = self.args.index('-c')
        configfile = self.args[c_index+1]
        d_index = self.args.index('-d')
        userdatafile = self.args[d_index+1]
        o_index = self.args.index('-o')
        gongzicsv = self.args[o_index+1]
        for filename in configfile,userdatafile:
            if not os.path.exists(filename):
                print('Param Error')
                sys.exit(1)
        return configfile,userdatafile,gongzicsv


class Config(object):
    def __init__(self, configfile):
        self.config = self._read_config(configfile)
    def _read_config(self, configfilename):
        config = {}
        with open(configfilename) as file:
            for line in file:
                try:
                    sbname = line.split('=')[0].strip()
                    sbvalue = line.split('=')[1].strip()
                    config[sbname] = sbvalue
                except Exception, e:
                    print(e)
                    sys.exit(1)
        return config
    def get_config(self, sbname):
        return self.config[sbname]


class UserData(object):
    def __init__(self, userdatafile):
        self.userdata = self._read_user_data(userdatafile)
    def _read_users_data(self, userdatafile):
        userdata = []
        with open(userdatafile) as file:
            for line in file:
                try:
                    gonghao = line.split(',')[0]            
                    gongzi = line.split(',')[1]
                except Exception,e:
                    print(e)
                    sys.exit(1)
                gz = (gonghao,gongzi)
                userdata.append(gz)
        return userdata


class IncomeTaxCalculator(object):
    def calc_for_all_userdata(self):
        


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
