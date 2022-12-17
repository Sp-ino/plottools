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
from argparse import ArgumentParser



def main():
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Palatino"]
        })
    
    #------------------------------Argument parsing-------------------------
    p = ArgumentParser(description = 
                       "This script allows to compute the rms value of a sequence imported from a virtuoso .csv")
    
    p.add_argument("filename", 
                   type = str, 
                   help = "name of the .csv file")
    args = p.parse_args() 
    #-----------------------------------------------------------------------

    #---------------------------Generate file paths-------------------------
    #decide in which path to look for the files (default or user defined)
    file = args.filename
    #-----------------------------------------------------------------------

    try:
        data = np.genfromtxt(file, delimiter = ",") #if -m is true then data is imported as a numpy matrix
    except:
        print("Could not import " + args.filename)
        sys.exit(1) 

    yval = data.transpose()
    yval = yval[1,1:]

    plt.plot(yval)
    plt.show()

    sq = [pow(val,2) for val in yval]
    rms_val = np.sqrt(sum(sq)/len(yval))
    print(rms_val)



if __name__ == "__main__":
    main()