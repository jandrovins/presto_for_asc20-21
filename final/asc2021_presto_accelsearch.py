"""
Accelsearch of PRESTO test for ASC20-21 Event

This is an example script for accelsearch process in PRESTO test, 
which has been tested and verfied with PRESTO-v3.0 software.
For PRESTO-v2.0 with Python 2.xx, the name of some importing
packages should be changed.

This test need a wroking directory `fft`, which contains the 
generated *.fft files from the `fft` test step and the given *.inf 
files from the input subfolder. The team may first copy the *.inf 
files, then run the script with following command:
```
    cd B1516+02_300s_2bit
    cp input/*.inf fft/
    (time python ../source/asc2021_presto_accelsearch.py) > log.accelsearch 2>&1
```

For more details about ASC Event, please refert to: 
http://www.asc-events.org/ASC20-21/
"""
import os, sys, glob, re
from subprocess import getoutput
import numpy as np
import time

from mpi4py.futures import MPIPoolExecutor
from mpi4py import MPI

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
#====================== fft search ======================#


def accelsearch(fftf):
    #return f"{fftf}\n", f"{time.time()}\n"
    searchcmd = "accelsearch -zmax %d -wmax %d %s"  % (zmax, wmax, fftf)
    stdout = f"{searchcmd} --- {os.getcwd()}\n"
    return getoutput(searchcmd), stdout

if __name__ == "__main__":
    cwd = os.getcwd()
    if not os.access('fft', os.F_OK):
        os.mkdir('fft')
        output = getoutput('cp ../input/*.inf ./')
        print(output)

#####################3
    logfile = open('accelsearch.log', 'wt')
    P_fft = Path('fft')
    fftfiles = [i.name for i in P_fft.glob("*.fft")]
    ### FOR MPI
    comm = MPI.COMM_WORLD
    nprocs = 48
    t0 = time.time() # start wall time of accelsearch
    with MPIPoolExecutor(max_workers=nprocs, wdir=P_fft.resolve()) as pool:
        result = pool.map(accelsearch, fftfiles)
        output, stdout = zip(*result)
        sys.stdout.writelines(stdout)
        logfile.writelines(output)
    walltime = "wall time = %.2f" % (time.time() - t0) # report wall time
    logfile.write(walltime + "\n")
    logfile.close()
    os.chdir(cwd)
    #MPI.COMM_WORLD.Abort(1)
