#!/usr/bin/env python3

import sys
import os
import csv

class Args(object):
    def __init__(self):
        self.args = sys.argv[1:]
        if len(sys.argv) != 7:
            print('Param1 Error')
            sys.exit(1)
        if not '-c' in sys.argv or not '-d' in sys.argv or not '-o' in sys.argv:
            print('Param2 Error')
            sys.exit(1)

    def get_args(self):
        c_index = self.args.index('-c')
        configfile = self.args[c_index+1]
        d_index = self.args.index('-d')
        userdatafile = self.args[d_index+1]
        o_index = self.args.index('-o')
        gongzicsv = self.args[o_index+1]
        for filename in configfile,userdatafile,gongzicsv:
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
                except Exception as e:
                    print(e)
                    sys.exit(1)
        return config
    def get_config(self, sbname):
        config_data = self.config[sbname]
        config_data = float(config_data)
        return config_data 


class UserData(object):
    def __init__(self, userdatafile):
        self.userdata = self._read_users_data(userdatafile)

    def _read_users_data(self, userdatafile):
        userdata = []
        with open(userdatafile) as file:
            for line in file:
                try:
                    gonghao = line.split(',')[0]            
                    gongzi = line.split(',')[1]
                    gongzi = float(gongzi)
                except Exception as e:
                    print(e)
                    sys.exit(1)
                gz = (gonghao,gongzi)
                userdata.append(gz)
        return userdata
    #sbh shebaohe

    def calculator(self, sbh, JiShuL, JiShuH):
        userdata = self.userdata
        gzlist = []
        for user in userdata:
            userid = user[0]
            userwages = int(user[1])
            jishu = userwages
            if jishu < JiShuL:
                jishu = JiShuL
            if jishu > JiShuH:
                jishu = JiShuH
            shebao = jishu * sbh
            geshui = self.geshui(userwages, shebao)
            afwages = userwages - shebao - geshui
            afwages = format(afwages, ".2f")
            geshui = format(geshui, ".2f")
            shebao = format(shebao, ".2f")
            gzinfo = (userid, userwages, shebao, geshui, afwages)
            gzlist.append(gzinfo)
        return gzlist

    def export(self, gzlist, gongzicsv):
        with open(gongzicsv, 'w') as file:
            writer = csv.writer(file, dialect='excel')
            for line in gzlist:
                #line = list(line)
                #line = list(map(lambda x:[x],line))
                #for info in line:
                #    writer.writerows(info)
                writer.writerow(line) 

    def geshui(self, wages, shebao):
        b_wages = wages - shebao - 3500
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


if __name__ == '__main__':
    args = Args()
    configfile,userdatafile,gongzicsv = args.get_args()
    config = Config(configfile)
    userdata = UserData(userdatafile)
    JiShuL = config.get_config('JiShuL')
    JiShuH = config.get_config('JiShuH')
    YangLao = config.get_config('YangLao')
    YiLiao = config.get_config('YiLiao')
    ShiYe = config.get_config('ShiYe')
    GongShang = config.get_config('GongShang')
    ShengYu = config.get_config('ShengYu')
    GongJiJin = config.get_config('GongJiJin')
    sbh = YangLao + YiLiao + ShiYe + GongShang + ShengYu + GongJiJin
    gzlist = userdata.calculator(sbh, JiShuL, JiShuH)
    print(gzlist)
    export = userdata.export(gzlist, gongzicsv)
