"""
FFT of PRESTO test for ASC20-21 Event

This is an example script for fft process in PRESTO test, 
which has been tested and verfied with PRESTO-v3.0 software.
For PRESTO-v2.0 with Python 2.xx, the name of some importing
packages should be changed.

This test need a wroking directory `fft`, which contains the 
given *.dat files from the `input` subdirectory. The team may
first create a directory and copy the *.dat files, such as
```
    cd B1516+02_300s_2bit
    mkdir -p fft
    cp input/*.dat fft/
    (time python ../source/asc2021_presto_fft.py) > log.fft 2>&1
```

http://www.asc-events.org/ASC20-21/
"""
import os, sys, glob, re
from subprocess import getoutput
import numpy as np
import time
import multiprocess as mp
from functools import partial
from pathlib import Path


#=================== Define Parameter ===================#
Tutorial_Mode = False

rootname = 'Sband'
maxDM = 31 #max DM to search
minDM = 29
Nsub = 32 #32 subbands
Nint = 64 #64 sub integration
Tres = 0.5 #ms
zmax = 200
wmax = 100

cores = mp.cpu_count()
pool = mp.Pool(cores)
#====================== fft search ======================#
cwd = os.getcwd()

if not os.access('fft', os.F_OK):
    os.mkdir('fft')
    output = getoutput('cp input/*.dat fft/')
    print(output)

def realfft(df):
    fftcmd = "realfft %s" % df.resolve()
    stdout = "%s\n" % fftcmd
    return getoutput(fftcmd), stdout

P_fft = Path('fft')
datfiles = list(P_fft.glob("*.dat"))
logfile = open('fft.log', 'wt')
t0 = time.time() #start wall time of fft
result = pool.map(realfft, datfiles)
output, stdout = list(zip(*result))
logfile.writelines(stdout)
logfile.writelines(output)
#for df in datfiles:
#    fftcmd = "realfft %s" % df
#    logfile.write(fftcmd + '\n')
#    print(fftcmd)
#    
#    output = getoutput(fftcmd)
#    logfile.write(output)
walltime = "wall time = %.2f" % (time.time() - t0) # count wall time
logfile.write(walltime + '\n')
logfile.close()
