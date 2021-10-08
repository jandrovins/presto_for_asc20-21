"""
Folding of PRESTO test for ASC20-21 Event

This is an example script for dedisperse process in PRESTO test, 
which has been tested and verfied with PRESTO-v3.0 software.
For PRESTO-v2.0 with Python 2.xx, the name of some importing
packages should be changed.

This test read the *.fits and cands.inc file as the input parameter, and 
generate a result folder `fold` as working directory.
Use following commands to run the fold test.
```
    cd B1516+02_300s_2bit
    (time python ../source/asc2021_presto_fold.py B1516+02_300s_2bit.fits) > log.fold 2>&1
```

For more details about ASC Event, please refert to: 
http://www.asc-events.org/ASC20-21/
"""
import os, sys, glob, re
from subprocess import getoutput
import numpy as np
import time

from mpi4py import MPI
from mpi4py.futures import MPIPoolExecutor
#=================== Define Parameter ===================#
import sys
# Tutorial_Mode = True
Tutorial_Mode = False

rootname = 'Sband'
maxDM = 31 #max DM to search
minDM = 29
Nsub = 32 #32 subbands
Nint = 64 #64 sub integration
Tres = 0.5 #ms
zmax = 200
wmax = 100

filename = "B1516+02_300s_2bit.fits"

# print '''

# ================reading candidates==================

# '''


fp = open('cands.inc', 'r')

lines = fp.readlines()
cands = []
for line in lines:
    cand = {}
    line_list = line.split()
    cand['DM'] = float(line_list[1])
    cand['p']  = float(line_list[3])
    cand['DMstr'] = line_list[5]
    cands.append(cand)
    
fp.close()



# print '''

# ================folding candidates==================

# '''

def fold(cand):
    #return f"{fftf}\n", f"{time.time()}\n"
    foldcmd = "prepfold -n %(Nint)d -nsub %(Nsub)d -dm %(dm)f -p %(period)f %(filfile)s -o %(outfile)s -noxwin -nodmsearch" % {
            'Nint':Nint, 'Nsub':Nsub, 'dm':cand["DM"],  'period':cand["p"], 'filfile':filename, 'outfile':rootname+'_DM'+cand["DMstr"]} #full plotssearchcmd = "accelsearch -zmax %d -wmax %d %s"  % (zmax, wmax, fftf)
    stdout = f"{foldcmd} --- {os.getcwd()} -- FILENAME{filename}\n"
    return getoutput(foldcmd), stdout

cwd = os.getcwd()
if not os.access('fold', os.F_OK):
    os.mkdir('fold')
os.chdir('fold')

logfile = open('folding.log', 'wt')

if __name__ == "__main__":
    os.system('ln -s ../%s %s' % (filename, filename))
    t0 = time.time() #start wall time of fold
    with MPIPoolExecutor() as executor:
        result = executor.map(fold, cands)
        output, stdout = zip(*result)
        sys.stdout.writelines(stdout)
        logfile.writelines(output)
    
    walltime = "wall time = %.2f" % (time.time() - t0) # count wall time
    logfile.write(walltime + '\n')
    logfile.close()
    os.chdir(cwd)

