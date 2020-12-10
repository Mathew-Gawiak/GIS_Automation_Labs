#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import geopandas as gpd
import pandas as pd
import fiona
import glob
from shapely.geometry import Point, LineString, Polygon
import matplotlib
from rasterstats import zonal_stats
import random
import numpy as np
random.seed(0)


# In[2]:


shed_files = fiona.listlayers(r'./lab3.gpkg')
sheds = []
for files in shed_files:
    if "wdbhuc" in files:
        sheds.append(files)
sample_points = {'point_id': [], 'geometry':[], 'HUC': []}
for polys in sheds:
    shed_files_gdf = gpd.read_file(r'./lab3.gpkg', layer = polys)
    huccode = [f for f in shed_files_gdf.columns if 'HUC' in f][0]
    for idx, row in shed_files_gdf.iterrows():
        j = int(0)
        extent = row['geometry'].bounds
        area_km = row["Shape_Area"]/1000000
        n = (int(round(area_km*0.05)))
        while j < n:
            x = random.uniform(extent[0], extent[2])
            y = random.uniform(extent[1], extent[3])
            p = (Point(x,y))
            if row['geometry'].contains(p):
                sample_points['geometry'].append(p)
                sample_points['point_id'].append(row[huccode][:8])
                sample_points['HUC'].append(huccode)
                j = j + 1
sample_points_gdf = gpd.GeoDataFrame(sample_points)
ssurgo = gpd.read_file(r'./lab3.gpkg', layer = 'ssurgo_mapunits_lab3')
sample_points_gdf = sample_points_gdf.set_crs("EPSG:26913")
new_class = gpd.sjoin(sample_points_gdf, ssurgo,  how='left', op="within")
group = new_class.groupby(by=['HUC', 'point_id']).mean()
print(group['aws0150'])

