#!/usr/bin/env python2.7



print('=====')
print('Importing modules')
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
print('Finished importing Modules')
print('=====')



# Loading the configuration file and making a variable
config = yaml.load(open('config.yaml'))
SOURCE = config['selection']['target']
DIR = config['fileio']['outdir']
LCDIR = config['lightcurve']['outdir']



print('=====')
print('Config Loaded')
print('=====')
print('=====')
print('Performing setup')
print('=====')



#Reading in the config.yaml and beginning the Fermi Analysis
gta = GTAnalysis('config.yaml', logging={'verbosity':3})
matplotlib.interactive(True)
gta.setup()



print('=====')
print('Freeing all sources with consequential significance')
print('And printing some information')
print('=====')

gta.print_model()
print(gta.roi[SOURCE])

gta.free_sources(minmax_ts = [9,1600000])
gta.optimize()

print('_____________________________________________')
print('-----')
gta.print_model()
print('=====')
gta.print_params(allpars=True)
print('=====')
gta.print_roi()
print('_____________________________________________')

print('=====')
print('Fit_results and plots')
print('=====')



fit_results = gta.fit()
gta.print_model()
print(gta.roi[SOURCE])
gta.write_roi('roi_1',save_model_map=True)

print('_____________________________________________')
print('Now to make a TSmap and residual map')
tsmap = gta.tsmap(prefix='TSmap', make_plots=True)
resid = gta.residmap('Residuals',make_plots=True)
print('_____________________________________________')

print('Printing info to the screen again')
print('_____________________________________________')
gta.print_model()
print('_____________________________________________')
gta.print_params(allpars=True)
print('_____________________________________________')
gta.print_roi()
print('_____________________________________________')


gta.residmap(prefix = 'weighted_residuals', make_plots = True, use_weights = True)



print('=====')
print('Starting SED')
print('=====')

#SED
'''
All the hard work has been done already. This will still take some
time to compute because it will peform the analysis with the
sources that were freed for the fitting. Go get some tea.....
'''

sed = gta.sed(SOURCE,prefix='SED_fit', use_local_index = True, free_background = True, cov_scale = None)
gta.write_roi('roi_2', make_plots=True,save_model_map=True)

print('=====')
print('SED finished')
print('=====')


print('End of SED')
