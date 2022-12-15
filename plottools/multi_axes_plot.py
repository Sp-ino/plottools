#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams


rcParams['text.usetex'] = True 
rcParams['font.family'] = 'Times New Roman'

dircsv="/home/cristian/csv/sallen_key_10GHz/csv_files/"
filecsv="csv_noisespectrum.csv"
data=np.genfromtxt(dircsv+filecsv,delimiter=',',skip_header=1)

datax=data[:,0]
datay=data[:,1:]










for columns in datay.transpose():
    plt.plot(datax/(10**9),columns,label=r"\textit{Noise Spectrum}")
#plt.yticks(np.linspace(50,100,11))
#plt.xticks(np.logspace(1, 3, 7))
#plt.xscale('log')
plt.xlabel(r"\textit{frequency [GHz]}",fontsize=16)

plt.ylabel(r"\textit{[$\frac{V}{\sqrt{Hz}}$]}",fontsize=16)
plt.title(r"\textit{Noise Spectrum}")
# plt.legend()
plt.savefig("/home/cristian/csv/sallen_key_10GHz/pdf_files/"+filecsv[:-4]+".pdf")
plt.figure()
plt.show()

