#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on Tue Mar  8 19:35:25 2022

@author: spino
Copyright (c) 2022 Valerio Spinogatti
Licensed under GNU license
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack as fttp
from argparse import ArgumentParser



def main():
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Palatino"]
        })
    
    #------------------------------Argument parsing--------------------------------
    p = ArgumentParser(description = 
                       "This script makes a histogram plot from a .csv file with one column.")
    
    p.add_argument("filename", 
                   type = str, 
                   help = "name of the .csv file"
                   )
    p.add_argument("-x", 
                   "--x_label",
                   type = str, 
                   help = "x label"
                   )
    p.add_argument("-y", 
                   "--y_label", 
                   type = str, 
                   help = "y label"
                   )
    p.add_argument("-p", 
                   "--userpath", 
                   type = str, 
                   help = "user specified path"
                   )
    p.add_argument("-m",
                   "--multiplier",
                   type = float,
                   default = 1,
                   help = "data is multiplied by the specified factor.\
                           Default value is 1"
                   )
    
    args = p.parse_args()
    #------------------------------------------------------------------------------
    
    
    #---------------------------Generate file paths-------------------------
    #decide in which path to look for the files (default or user defined)
    if args.userpath is None:
        filepath = "/home/spino/PhD/Lavori/ADC_test/CSV/" #if userpath is not specified then a default path is used 
    else:
        filepath = args.userpath
        
    file = filepath + args.filename
    #------------------------------------------------------------------------------
    
    
    #--------------------------Import list from csv--------------------------------
    try:
        data = args.multiplier * np.genfromtxt(file, delimiter = ",")

        # if data.shape has len greater than 1 it means the array imported from .csv has 2 columns
        # therefore, take only the second column (y values)
        if len(data.shape) > 1:
            data = data[1:,1]
    except OSError:
        print("\nCould not import " + args.filename)
        sys.exit(1)
    #------------------------------------------------------------------------------
     
    
    #------------------------Compute mean and standard dev-------------------------
    datalen = len(data)
    mean = sum(data)/datalen
    squares = [pow((value - mean), 2) for value in data]
    stdev = np.sqrt(sum(squares)/datalen)
    #------------------------------------------------------------------------------
    
    
    #--------------------------Generate histogram and save figure------------------
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    #textstr = f"$\mu={mean}$ \n$\sigma={stdev}$ \n $N_p={datalen}$"
    textstr = '\n'.join((
        r'$\mu=%.2f$' % (mean, ),
        r'$\sigma=%.2f$' % (stdev, ),
        r'$N_{points}=%d$' % (datalen, ),
        r'$Min=%f$' % (np.min(data), ),
        r'$Max=%f$' % (np.max(data), ),
        ))
    
    ax.hist(data)
    ax.text(0.05, 0.95, textstr, transform = ax.transAxes, fontsize = 14,
            verticalalignment = 'top', bbox = props)

    # Save figure
    if args.userpath is None:   
        savepath = "/home/spino/PhD/Lavori/ADC_test/Manoscritti/figures/"
    else:
        savepath = args.userpath[0:-4] + "Manoscritti/figures/"
    figname = args.filename[0:-4] + ".png"
    figurepath = savepath + figname
    
    try:
        fig.savefig(figurepath, dpi = 600)
    except:
        print("Couldn't save figure to specified path. Check savepath and make sure it exists.")

    # Show figure before exiting
    plt.show(block=True)    
    #-----------------------------------------------------------------------
    

if __name__ == "__main__":
    main()
