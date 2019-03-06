# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 20:19:44 2019

@author: Yulong WANG
"""

import pickle
import pandas as pd

for i in [2]:
    inps = '../inps/inps_'+ str(i) +'.csv'
    df_new = pickle.load(open('../otps/houseInfoStatic_'+ str(i) +'.data', mode = "rb"))
    df_inp = pd.read_csv(inps)
    pickle.dump(df_inp, open('../otps/input.data', mode = 'wb'), protocol = True)  
    df = df_inp.merge(df_new, on = ["ID"], how = "outer")
    df['Fill perstg'] = df['Rainwater'] / df['Capacity']
    df['House water'] = df['House roof area'] * 57.1 / 1000 / 3600
    df['RWH contrbt'] = df['House water'] / df['Rainwater']
    pickle.dump(df, open('../otps/outputCalInfo_'+str(i)+'.data', mode = 'wb'), protocol = True)
    
    file = open('../otps/outputCalInfo_'+ str(i) +'.txt', 'w+')
    file.write('Calculation of level '+ str(i) +' drainage area' + '\n')
    file.write('\n')
    file.write('%-8s %-8s %-8s %-8s %-8s %-8s %-10s %-12s %-12s %-12s %-12s %-12s %-12s'          \
               % ('ID','Inlet 1','Inlet 2','Inlet 3','Outlet','Slope','Rainwater','Capacity','Fill pstg',     \
                  'House num','Roof area','Roof water','RWH ctrbt') + '\n')
    file.write('%-8s %-8s %-8s %-8s %-8s %-8s %-10s %-12s %-12s %-12s %-12s %-12s %-12s'          \
               % ('(-)','(-)','(-)','(-)','(-)','(10^-3)','(m^3/sec)','(m^3/sec)','(-)',     \
                  '(-)','(m^2)','(m^3/sec)','(-)') + '\n')
    for j in range(len(df)):
        file.write(                                                     \
                "{:4.0f}".format(df['ID'].tolist()[j]) +            \
                "{:9.0f}".format(df['Inlet 1'].tolist()[j]) +            \
                "{:9.0f}".format(df['Inlet 2'].tolist()[j]) +            \
                "{:9.0f}".format(df['Inlet 3'].tolist()[j]) +            \
                "{:10.0f}".format(df['Outlet'].tolist()[j]) +           \
                "{:9.1f}".format(df['Slope'].tolist()[j]) +            \
                "{:11.3f}".format(df['Rainwater'].tolist()[j]) +       \
                "{:11.3f}".format(df['Capacity'].tolist()[j]) +        \
                "{:13.0%}".format(df['Fill perstg'].tolist()[j]) +     \
                "{:13.0f}".format(df['House number'].tolist()[j]) +    \
                "{:14.2f}".format(df['House roof area'].tolist()[j]) + \
                "{:13.4f}".format(df['House water'].tolist()[j]) +     \
                "{:13.0%}".format(df['RWH contrbt'].tolist()[j]) +     \
                "\n")
    file.close()