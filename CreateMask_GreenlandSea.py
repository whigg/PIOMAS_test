#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 11:44:55 2017

@author: valeria
"""

from struct import unpack
import numpy as np
import glob, os
import matplotlib.pyplot as plt

INDIR = './vars/'

#load lon, lat
fname_grid = INDIR+'grid.dat'
a = np.loadtxt(fname_grid)
b = a.flatten()
np.shape(b)
lon = b[0:43200]
lons = lon.reshape(120,360)
lat = b[43200:]
lats = lat.reshape(120,360)
#load kmt
kmt = np.loadtxt(INDIR+'kmt_test.txt')

#region lims [lat0,lat1,lon0,lon1]
REGION = [66,83,320,25]

GreenlandSea_mask = np.zeros((120,360))
GreenlandSea_mask_kmt = np.zeros((120,360))
for i in range(120):
    for j in range(360):
        if (lats[i,j]>REGION[0] and lats[i,j]<REGION[1]):
            if (lons[i,j]>REGION[2] or lons[i,j]<REGION[3]):
                GreenlandSea_mask[i,j]=1
                if kmt[i,j]>0:
                    GreenlandSea_mask_kmt[i,j]=1
GreenlandSea_mask.dump(INDIR+'GreenlandSea_mask')
GreenlandSea_mask_kmt.dump(INDIR+'GreenlandSea_mask_kmt')
np.savetxt(INDIR+'GreenlandSea_mask.txt',GreenlandSea_mask, fmt ='%i')
np.savetxt(INDIR+'GreenlandSea_mask_kmt.txt',GreenlandSea_mask_kmt, fmt ='%i')

#plot mask    
from mpl_toolkits.basemap import Basemap

plt.figure()
m = Basemap(projection='npstere',boundinglat=48,lon_0=0,resolution='l')
m.drawcoastlines()

(x, y) = m(lons,lats)

m.pcolormesh(x, y, GreenlandSea_mask+GreenlandSea_mask_kmt)
plt.colorbar()
plt.title('Greenland Sea')
plt.show()
plt.savefig(INDIR+'Greenland Sea mask')