#!/usr/bin/env python
#RMS 2018
#Functions to aid in the generation of a dataframe from earthquake information

import re
import pandas as pd
import numpy as np
    

def read_quakes(infilename):
    
    '''Reads in a file in Global CMT ndk format and returns pandas dataframe of 
    event information. For now this just does the event location and magnitude,
    plus the strike, rake and dip of the first nodal plane. The full moment tensor
    information is also available if desired, but for the purposes of our clustering
    attempt this is probably not really needed'''
    
    split_string = lambda x, n: [x[i:i+n] for i in range(0, len(x), n)]
    
    infile = open(infilename,'r')
    fstring = infile.read().strip()
    
    quakes = split_string(fstring,405)
    
    #Columns of the dataframe to be filled
    EVLON = []
    EVLAT = []
    EVDEP = []
    EVMAG = []
    STRIKE1 = []
    RAKE1 = []
    DIP1 = []
    STRIKE2 = []
    RAKE2 = []
    DIP2 = []
    
    
    for quakestr in quakes:
        parts = quakestr.split('\n')
        hypocenter = parts[0].split()
        
        EVLAT.append(hypocenter[3])
        
        if float(hypocenter[4]) < 0:
            EVLON.append(360+float(hypocenter[4]))
        else:
            EVLON.append(float(hypocenter[4]))
            
        EVDEP.append(hypocenter[5])
        
        #print(hypocenter)
        
        try:
        
            if float(hypocenter[6]) == 0.0:
                EVMAG.append(hypocenter[7])
            else:
                EVMAG.append(hypocenter[6])
        except:
            
            EVMAG.append(np.nan)
        
        FP_elements = re.sub('\s+',',',parts[4]).split(',')
        #print(FP_elements)
        
        STRIKE2.append(FP_elements[-3])
        RAKE2.append(FP_elements[-2])
        DIP2.append(FP_elements[-1])
        
        STRIKE1.append(FP_elements[-6])
        RAKE1.append(FP_elements[-5])
        DIP1.append(FP_elements[-4])
       
       
    quakedf = pd.DataFrame({'Lat':EVLAT,'Lon':EVLON,'Dep':EVDEP,'Mag':EVMAG,
                'Strike_1':STRIKE1,'Rake_1':RAKE1,'Dip_1':DIP1,'Strike_2':STRIKE2,
                 'Rake_2':RAKE2,'Dip_2':DIP2})
    
    return quakedf
        
    
    
    
if __name__ == "__main__":
    
    read_quakes('jan76_dec17.ndk')

