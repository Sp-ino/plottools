#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Tue Mar  8 22:58:26 2022

@author: spino
Copyright (c) 2022 Valerio Spinogatti
Licensed under GNU license
"""


import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from argparse import ArgumentParser



def prettyprint_harms(xdata, ydata):
    print(f"\n\tFrequency:\t\t    Power:\n")
    for freq, power in zip(xdata, ydata):
        print(f"\t{freq:10.2f}\t\t{power:10.2f}")



def main():
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Palatino"]
        })
    
    #------------------------------Argument parsing-------------------------
    p = ArgumentParser(description = 
                       "This script performs some Fourier analysis on traces imported from \
                        a .csv file. In particular, it computes the FFT of every column \
                        (except the one with index 0) and optionally saves THD values \
                        to an output .csv file.")
    
    p.add_argument("filename", 
                   type = str, 
                   help = "name of the .csv file")
    p.add_argument("-p", 
                   "--userpath", 
                   type = str, 
                   help = "user specified path")
    p.add_argument("-x",
                   "--x_label",
                   type = str, 
                   help = "x label")
    p.add_argument("-y", 
                   "--y_label", 
                   type = str, 
                   help = "y label")
    p.add_argument("-a", 
                   "--start", 
                   type = int, 
                   help = "starting index from which to plot")
    p.add_argument("-m",
                   "--multiplier",
                   type = float,
                   default = 1,
                   help = "data is multiplied by the specified factor.\
                           Default value is 1")
    p.add_argument("-s", 
                   "--savethd", 
                   type = bool,
                   default = None,
                   help = "This option allows to save the list of THD values into a THD file")
    p.add_argument("-n", 
                   "--nyquist", 
                   type = bool,
                   default = None,
                   help = "This option allows proper computation of THD when the input signal is a tone at Nyquist.")
        
    
    args = p.parse_args() 
    #-----------------------------------------------------------------------


    #----------------------Generate file paths and import-------------------
    #decide in which path to look for the files (default or user defined)
    workdir = "ADC_test" 
    if args.userpath is None:
        filepath = f"/home/spino/PhD/Lavori/{workdir}/CSV/"
    else:
        filepath = args.userpath

    file = filepath + args.filename

    try:
        data = np.genfromtxt(file, delimiter = ",", dtype = np.double)
    except FileNotFoundError as e:
        print("Error: ", e)
        sys.exit(1) 

    if args.multiplier is not None:
        mul = args.multiplier
    else:
        mul = 1

    data_rows = data.transpose()
    xdata = data_rows[0, 1:]
    ydata = mul * data_rows[1:, 1:]
    #-----------------------------------------------------------------------


    #----------------------Save arguments into variables--------------------
    if args.start is not None:  
        first_sample = args.start
    else:
        first_sample = 0  
        
    if args.x_label is not None:
        xlab = args.x_label
    else:
        xlab = "frequency [Hz]"

    if args.y_label is not None:
        ylab = args.y_label
    else:
        ylab = "magnitude [dB20]"
    #-----------------------------------------------------------------------


    #-----------------------------------------------------------------------
    Tsample =12*416e-12
    N = 32                                                          #N should be a power of 2
    sndr_list = []
    n_traces = ydata.shape[0]
    bottomval = -80
    print("\n\nn_traces: ", n_traces, "\n\n")    
    if args.nyquist:
        fundam_index = N//2
    else:
        fundam_index = 1

    linydata = np.zeros((n_traces, N))

    for index, curve in enumerate(ydata):
        totransform = curve[first_sample:N+first_sample]            #compute DFT
        plt.plot(totransform, "-o")
        transform = fft(totransform)
        linydata[index,:] += 2.0/N * np.abs(transform[:N])

        totsquared = sum(np.power(linydata[index, 2:N//2], 2))
        thdlin = totsquared/(linydata[index, fundam_index]**2)
        thd = 10*np.log10(thdlin)   
        sndr_list.append(-thd)
        print("SNDR =", -thd)

    start_index = 0
    stop_index = N
    
    xdata = np.linspace(0.0, 1.0/(Tsample), N+1) #compute x-axis for the DFT
    ydata = 20*np.log10(linydata)               #compute DFT in dB
    prettyprint_harms(xdata, ydata[0])

    if len(sndr_list) >= 2 and args.savethd:
        print("saving thd list...")
        outname = "sndr_" + args.filename
        outfile = filepath + outname
        np.savetxt(outfile, sndr_list, delimiter = ",")
    #-----------------------------------------------------------------------


    #-----------------------Extract vectors, plot and save------------------
    fig, ax = plt.subplots(figsize=(7.5, 4.5))

    for trace in ydata:
        ax.stem(xdata[start_index:stop_index], trace[start_index:stop_index], bottom = bottomval)

    if len(sndr_list) == 1:
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        textstr = '\n'.join((
            r'$SNDR =%.2f$' % (sndr_list[0], ),
            ))
        ax.text(0.05, 0.95, textstr, transform = ax.transAxes, fontsize = 14,
                verticalalignment = 'top', bbox = props)

    # #add legend if necessary
    # ax.legend(loc = "lower right")
    

    ax.set_xlabel(xlab) #add x label
    ax.set_ylabel(ylab) #add y label

    #clean whitespace padding
    fig.tight_layout()
    
    #save and show the result
    if args.userpath is None:
        savepath = f"/home/spino/PhD/Lavori/{workdir}/CSV/" #if userpath is not specified then a default path is used 
    else:
        savepath = args.userpath[0:-4] + "Manoscritti/figures/"

    figname = "dft_" + args.filename[0:-4] + ".png"
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
