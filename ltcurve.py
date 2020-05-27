#!/usr/bin/env python2.7


#LIGHTCURVE
#PART I: IMPORTING MODULES



print('=====')
print('PART I: IMPORTING MODULES')
print('=====')

#Importing the needed modules
import os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from fermipy.gtanalysis import GTAnalysis
from fermipy.plotting import ROIPlotter, SEDPlotter
from astropy.table import Table, Column
import astropy.io.fits as pyfits
import yaml 

#This makes matplotlib.pyplot function correctly.
plt.switch_backend('agg')

print('=====')
print('PART I: FINISHED')
print('=====')

print('=====')
print('PART II: CONFIGURATION FILES, SETUP, SOURCE INFORMATION')
print('=====')



#PART II: CONFIGURATION FILES, SETUP, SOURCE INFORMATION



# Loading the configuration file and making a variable
config = yaml.load(open('config1.yaml'))
SOURCE = config['selection']['target']
DIR = config['fileio']['outdir']
LCDIR = config['lightcurve']['outdir']

print('Loading in the config.yaml')
print('Preparing to run the analysis for source %s....' % (SOURCE))
print('...............................................')

#Reading in the config.yaml and beginning the Fermi Analysis
gta = GTAnalysis('config1.yaml', logging={'verbosity':3})
matplotlib.interactive(True)
gta.setup()

#Fitting a model to our data
print('----------')
gta.print_model()
print('----------')
print(gta.roi[SOURCE])
print('----------')



print('=====')
print('SETTING PARAMETERS AND FREED SOURCES')
print('=====')



gta.set_parameter('4FGL J1104.4+3812','norm',value = 1.721997147e-11, scale = 1, error = 0.01313677393e-11, update_source = False)
gta.set_parameter_bounds('4FGL J1104.4+3812','norm',[1e-16,1000e-11]) 

gta.set_parameter('4FGL J1104.4+3812','alpha', value = 1.739376675, scale = 1, error =  0.006991402649, update_source = False)
gta.set_parameter('4FGL J1104.4+3812','Eb', value = 1287.365845, scale = 1, update_source = False)
gta.set_parameter('4FGL J1104.4+3812','beta', value = 0.01523674109, scale = 1, error = 0.002518878993, update_source = False)



print('=====')
print('PART II: FINISHED')
print('=====')


#PART III: LIGHT CURVE



print('=====')
print('PART III: LIGHT CURVE')
print('=====')

'''
This is gonna take hella long to complete too! This part of the script
will make a light curve of the data. The plots may come out with the
make_plots paramater, but if it doesn't then there is code to do it anyway.
'''




print('')
print('__________________________________________________')
lc = gta.lightcurve(SOURCE,free_background=False,make_plots=True,shape_ts_threshold = 1000000000)
gta.write_roi(LCDIR+'LightCurve',make_plots=True,save_model_map=True)
print('')



#code for the hand done plots are here
print('Photons for Amy!')
fig = plt.figure(figsize=(8,6))
plt.errorbar((lc['tmin_mjd']+lc['tmax_mjd'])/2., lc['flux'],
             yerr=lc['flux_err'], xerr = (lc['tmin_mjd']-lc['tmax_mjd'])/2., fmt='ko')
plt.ylabel('Phi_{\gamma}$ [ph/cm$^2$/s]', fontsize=18)
plt.xlabel('MJD', fontsize=18)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.grid(True)
plt.legend(loc=1,prop={'size' :16},numpoints=1,scatterpoints=1,ncol=1)
fig.tight_layout(pad=0.5)
plt.savefig(DIR+'/'+LCDIR+'_LightCurve'+'_Photon'+'.png')



print('Energy for Oliver!')
fig2 = plt.figure(figsize=(8,6))
plt.errorbar((lc['tmin_mjd']+lc['tmax_mjd'])/2., lc['eflux'], yerr=lc['eflux_err'], xerr = (lc['tmin_mjd']-lc['tmax_mjd'])/2., fmt='ko')
plt.ylabel('Phi_{\gamma}$ [ph/cm$^2$/s]', fontsize=18)
plt.xlabel('$t$ [s]', fontsize=18)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.grid(True)
plt.legend(loc=1,prop={'size' :16},numpoints=1,scatterpoints=1,ncol=1)
fig.tight_layout(pad=0.5)
plt.savefig(DIR+'/'+LCDIR+'_LightCurve'+'_Energy'+'.png')



print('And another one for Oliver...')
fig3 = plt.figure(figsize=(8,6))
bins = np.linspace(0,500,11)
plt.hist(lc['ts'], bins, color='r', ec='k')
plt.xlabel('TS', fontsize=18)
fig.tight_layout(pad=0.5)
plt.savefig(DIR+'/'+LCDIR+'_LightCurve'+'_TS_Hist'+'.png')



#saving the necessary info in an easy to read table in ascii format
lctab = Table([lc['tmin_mjd'],lc['tmax_mjd'],lc['ts'],lc['flux'],lc['flux_err'],lc['eflux'],lc['eflux_err']])
lctab.write(DIR+'/'+LCDIR+'LightCurve.txt',format='ascii.fixed_width')



#Finally done!!!
print('We are finally done....')
print('Estimated time: ')
print('Enough to watch the complete LOTR and The Hobbit!')

print('=====')
print('PART III: FINISHED')
print('=====')



print('THE END')

