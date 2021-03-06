#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 13:56:10 2018

@author: valeria
"""
import numpy as np
#import matplotlib
#matplotlib.use('Agg')
from matplotlib import pyplot as plt
import datetime
from scipy import stats
import sys
sys.path.append('/home/valeria/NIERSC/Scripts/IceVolume/PIOMAS_test/functions/')
import Vi_functions as V

def bias_Vi(model,obs):
    n = len(model)
    b = obs-model
#    for i in range(len(dataset1)):
#        b[i]=dataset1[i]-dataset2[i]read_PIOMAS_Vi_flux()
    bias = np.sum(b)/n
    return bias

def rmse_Vi(model,obs):
    n = len(model)
    r = np.zeros((n))
    for i in range(len(model)):
        r[i]=np.sqrt((obs[i]-model[i])**2)
    rmse = np.sum(r/n)
    return rmse

def rpd_Vi(model,obs):
    n = len(model)
    dif = obs-model
    rdif = dif/model
    rdif_sum = np.sum(rdif)
    rpd = rdif_sum/n
    return rpd*100

def P_Cr_monthly_stats(function_name,months_winter):
    stat_param = np.zeros((len(months_winter)))
    no_data_2010_cr = np.array([10,1,2,3,4])
    fname_PIOMAS = INDIR+'PIOMAS_vol_export.txt'
    fname_Cryosat = INDIR+'CRYOSAT_vol_export.txt'
    outname = OUTDIR+'temp.txt'
    Vif_PIOMAS, dates_PIOMAS = V.read_PIOMAS_Vi_flux(fname_PIOMAS)
    Vif_Cr, dates_Cr = V.read_Cryosat_Vi_flux(fname_Cryosat)
    years_Cr = np.arange(2010,2017,1)
    monthly_Vif_PIOMAS, mean_monthly_Vif_PIOMAS, std_monthly_Vif_PIOMAS = V.calculate_monthly_stats_Vif(years_Cr, months_winter, Vif_PIOMAS, dates_PIOMAS, outname)
    monthly_Vif_Cr, mean_monthly_Vif_Cr, std_monthly_Vif_Cr = V.calculate_monthly_stats_Vif(years_Cr, months_winter, Vif_Cr, dates_Cr, outname)
    for m in range(len(months_winter)):
        d1 = monthly_Vif_PIOMAS[m]
        d2 = monthly_Vif_Cr[m]
        if months_winter[m] in no_data_2010_cr:
            d1=d1[1:]
        stat_param[m] = function_name(d1,d2)
    return stat_param

def P_K04_monthly_stats(function_name, months_winter):
    fname_PIOMAS = INDIR+'PIOMAS_vol_export.txt'
    fname_k04=INDIR+'Kwok_vol_export_2004.txt'
    outname = OUTDIR+'temp.txt'
    Vif_PIOMAS, dates_PIOMAS = V.read_PIOMAS_Vi_flux(fname_PIOMAS)
    Vif_k04, dates_k04 = V.read_Kwk_Sprn_Vi_flux(fname_k04)
    years_k04 = np.arange(1991,2000,1)
    monthly_Vif_k04, mean_monthly_Vif_k04, std_monthly_Vif_k04 = V.calculate_monthly_stats_Vif(years_k04, months_winter, Vif_k04, dates_k04, outname)
    monthly_Vif_PIOMAS, mean_monthly_Vif_PIOMAS, std_monthly_Vif_PIOMAS = V.calculate_monthly_stats_Vif(years_k04, months_winter, Vif_PIOMAS, dates_PIOMAS, outname)
    stat_param = np.zeros((len(months_winter)))
    no_data_1991_k04 = np.array([1,2,3,4])
    no_data_1999_k04 = np.array([10,11,12])
    for m in range(len(months_winter)):
        d1 = monthly_Vif_PIOMAS[m]
        d2 = monthly_Vif_k04[m]
        if months_winter[m] in no_data_1991_k04:
            d1=d1[1:]
        if months_winter[m] in no_data_1999_k04:
            d1=d1[:-1]
        stat_param[m] = function_name(d1,d2)
    return stat_param

def P_S09_monthly_stats(function_name, months_winter):
    fname_PIOMAS = INDIR+'PIOMAS_vol_export.txt'
    fname_s09=INDIR+'Spreen_vol_export_2009.txt'
    outname = OUTDIR+'temp.txt'
    Vif_PIOMAS, dates_PIOMAS = V.read_PIOMAS_Vi_flux(fname_PIOMAS)
    Vif_s09, dates_s09 = V.read_Kwk_Sprn_Vi_flux(fname_s09)
    years_s09 = np.arange(2003,2009,1)
    monthly_Vif_s09, mean_monthly_Vif_s09, std_monthly_Vif_s09 = V.calculate_monthly_stats_Vif(years_s09, months_winter, Vif_s09, dates_s09, outname)
    monthly_Vif_PIOMAS, mean_monthly_Vif_PIOMAS, std_monthly_Vif_PIOMAS = V.calculate_monthly_stats_Vif(years_s09, months_winter, Vif_PIOMAS, dates_PIOMAS, outname)
    stat_param = np.zeros((len(months_winter)))    
    no_data_2008_s09 = np.array([10,11,12])
    for m in range(len(months_winter)):
        d1 = monthly_Vif_PIOMAS[m]
        d2 = monthly_Vif_s09[m]
        if months_winter[m] in no_data_2008_s09:
            d1=d1[:-1]
        stat_param[m] = function_name(d1,d2)
    return stat_param

        
INDIR = '/home/valeria/NIERSC/Projects/Bashmachnikov/data/PIOMAS/'
OUTDIR = '/home/valeria/NIERSC/Scripts/IceVolume/PIOMAS_test/Comparison_obs/'
months_winter = np.array([10,11,12,1,2,3,4])
months_dc = np.array([1,2,3,4])

##PIOMAS vs Cryosat
bias_cr = P_Cr_monthly_stats(bias_Vi, months_winter)
rmse_cr = P_Cr_monthly_stats(rmse_Vi, months_winter)
rpd_cr = P_Cr_monthly_stats(rpd_Vi, months_winter)
    
##PIOMAS vs Kwok 
bias_k04 = P_K04_monthly_stats(bias_Vi, months_winter)
rmse_k04 = P_K04_monthly_stats(rmse_Vi, months_winter)
rpd_k04 = P_K04_monthly_stats(rpd_Vi, months_winter)

###PIOMAS vs Spreen
bias_s09 = P_S09_monthly_stats(bias_Vi, months_winter)
rmse_s09 = P_S09_monthly_stats(rmse_Vi, months_winter)
rpd_s09 = P_S09_monthly_stats(rpd_Vi, months_winter)


#
plt.figure()
plt.plot(range(len(months_winter)),bias_cr,  'o', markersize=8,  markeredgecolor = 'darkorange', markerfacecolor = 'orange', label = 'Cryosat2/SMOS')
plt.plot(range(len(months_winter)),bias_k04, 'd',  markersize=9,  markeredgecolor = 'orchid', markerfacecolor = 'plum', label = 'Kwok2004')
plt.plot(range(len(months_winter)),bias_s09, 's',  markersize=8,  markeredgecolor = 'mediumseagreen', markerfacecolor = 'mediumspringgreen', label = 'Kwok2004')    
plt.xticks(np.arange(len(months_winter)),[str(m) for m in months_winter])
plt.ylim((-10,180))
plt.xlabel('Months')
plt.ylabel('Bias, km^3')
plt.title('Bias, Obs-PIOMAS')
plt.grid()
plt.tight_layout()
plt.legend()
plt.show()
plt.savefig(OUTDIR+'figs/'+'PIOMAS_Viflux_bias.pdf')

plt.figure()
plt.plot(range(len(months_winter)),rmse_cr,  'o', markersize=8,  markeredgecolor = 'darkorange', markerfacecolor = 'orange', label = 'Cryosat2/SMOS')
plt.plot(range(len(months_winter)),rmse_k04, 'd',  markersize=9,  markeredgecolor = 'orchid', markerfacecolor = 'plum', label = 'Kwok2004')
plt.plot(range(len(months_winter)),rmse_s09, 's',  markersize=8,  markeredgecolor = 'mediumseagreen', markerfacecolor = 'mediumspringgreen', label = 'Kwok2004')    
plt.xticks(np.arange(len(months_winter)),[str(m) for m in months_winter])
plt.ylim((-10,180))
plt.xlabel('Months')
plt.ylabel('RMSE, km^3')
plt.title('RMSE, Obs-PIOMAS')
plt.grid()
plt.tight_layout()
plt.legend()
plt.show()
plt.savefig(OUTDIR+'figs/'+'PIOMAS_Viflux_rmse.pdf')

plt.figure()
plt.plot(range(len(months_winter)),rpd_cr,  'o', markersize=8,  markeredgecolor = 'darkorange', markerfacecolor = 'orange', label = 'Cryosat2/SMOS')
plt.plot(range(len(months_winter)),rpd_k04, 'd',  markersize=9,  markeredgecolor = 'orchid', markerfacecolor = 'plum', label = 'Kwok2004')
plt.plot(range(len(months_winter)),rpd_s09, 's',  markersize=8,  markeredgecolor = 'mediumseagreen', markerfacecolor = 'mediumspringgreen', label = 'Spreen2009')    
plt.xticks(np.arange(len(months_winter)),[str(m) for m in months_winter])
#plt.ylim((-10,210))
plt.xlabel('Months')
plt.ylabel('RPD, %')
plt.title('RPD, Obs-PIOMAS')
plt.grid()
plt.tight_layout()
plt.legend()
plt.show()
plt.savefig(OUTDIR+'figs/'+'PIOMAS_Viflux_rpd.pdf')

