#!/usr/bin/env python 

#RMS 2019
#Finds the coordinates of the corners of MGRS grid cells and outputs shapely polgon objects
#Has not been properly tested and may give strange/incorrect results for MGRS precision level 0.

import mgrs
import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon

class MGRStopoly():
    def __init__(self,ncells):

        '''Takes in ncells, which is list of MGRS cells to be converted into shapely polygons'''

        self.ncells = ncells
        self.m = mgrs.MGRS()

    def generate_polytable(self):

        polys = [None]*len(self.ncells)
        for i in range(len(self.ncells)):
            c = self.ncells[i]
            cc = self.find_corners(c)
            polygon = self._make_mgrs_polgon(cc)
            polys[i] = polygon
    
        crs = {'init': 'epsg:4326'}
        polygon_data = gpd.GeoDataFrame(index=np.arange(len(polys)), crs=crs, geometry=polys) 

        return polygon_data  

    def _split_cell(self,cell):

        decoded_cell = cell.decode()
        base_comp = decoded_cell[:5]
        precision = int((len(decoded_cell) - len(base_comp))/2)
        
        #Easting is distance in meters from the SW corner of the cell
        easting = decoded_cell[5:5+precision]
        #Northing is distance in meters from the base of the cell 
        northing = decoded_cell[5+precision:]
        
        if len(str(easting)) == 0:
            easting = None
            northing = None
            
            return base_comp, easting, northing, precision
        
        else:
            
            return base_comp, int(easting.strip()), int(northing.strip()), precision

    def _lon_lat_conversion(self,lon,lat,distlon,distlat):
        
        '''Get the coordinates of a new point lon + distlon, lat + distlat'''
        
        
        R = 6.731e6 #earth radius in meters
        distance_1_deg_lon = 2*np.pi*R*np.cos(lat*np.pi/180.0)/360.0
        distance_1_deg_lat = 2*np.pi*R/360.0
        
        new_lon = lon + distlon/distance_1_deg_lon
        new_lat = lat + distlat/distance_1_deg_lat
        
        return new_lon,new_lat


    def _precision_string(self,p):
        
        if p <= 1:
            return '%i%i'
        elif p == 2:
            return '%02i%02i'
        elif p == 3:
            return '%03i%03i'
        elif p == 4:
            return '%04i%04i'
        elif p == 5:
            return '%05i%05i'
        elif p == 6:
            return '%06i%06i'

    def find_corners(self,cell):
        
        '''Return the coodinates of the four corners of this MGRS grid cell'''
        
        # . (lat_NW,lon_NW) -- .(lat_NE,lon_NE)
        # |                    |
        # |                    | 
        # |                    |
        # . (given) ---------- .(lat_SE,lon_SE)
        

        basecomp, easting, northing, precision = self._split_cell(cell)
        
        #Get the length of the cell side and multiply it by 
        #a scale factor so that we can be sure of ending up in the
        #adjacent cell. This is something of a fudge factor and should 
        #really be fixed. 

        side_length = 1.2*10000/10**(precision-1)
        
        if precision > 0:
            
            #Get the coordinates of the SW corner of the cell
            pstring = self._precision_string(precision)
            cellID = basecomp+pstring %(easting,northing)
            latitude_SW,longitude_SW = self.m.toLatLon(cellID.encode())
            
            #initial attempt to find numerical neighbors (assuming we don't have to extend into the next cell)

            east_comp = easting + 1
            north_comp = northing + 1
        
            
            #Get the southeast cell coordinates
            try:
                c_southeast = basecomp+pstring %(east_comp,northing)
                latitude_SE, longitude_SE = self.m.toLatLon(c_southeast.encode())
            except:
                latitude_SE = None
                longitude_SE = None
            
            #Get the northeast cell coordinates
            try:
                c_northeast = basecomp+pstring %(east_comp,north_comp)
                latitude_NE, longitude_NE = self.m.toLatLon(c_northeast.encode())
            except:
                latitude_NE = None
                longitude_NE = None
            
            #Get the northwest cell coordinates
            try:
                c_northwest = basecomp+pstring %(easting,north_comp)
                latitude_NW, longitude_NW = self.m.toLatLon(c_northwest.encode())
            except:
                latitude_NW = None
                longitude_NW = None
                
            if len(str(east_comp)) > len(str(easting)):
                print('Need to check the ID of eastern adjacent 100,000 m^2 cell')
                
                nlon,nlat = self._lon_lat_conversion(longitude_SW,latitude_SW,distlon=side_length,distlat=0)
                
                #This is the cell directly east of our cell
                c = self.m.toMGRS(nlat,nlon,MGRSPrecision=precision)
                latitude_SE, longitude_SE = self.m.toLatLon(c)
                
                nlon,nlat = self._lon_lat_conversion(longitude_SW,latitude_SW,distlon=side_length,distlat=side_length)            
                #This is the cell northeast of our cell
                c = self.m.toMGRS(nlat,nlon,MGRSPrecision=precision)
                latitude_NE, longitude_NE = self.m.toLatLon(c)
                            
            if len(str(north_comp)) > len(str(northing)):
                print('Need to check the ID of northern adjacent 100,000 m^2 cell')
                
                nlon,nlat = self._lon_lat_conversion(longitude_SW,latitude_SW,distlon=0,distlat=side_length)
                
                #This is the cell directly north of our cell
                c = self.m.toMGRS(nlat,nlon,MGRSPrecision=precision)
                latitude_NW, longitude_NW = self.m.toLatLon(c)
                
                nlon,nlat = self._lon_lat_conversion(longitude_SW,latitude_SW,distlon=side_length,distlat=side_length)            
                #This is the cell northeast of our cell
                c = self.m.toMGRS(nlat,nlon,MGRSPrecision=precision)
                latitude_NE, longitude_NE = self.m.toLatLon(c)
                
            
        else:
            
            #Get the coordinates of the SW corner of the cell 
            cellID = basecomp
            latitude_SW,longitude_SW = self.m.toLatLon(cellID.encode())
           
            elon,slat = self._lon_lat_conversion(longitude_SW,latitude_SW,distlon=side_length,distlat=0)
            c = self.m.toMGRS(slat,elon,MGRSPrecision=precision)
            latitude_SE, longitude_SE = self.m.toLatLon(c)
            
            elon,nlat = self._lon_lat_conversion(longitude_SW,latitude_SW,distlon=side_length,distlat=side_length)
            c = self.m.toMGRS(nlat,elon,MGRSPrecision=precision)
            latitude_NE, longitude_NE = self.m.toLatLon(c)
            
            wlon,nlat = self._lon_lat_conversion(longitude_SW,latitude_SW,distlon=0,distlat=side_length)
            c = self.m.toMGRS(nlat,wlon,MGRSPrecision=precision)
            latitude_NW, longitude_NW = self.m.toLatLon(c)
        
        
        return {'southwest':(latitude_SW,longitude_SW),'southeast':(latitude_SE,longitude_SE),'northeast':(latitude_NE,longitude_NE),\
                'northwest':(latitude_NW,longitude_NW)}

    def _make_mgrs_polgon(self,cc):
        
        lat_point_list = [cc['southwest'][0], cc['southeast'][0], cc['northeast'][0] ,cc['northwest'][0],cc['southwest'][0]]
        lon_point_list = [cc['southwest'][1], cc['southeast'][1], cc['northeast'][1] ,cc['northwest'][1],cc['southwest'][1]]
        polygon_geom = Polygon(zip(lon_point_list, lat_point_list))
        
        return polygon_geom
