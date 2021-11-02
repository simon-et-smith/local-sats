import numpy as np
import astropy.units as u
import astropy.constants as c
from astropy.io import fits
import matplotlib.pyplot as plt
import pandas as pd
import isochrones as iso
from scipy.signal import find_peaks



############################
# Functions that manipulate isochrones, building towards filter-match fitting
#
#
#
############################



def find_jump(blue_mag, red_mag):
    """
    For a pair of bands, create CMD axes then return the index where a significant jump occurs. Should correspond to the tip of the RGB
    """
    
    color = blue_mag-red_mag
    mag = red_mag
    
    diff = []
    for i in range(1, len(mag)):
        d = np.sqrt((mag[i]-mag[i-1])**2 + (color[i]-color[i-1])**2)
        diff.append(d)
    height = np.std(diff)   
    peak = find_peaks(diff, height=height)
    
    return peak[0][0], diff

