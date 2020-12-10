#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importing Packages
import os
import geopandas as gpd
import pandas as pd
import fiona
import glob
from shapely.geometry import Point, LineString, Polygon
import matplotlib
from rasterstats import zonal_stats


# In[2]:


#Create a list of txt files and a dictionary for the columns of the dataframe to be used later)
file_list = [r'lab2_data/data/districts/district01.txt', r'lab2_data/data/districts/district05.txt' , r'lab2_data/data/districts/district06.txt']
dictionary = {'district': [], 'num_coords': [] , 'geometry': []}
for file in file_list:
    x = pd.read_csv(file , delim_whitespace = True) # read txt files in file_list
    coords = list(zip(x['X'], x['Y'])) #Create a list of coordinate pairs from the X and Y column of each file in file_list     
    poly = Polygon(coords) #create shape from coordinates
    num_coords = len(coords)   # Coordinate Count
    district = file[-14: -4:]   #District name in data frame
    dictionary['district'].append(district)   #Assigning vale to column in dictionary
    dictionary['num_coords'].append(num_coords)   #Assigning vale to column in dictionary
    dictionary['geometry'].append(poly)   #Assigning vale to column in dictionary
district_gdf = gpd.GeoDataFrame.from_dict(dictionary)   #Create geodataframe from dictionary

district_gdf.crs = {'init': 'epsg:4326'}  #Projection
district_gdf.to_file(driver='ESRI Shapefile',filename='district_gdf.shp') #Create shapefile from geodataframe

# Create list of tif files and run zonaal stats
agr_04 = zonal_stats(r'./district_gdf.shp', r'./lab2_data/data/agriculture/GLOBCOVER_2004_lab2.tif', stats="count min mean max median", categorical = True)
agr_09 = zonal_stats(r'./district_gdf.shp', r'./lab2_data/data/agriculture/GLOBCOVER_2009_lab2.tif', stats="count min mean max median", categorical = True)
print(agr_04)
print(agr_09)


# In[3]:


pix_total = [89799, 18585, 86459] #Total number of pixel in each district
pix_agr_04 = [35922, 6639, 39629] #Total numner of agricultural pixels in 2004
pix_agr_09 = [49487, 6449, 39185] #Total numner of agricultural pixels in 2000

#percentage of agricultural pixels = (Number of agricultural pixels/Total number of pixels) * 100
percent_agriculture_2004 = [(x / y) * 100 for x , y in zip(pix_agr_04, pix_total)]
percent_agriculture_2009 = [(x / y) * 100 for x , y in zip(pix_agr_09, pix_total)]
print(percent_agriculture_2004)
print(percent_agriculture_2009)


# In[4]:


# Create Datframe
final = {'district': ['01', '05', '06'], '2004%': ['40.0', '35.7', '45.8'], '2009%': ['55.0', '34.7', '45.3']}
final_df = pd.DataFrame(final)
print(final_df)


# In[5]:


# Trying Part 2 Loop
tif_list = [r'./lab2_data/data/agriculture/GLOBCOVER_2004_lab2.tif', r'./lab2_data/data/agriculture/GLOBCOVER_2009_lab2.tif']
for tif in tif_list:
    agriculture = zonal_stats(r'./district_gdf.shp', tif, stats="count min mean max median")
    print(agriculture)
    for item in agriculture:
        item['mean'] * 100


# In[ ]:




