#!/bin/bash

#RMS 2019
#Driver program for the ISS track matter

#User enters the number of hours they want to track ISS for
nhours=$1

#Get the historical data file
scp dna@lx4.geo.berkeley.edu:/data/dna/rmartin/ISS_tracker/ISS_tracking.csv .

#Run the script to plot the map
./track_map.py --n $nhours

