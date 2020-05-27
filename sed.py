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
gta.write_roi('fit_LP', make_plots=True,save_model_map=True)
print('')
print('Once again diagnostic plots and the model map has been made')
print('')
print('Now to make a TSmap and residual map')
tsmap = gta.tsmap(prefix='TSmap_fit_LP', make_plots=True)
resid = gta.residmap('Residuals_fit_LP',make_plots=True)
print('')
print('Now if the following fit attempt fails,')
print('we at least have a place to start....')
print('_____________________________________________')



print('-----')
gta.print_model()
print('=====')
gta.print_params(allpars=True)
print('=====')
gta.print_roi()
print('=====')


gta.residmap(prefix = 'weighted_residuals', make_plots = True, use_weights = True)



print('=====')
print('Starting SED')
print('=====')

#SED
'''
All the hard work has been done already. This will still take a very
long time to compute because it will peform the analysis with the
sources that were freed for the fitting. Go get some tea.....
'''

sed = gta.sed(SOURCE,prefix='SED_fit_LP', bin_index = 1.72304034233, free_background = True, cov_scale = None,free_pars=['norm','alpha','beta'])
#1.739376675

gta.write_roi('SED_fit_LP', make_plots=True,save_model_map=True)

print('=====')
print('SED finished')
print('=====')


print('End of SED')
