#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from argparse import ArgumentParser



def main():
    p = ArgumentParser(description = 
                       "This script computes the Walden FOM under mismatch+process starting\
                       from Montecarlo data of SNDR and power consumption.")
    
    p.add_argument("sndr_file", 
                   type = str, 
                   help = "name of the .csv file containing SNDR data.")        

    p.add_argument("pwr_file", 
                   type = str, 
                   help = "name of the .csv file containing power consumption data.")        

    args = p.parse_args() 

    workdir = "ADC_test" 
    filepath = f"/home/spino/PhD/Lavori/{workdir}/CSV/"
    sndr_file = filepath + args.sndr_file
    pwr_file = filepath + args.pwr_file
    
    sndr_data = np.genfromtxt(sndr_file, delimiter=',')
    pwr_data = np.genfromtxt(pwr_file, delimiter=',')

    which_column_sndr = 1
    which_column_pwr = 1

    if sndr_data.shape != (sndr_data.shape[0],):
        sndr_data = np.transpose(sndr_data.transpose()[which_column_sndr])

    if pwr_data.shape != (pwr_data.shape[0],):
        pwr_data = pwr_data[1:][:]
        pwr_data = np.transpose(pwr_data.transpose()[which_column_pwr])


    fom_data = np.zeros_like(sndr_data)
    sampling_frequ = 200e6

    for idx, (sndr, power_consumption) in enumerate(zip(sndr_data, pwr_data)):
        enob = (sndr - 1.76)/6
        fom_data[idx] = power_consumption/(pow(2,enob) * sampling_frequ)        
    

    savepath = filepath + "fom_v12c.csv"
    np.savetxt(savepath, fom_data, delimiter=',')



if __name__ == "__main__":
    main()