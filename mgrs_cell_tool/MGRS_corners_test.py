#!/usr/bin/env python 

#RMS 2019
#test of MGRS corners 

import mgrs
import numpy as np
from MGRS_corners import MGRStopoly

def main():

    m = mgrs.MGRS()

    ncells = []
    precision = 3
    for i in range(100):
        randlat = np.random.uniform(-50,50,1)[0]
        randlon = np.random.uniform(-179,179,1)[0]
        c = m.toMGRS(randlat,randlon,MGRSPrecision=precision)
        ncells.append(c)

    convert = MGRStopoly(ncells)
    polygons = convert.generate_polytable()
    print(polygons)


if __name__ == '__main__':

    main()




