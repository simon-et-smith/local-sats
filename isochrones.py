import numpy as np
import astropy.units as u
import astropy.constants as c
from astropy.io import fits
import matplotlib.pyplot as plt
import pandas as pd

############################
# Functions that help open and create arrays containing isochrones from text files
#
#
#
############################


def prep_cols(header):
    """
    For the column name row, convert to an array of strings where each is the name of a column
    """
    
    new_header = header.split()[1:]
    new_header[-1] = new_header[-1][:-1]
    return np.array(new_header)

def convert_row_to_data(line):
    """
    For a row in an isochrone txt file, convert the string into an array of floats
    """
    
    strs = line.split()
    strs[-1] = strs[-1][:-1]
    arr = np.array(strs).astype(np.float)
    return arr

def lines_to_data(data_lines):
    """
    For all rows containing data, convert from strings into an (nxm) array prepared for an np.array
    """
    
    data = []
    
    for line in data_lines:
        data.append(convert_row_to_data(line))
        
    return np.array(data)

def lines_to_df(lines):
    """
    Given a list of lines where lines[0] is the column names and lines[1:] is data, create a pandas DataFrame
    """
    
    header_line = lines[0]
    data_lines = lines[1:]
    cols = prep_cols(header_line)
    data = lines_to_data(data_lines)
    iso_df = pd.DataFrame(data, columns=cols)
    
    return iso_df

def find_starts(lines):    
    """
    Find the index number of all rows where a new isochrone starts
    Identifier of header is '# Zini'
    """
    
    starts = []
    i = 0
    for line in lines:
        if '# Zini' in line:
            starts.append(i)
        i+=1
    return starts

def find_isos(lines):
    """
    for a set of lines with isochrone data tables, 
    return a list of triples which represent the index of the header, start of data, and end of data
    for each isochrone data set
    """
    starts = find_starts(lines)
    
    isos = []

    first = True
    for i in range(len(starts)-1, -1, -1):
        if first:
            isos.append([starts[i], starts[i]+1, len(lines)-2])
            first = False
        else:
            isos.append([starts[i], starts[i]+1, starts[i+1]])
    return isos

def lines_to_iso(lines):    
    """
    for all lines in an n isochrone .rtf file, return a numpy array of length n, 
    where each item in a numpy array of size row x column
    also return the header
    """
    
    isochrone = []
    idxs = find_isos(lines)
    header = idxs[0][0]
    for i in idxs:
        isochrone.append(lines_to_data(lines[i[1]:i[2]]))

    return prep_cols(lines[header]), np.array(isochrone)

def open_create(filename):
    """
    create an array of isochrones by passing in the .rtf file name of a downloaded set of isochrones
    also, return the header with the names of all columns
    """
    
    txt = open(filename, 'r')
    lines = txt.readlines()
    
    return lines_to_iso(lines)

def dist_mod(d):
    '''
    for distance d in kpc, return the difference between the absolute and apparent magnitudes
    '''
    
    return 5*np.log10(d*u.kpc/10/u.pc)



