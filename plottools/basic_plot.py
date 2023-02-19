#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on Tue Mar  8 19:35:25 2022

@author: spino
Copyright (c) 2022 Valerio Spinogatti
Licensed under GNU license
"""

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
                       "This script allows to plot traces imported from .csv files. The .csv file is \
                        expected to have traces stored as columns, with the first column being the x data. \
                        The first row is expected to contain the header of the .csv with the column names.\
                        The program supports basic on-the-fly processing of the traces: for example, the \
                        user can choose whether to plot all the points in each trace or just part of them, \
                        or it can decide to treat the first column of the .csv file as either x data or y \
                        data.")
    
    p.add_argument("filename", 
                   type=str, 
                   help="Name of the .csv file"
                   )
    p.add_argument("-x", 
                   "--x_label",
                   type=str, 
                   help="x axis label")
    p.add_argument("-y", 
                   "--y_label", 
                   type=str, 
                   help="y axis label"
                   )
    p.add_argument("-a", 
                   "--start", 
                   type=int, 
                   help="Starting index from which to plot"
                   )
    p.add_argument("-o", 
                   "--stop", 
                   type=int, 
                   help="Index of the last element to be plotted"
                   )
    p.add_argument("-l",
                    "--legend",
                    type=str,
                    nargs="+",
                    default=None,
                    help="Names to be used in the legend. If there are more names \
                            than the number of traces, the extra ones are ignored."
                    )
    p.add_argument("-c",
                   "--columns",
                   type=int,
                   nargs="+",
                   default=None,
                   help="Indices of the columns to plot as y data from the .csv. \
                        The count should start from 1 if the first column of the .csv \
                        represents the x axis. If a 0 is passed as argument, the program \
                        will assume that column 0 of the .csv  also represents y data \
                        and the selected columns will be plotted against the number of \
                        samples. If an index is specified more than once the extra \
                        occurrences are ignored."
                   )
    p.add_argument("-f",
                   "--formatting",
                   type=str,
                   nargs="+",
                   default=None,
                   help="Formatting with which each column should be plotted. Formattings will be \
                        applied in the same order with which they are specified to each of \
                        the traces that are plotted")
    p.add_argument("-m",
                   "--multipliers",
                   type=float,
                   nargs="+",
                   default=None,
                   help="y data is multiplied by the specified factors.\
                           Default value is 1 for all columns. The number \
                           of multipliers that are passed to the program \
                           must coincide with the number of y data columns \
                           that are going to be plotted (this takes into account \
                           the -c option)."
                   )

    args = p.parse_args() 
    #-----------------------------------------------------------------------

    #----------------------Generate file paths and import-------------------
    file = args.filename    

    try:
        data = np.genfromtxt(file, delimiter=",", dtype=np.double, skip_header=1)
    except FileNotFoundError as e:
        raise FileNotFoundError("Could not open csv file. Check that it exists and/or you have permission to read it.")

    # Remove header
    # _, data = data[0], data[1:]

    # Extract number of columns
    num_data_cols = data.shape[1]
    #-----------------------------------------------------------------------

    #----------------------Save arguments into variables--------------------
    # Manage start and stop arguments
    if args.start is not None:  
        start_index = args.start
    else:
        start_index = 0  
        
    if args.stop is not None:
        stop_index = args.stop + 1
    else:
        stop_index = data.shape[0]

    # Manage labels
    if args.x_label is not None:
        xlab = args.x_label
    else:
        xlab = "x axis"

    if args.y_label is not None:
        ylab = args.y_label
    else:
        ylab = "y axis"

    # Manage legend names
    if args.legend is not None:
        legend_names = args.legend

    # Manage --columns argument, that defines which columns of the .csv are plotted
    if args.columns is None:    # if -c option is not specified, plot all columns against column 0
        col_indices = np.arange(1, num_data_cols)
    else:                       # otherwise plot only the specified ones
        col_indices = np.unique(args.columns)

    num_y_cols = col_indices.shape[0]

    if num_data_cols == 1 and 0 not in col_indices:
        raise Warning("Option -c: the .csv file that has been imported has just one column of data. \
If you want to plot it rerun the script with the option --columns 0 or -c 0.")
    
    if (0 not in col_indices and num_y_cols > num_data_cols-1) or (0 in col_indices and num_y_cols > num_data_cols):
        raise ValueError("Option -c: The number of selcted columns must be less or equal than the number \
of columns in the .csv file.")

    if np.any(col_indices[col_indices > num_data_cols]) or np.any(col_indices[col_indices < 0]):
        raise ValueError("Option -c: one (or more) of the specified indices is invalid.")
    

    # Manage scaling factor for each trace
    if args.multipliers is not None:
        if len(args.multipliers) != num_y_cols:
            raise ValueError("Option -m: the number of multipliers that are specified must coincide with \
the number of traces to be plotted.")
        multipliers = np.expand_dims(np.array(args.multipliers), 0)
    else:
        multipliers = np.ones((1, num_y_cols))
    #-----------------------------------------------------------------------

    #-----------------------Extract traces, plot and save-------------------
    fig, ax = plt.subplots(figsize=(7.5, 4.5))

    y = multipliers * data[start_index:stop_index, col_indices]

    for idx, trace in enumerate(y.transpose()):
        formatting = f"{args.formatting[idx]}" if args.formatting is not None else ''

        if 0 not in col_indices:
            x = data[start_index:stop_index, 0]
            ax.plot(x, trace, formatting)
        else:
            ax.plot(trace, formatting)

    # #add legend if necessary
    if args.legend is not None:
        ax.legend(legend_names, loc = "lower right")
    
    ax.set_xlabel(xlab) #add x label
    ax.set_ylabel(ylab) #add y label

    #clean whitespace padding
    fig.tight_layout()

    savepath = f"{args.filename[0:-4]}.png"
    try:
        fig.savefig(savepath, dpi = 600)
    except:
        print("Couldn't save figure to specified path. Check savepath and make sure it exists.")

    # Show figure before exiting
    # Add log that warns user to close the figure
    plt.show(block=True) 
    #-----------------------------------------------------------------------
    
    
if __name__ == "__main__":
    main()