# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 18:50:25 2019

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
pont1 = '../inps/'+ proj +'/p_1.shp'
pont2 = '../inps/'+ proj +'/p_2.shp'

# Extract shapefile
spf_d1 = sf.Reader(file1)
spf_d2 = sf.Reader(file2)
spf_h0 = sf.Reader(house)
spf_hb = sf.Reader(boxes)
spf_bd = sf.Reader(bound)
spf_p1 = sf.Reader(pont1)
spf_p2 = sf.Reader(pont2)


# Extract record class from shapefile
rec_d1 = spf_d1.records()
rec_d2 = spf_d2.records()
rec_h0 = spf_h0.records()
rec_hb = spf_hb.records()
rec_bd = spf_bd.records()
rec_p1 = spf_p1.records()
rec_p2 = spf_p2.records()

# Extract shaperecord class from shapefile
src_d1 = spf_d1.shapeRecords()
src_d2 = spf_d2.shapeRecords()
src_h0 = spf_h0.shapeRecords()
src_hb = spf_hb.shapeRecords()
src_bd = spf_bd.shapeRecords()
src_p1 = spf_p1.shapeRecords()
src_p2 = spf_p2.shapeRecords()

for i in [1,2]:
    df_inf = pickle.load(open('../otps/outputCalInfo_'+ str(i) +'.data', mode = "rb"))
    df = df_inf[['ID','Fill perstg','RWH contrbt']]
    df.replace(np.inf, 2, inplace=True)
    
    fig, ax = plt.subplots()
    spf = sf.Reader('../inps/'+ proj +'/d_'+ str(i) +'.shp')
    rec = spf.records()
    for s in range(len(spf.shapeRecords())):
        sh = spf.shapeRecords()[s]
        x = [j[0] for j in sh.shape.points[:]]
        y = [j[1] for j in sh.shape.points[:]]
        c = [k[0] for k in rec]
        b = [str(1 - (df[df['ID'] == l]['Fill perstg'].tolist()[0])) for l in c]
        ax.fill(x, y, linewidth=1, color = s[b], alpha = 0.5)
    ax.set(xlabel='Lon. (deg)', ylabel='Lat. (deg)',
    title= 'Disaster risk in level '+ str(i) +' drainage areas')
    my_x_ticks = np.arange(139.550, 139.571, 0.005)
    plt.xticks(my_x_ticks)
    my_y_ticks = np.arange(35.307, 35.319, 0.003)
    plt.yticks(my_y_ticks)
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.grid(color='0.75', linewidth=0.25)   
    fig.savefig('../otps/fig_disaster_'+ str(i) +'.png', dpi=1200)
    plt.show()
    

