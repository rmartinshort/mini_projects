#!/usr/bin/env python

#RMS 2019
#track map for the ISS

from urllib.request import urlopen
import json
import pandas as pd
import numpy as np
import time
from datetime import datetime

import shapely.geometry as sgeom
import cartopy.crs as ccrs
from cartopy.feature.nightshade import Nightshade
import matplotlib.pylab as plt

import argparse


def getISSloc():
    
    response = urlopen("http://api.open-notify.org/iss-now.json")
    obj = json.loads(response.read())
    
    lon = float(obj['iss_position']['longitude'])
    lat = float(obj['iss_position']['latitude'])
    
    return lon,lat


def plot_ISS(trackdf,nhours_plot=1):

    fig = plt.figure(figsize=(20, 10))

    projection_type = ccrs.PlateCarree()
    ax = fig.add_subplot(1, 1, 1, projection=projection_type)

    ax.coastlines(resolution='50m',linewidth=0.3)

    timestart = trackdf.index[-1] - np.timedelta64(nhours_plot,'h')
    track = trackdf[timestart:]

    jump_indices = list(track[abs(track['londiff'])>330].index)

    for i in range(len(jump_indices)):
        
        if i == 0:
            subtrack = track[:jump_indices[0]]
        else:
            subtrack = track[jump_indices[i-1]:jump_indices[i]].iloc[1:]
            
        track_points = sgeom.LineString(zip(subtrack['Lon'], subtrack['Lat']))
        ax.add_geometries([track_points], projection_type,facecolor='none', \
                        edgecolor='r',alpha=0.8)
        
        #plot the locations as points
        ax.plot(subtrack['Lon'],subtrack['Lat'],'ko',transform=projection_type,markersize=0.5)

    #plot the final subtrack
    subtrack = track[jump_indices[i]:].iloc[1:]
    track_points = sgeom.LineString(zip(subtrack['Lon'], subtrack['Lat']))
    ax.add_geometries([track_points], projection_type,facecolor='none', \
                      edgecolor='r',alpha=0.8)
    #plot the locations as points
    ax.plot(subtrack['Lon'],subtrack['Lat'],'ko',transform=projection_type,markersize=0.5)

    #Get current location
    current_lon,current_lat = getISSloc()

    ax.plot(current_lon,current_lat,'bo',transform=projection_type,markersize=20)

    #Get current time
    date = datetime.utcnow()

    ax.set_title('ISS history and position for {}'.format(date))
    ax.stock_img()
    ax.add_feature(Nightshade(date, alpha=0.2))
    plt.show()
    plt.savefig('Latest_ISS_plot.pdf',dpi=200)


def main():

    parser = argparse.ArgumentParser(description='Enter the number of hours of ISS data to plot')

    parser.add_argument('--n','--nhours', action='store',dest='nhours',\
        type=int, help='Number of hours of ISS to plot (from present)')
    args = parser.parse_args()

    nhours = args.nhours

    trackdf = pd.read_csv('ISS_tracking.csv',index_col='Timestamp',parse_dates=True)

    trackdf['londiff'] = abs(trackdf['Lon'].diff().shift(-1))

    plot_ISS(trackdf,nhours)



if __name__ == '__main__':

    main()



