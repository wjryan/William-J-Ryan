#!/usr/bin/env python2.7





print('=====')
print('Importing Modules')
print('=====')

#Begin by importing all python modules needed for the analyses to run.
import os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from fermipy.gtanalysis import GTAnalysis
from fermipy.plotting import ROIPlotter, SEDPlotter
from astropy.table import Table, Column
import astropy.io.fits as pyfits
import yaml

#This argument tweaks matplotlib.pyplot so it functions correctly with fermipy.
plt.switch_backend('agg')

print('=====')
print('Finished Importing Modules')
print('=====')





print('=====')
print('Config Loading')
print('=====')

#Now, the configuration file and all its initial parameters are loaded in to the program.
#Heads up, many of these configuration parameters can also be changed using this script.
config = yaml.load(open('config.yaml'))
SOURCE = config['selection']['target']
DIR = config['fileio']['outdir']
LCDIR = config['lightcurve']['outdir']

print('=====')
print('Config Loaded')
print('=====')





print('=====')
print('Performing Setup')
print('=====')

#The loaded parameters are now read and used to setup a number of files formatted
# such that calculations are quicker later on.
gta = GTAnalysis('config.yaml', logging={'verbosity':3})
matplotlib.interactive(True)
gta.setup()

print('=====')
print('Setup Finished')
print('=====')





print('=====')
print('Optimizing')
print('=====')

#The optimize function performs a quick SED fit so the TS can be calculated for each source
# in the field of view.
#The TS (Test Statistic) is used by a number of subsequent commands to tailor the analyses.
gta.optimize()

print('=====')
print('Finished Optimizing')
print('=====')





print('=====')
print('Freezing all sources with significance less than 9 TS and Printing information')
print('=====')

#For those sources with low significance, and hence low TS, the gta.free_sources command
# will freeze those sources with TS outside the designated boundaries. I have set the
# lower bound at 9 TS (~3 standard deviations) and the upper bound arbitrarily high so
# only those sources with TS<9 are frozen in the fit. This will constrain the fit and
# usually produce more reasonable SEDs. I also print some information to the screen
# so I know what information the program starts with.
gta.print_model()
print(gta.roi[SOURCE])
gta.free_sources(minmax_ts = [9,1600000])

print('=====')
print('Finished freezing sources and Printing information')
print('=====')





print('=====')
print('Printing information to screen to make sure the sources were frozen/freed correctly')
print('=====')

print('_____________________________________________')
print('=====')
gta.print_model()
print('=====')
gta.print_params(allpars=True)
print('=====')
gta.print_roi()
print('_____________________________________________')

print('=====')
print('Finished sanity check')
print('=====')





print('=====')
print('Preliminary fit to make preliminary plots')
print('=====')

#Here we do a preliminary fit without any input parameters
fit_results = gta.fit()
gta.print_model()
print(gta.roi[SOURCE])
tsmap = gta.tsmap(prefix='TSmap', make_plots=True)
resid = gta.residmap('Residuals',make_plots=True)
gta.residmap(prefix = 'weighted_residuals', make_plots = True, use_weights = True)

print('=====')
print('Done with preliminary fit and plots')
print('=====')





print('=====')
print('Printing info to the screen for another sanity check')
print('=====')

print('_____________________________________________')
print('=====')
gta.print_model()
print('=====')
gta.print_params(allpars=True)
print('=====')
gta.print_roi()
print('_____________________________________________')

print('=====')
print('Finished another sanity check')
print('=====')





print('=====')
print('Starting the SED fit')
print('=====')

#Here, the SOURCE is the name of the source in question, as defined in the loading
# of the configuration file. The prefix attribute lets you set the prefix name of all
# output files of the SED fitting process. The gta.write_roi() function saves the
# state of the analysis so you can later load it and continue with a subsequent analysis,
# like a light-curve, without having to manually input parameters or redoing the analysis.
#Specific parameters can be defined, frozen, or freed here as well. For more analysis
# options visit https://fermipy.readthedocs.io/en/latest/fermipy.html#fermipy-gtanalysis-module

sed = gta.sed(SOURCE,prefix='SED_fit', use_local_index = True, free_background = True, cov_scale = None)
gta.write_roi('save_analysis_state', make_plots=True,save_model_map=True)

print('=====')
print('SED fit finished')
print('=====')




#=================================================================================
#Stop here if you do not want to make a light-curve
#=================================================================================





print('=====')
print('Starting the light-curve fit')
print('=====')

print('=====')
print('light-curve fit finished')
print('=====')
