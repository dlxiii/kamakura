# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 16:25:56 2019

@author: Yulong WANG
"""

import pickle
import numpy as np
import pandas as pd
import shapefile as sf
import matplotlib.pyplot as plt

# Choose projection 'wgs84' or 'epsg'
proj = 'wgs84' 

# Input and output file paths
file1 = '../inps/'+ proj +'/d_1.shp'
file2 = '../inps/'+ proj +'/d_2.shp'
house = '../inps/'+ proj +'/h_0.shp'
boxes = '../inps/'+ proj +'/h_0_box.shp'
bound = '../inps/'+ proj +'/boundary.shp'

# Extract shapefile
spf_d1 = sf.Reader(file1)
spf_d2 = sf.Reader(file2)
spf_h0 = sf.Reader(house)
spf_hb = sf.Reader(boxes)
spf_bd = sf.Reader(bound)

# Extract record class from shapefile
rec_d1 = spf_d1.records()
rec_d2 = spf_d2.records()
rec_h0 = spf_h0.records()
rec_hb = spf_hb.records()
rec_bd = spf_bd.records()

# Extract shaperecord class from shapefile
src_d1 = spf_d1.shapeRecords()
src_d2 = spf_d2.shapeRecords()
src_h0 = spf_h0.shapeRecords()
src_hb = spf_hb.shapeRecords()
src_bd = spf_bd.shapeRecords()

fig, ax = plt.subplots()
for sh in spf_hb.shapeRecords():
    x = [i[0] for i in sh.shape.points[:]]
    y = [i[1] for i in sh.shape.points[:]]
    ax.plot(x, y, color='0.25', linewidth=0.5)
for sh in spf_bd.shapeRecords():
    x = [i[0] for i in sh.shape.points[:]]
    y = [i[1] for i in sh.shape.points[:]]
    ax.plot(x, y, '-.', color='red', linewidth=0.5)
ax.set(xlabel='Lon. (deg)', ylabel='Lat. (deg)',
title= str(len(rec_hb)) + ' houses in Sakasagawa area')
my_x_ticks = np.arange(139.550, 139.571, 0.005)
plt.xticks(my_x_ticks)
my_y_ticks = np.arange(35.307, 35.319, 0.003)
plt.yticks(my_y_ticks)
ax.get_xaxis().get_major_formatter().set_useOffset(False)
ax.grid(color='0.75', linewidth=0.25)   
fig.savefig("../otps/fig_house.png", dpi=1200)
plt.show()

fig, ax = plt.subplots()
for sh in spf_d1.shapeRecords():
    x = [i[0] for i in sh.shape.points[:]]
    y = [i[1] for i in sh.shape.points[:]]
    ax.plot(x, y, linewidth=1)
ax.set(xlabel='Lon. (deg)', ylabel='Lat. (deg)',
title= str(len(rec_d1)) + ' level 1 drainage areas in Sakasagawa')
my_x_ticks = np.arange(139.550, 139.571, 0.005)
plt.xticks(my_x_ticks)
my_y_ticks = np.arange(35.307, 35.319, 0.003)
plt.yticks(my_y_ticks)
ax.get_xaxis().get_major_formatter().set_useOffset(False)
ax.grid(color='0.75', linewidth=0.25)   
fig.savefig("../otps/fig_drainage_1.png", dpi=1200)
plt.show()

fig, ax = plt.subplots()
for sh in spf_d2.shapeRecords():
    x = [i[0] for i in sh.shape.points[:]]
    y = [i[1] for i in sh.shape.points[:]]
    ax.plot(x, y, linewidth=1)
ax.set(xlabel='Lon. (deg)', ylabel='Lat. (deg)',
title= str(len(rec_d2)) + ' level 2 drainage areas in Sakasagawa')
my_x_ticks = np.arange(139.550, 139.571, 0.005)
plt.xticks(my_x_ticks)
my_y_ticks = np.arange(35.307, 35.319, 0.003)
plt.yticks(my_y_ticks)
ax.get_xaxis().get_major_formatter().set_useOffset(False)
ax.grid(color='0.75', linewidth=0.25)   
fig.savefig("../otps/fig_drainage_2.png", dpi=1200)
plt.show()

def houseSumInArea(rec_h0, id_area, flag):
    houseSum = 0
    for i in rec_h0:
        if i[flag+1] == id_area:
            houseSum = houseSum + i[1] 
    return round(houseSum,2)

def houseListInArea(rec_h0, id_area, flag):
    houseList = []
    for i in rec_h0:
        if i[flag+1] == id_area:
            houseList.append(i[0])
    return houseList

def houseNumInArea(rec_h0, id_area, flag):
    houseNum = 0
    for i in rec_h0:
        if i[flag+1] == id_area:
            houseNum = houseNum + 1
    return houseNum

def houseInfoStatic(rec_h0, rec_xx):
    idList = [i[0] for i in rec_xx]
    if len(idList) == 46:
        flag = 1
    if len(idList) == 219:
        flag = 2
    outputData = []
    for j in idList:
        houseSum = houseSumInArea(rec_h0, j, flag)
        houseList = houseListInArea(rec_h0, j, flag)
        houseNum = houseNumInArea(rec_h0, j, flag)
        outputData.append([j,houseNum,houseSum,houseList])
    return outputData

for i in [rec_d1,rec_d2]:
    if len(i) == 46: flag = 1
    if len(i) == 219: flag = 2
    print('Information of house statics in level '+ str(flag) +' drainage.')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('%-10s %-12s %-15s' % ('ID','House number','House roof area'))
    for j in houseInfoStatic(rec_h0, i):
        print('%-10.0f %-12.0f %-15.2f' % (j[0],j[1],j[2]))
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    
for i in [rec_d1,rec_d2]:
    if len(i) == 46: flag = 1
    if len(i) == 219: flag = 2
    file = open('../otps/houseInfoStatic_'+ str(flag) +'.txt', 'w+')
    file.write('Information of house stactics in level '+ str(flag) +' drainage' + '\n')
    file.write('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%' + '\n')
    file.write('%-10s %-12s %-15s' % ('ID','House number','House roof area') + '\n')
    for j in houseInfoStatic(rec_h0, i):
        file.write('%-10.0f %-12.0f %-15.2f' % (j[0],j[1],j[2]) + '\n')
    file.write('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%' + '\n')
    file.close()
    
for i in [rec_d1,rec_d2]:
    if len(i) == 46: flag = 1
    if len(i) == 219: flag = 2
    df = pd.DataFrame({'ID':[], 'House number':[], 'House roof area':[], 'House ID':[]})
    list_0 = []
    list_1 = []
    list_2 = []
    list_3 = []
    for j in houseInfoStatic(rec_h0, i):
        list_0.append(j[0])
        list_1.append(j[1])
        list_2.append(j[2])
        list_3.append(j[3])
    df['ID'] = list_0
    df['House number'] = list_1
    df['House roof area'] = list_2
    df['House ID'] = list_3
    pickle.dump(df, open('../otps/houseInfoStatic_'+str(flag)+'.data', mode = 'wb'), protocol = True)