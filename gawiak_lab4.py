{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import pandas as pd\n",
    "import geopandas as gpd\n",
    "import fiona\n",
    "import glob\n",
    "import random\n",
    "import numpy as np\n",
    "import rasterio\n",
    "from rasterio.plot import  show, show_hist\n",
    "from rasterio.mask import mask\n",
    "from scipy.spatial import distance\n",
    "from scipy.spatial import cKDTree"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Function (that I couldn't get to work)\n",
    "#def stack_coords(data, other):\n",
    "    #'This function is used to stack x,y coordinates'\n",
    "    #for l in lines:\n",
    "    #x,y = l.split(',')\n",
    "    #data.append(float(x))\n",
    "    #other.append(float(y))\n",
    "    #stations = np.vstack([xs, ys])\n",
    "    #stations = stations.T\n",
    "    #return stations"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Open Files\n",
    "protected_areas_ras = rasterio.open(r'./data/data/protected_areas.tif')\n",
    "slope_ras = rasterio.open(r'./data/data/slope.tif')\n",
    "urban_areas_ras = rasterio.open(r'./data/data/urban_areas.tif')\n",
    "water_bodies_ras = rasterio.open(r'./data/data/water_bodies.tif')\n",
    "ws80m_ras = rasterio.open(r'./data/data/ws80m.tif')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Read Band\n",
    "protected_areas = protected_areas_ras.read(1)\n",
    "slope = slope_ras.read(1)\n",
    "urban_areas = urban_areas_ras.read(1)\n",
    "water = water_bodies_ras.read(1)\n",
    "ws80m = ws80m_ras.read(1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Wind\n",
    "#ws80m_rs = rasterio.open('/Users/jonathanburton/Desktop/Fall2020/Geog5092/lab4/data/ws80m.tif')\n",
    "#ws80m = ws80m_rs.read(1)\n",
    "ws80m = np.where(ws80m < 0, 0, ws80m)\n",
    "wind_arr = np.zeros_like(ws80m, np.float32)\n",
    "for row in range(5, ws80m.shape[0] - 5):\n",
    "    for col in range(4, ws80m.shape[1] - 4):     \n",
    "        win = ws80m[row - 5:row + 6,\n",
    "                   col - 4:col +5]\n",
    "        wind_arr[row, col] = win.mean()\n",
    "ws80m_array = np.where(wind_arr > 8.5, 1, 0)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "1754"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "row-5"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Protected Areas\n",
    "#pro_areas_rs = rasterio.open('./data/protected_areas.tif')\n",
    "#pro_areas = pro_areas_rs.read(1)\n",
    "protected_areas = np.where(protected_areas < 0, 0, protected_areas)\n",
    "pro_arr = np.zeros_like(protected_areas)\n",
    "for row in range(5, protected_areas.shape[0] - 5):\n",
    "    for col in range(4, protected_areas.shape[1] - 4):\n",
    "        win = protected_areas[row - 5:row + 6,\n",
    "                        col - 4:col + 5]\n",
    "        pro_arr[row, col] = win.mean()\n",
    "protected_areas_array = np.where(pro_arr < 0.05, 1, 0)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Slope\n",
    "slope = np.where(slope < 0, 0, slope)\n",
    "slope_arr = np.zeros_like(slope, np.float32)\n",
    "for row in range(5, slope.shape[0] - 5):\n",
    "    for col in range(4, slope.shape[1] - 4):\n",
    "        win=slope[row - 5: row + 6, \n",
    "                 col - 4: col + 5]\n",
    "        slope_arr[row, col] = win.mean()\n",
    "slope_array=np.where(slope_arr < 15, 1, 0)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Urban Areas\n",
    "#urban_areas_rs = rasterio.open('./data/urban_areas.tif')\n",
    "#urban_areas = urban_areas_rs.read(1)\n",
    "urban_areas = np.where(urban_areas < 0, 0, urban_areas)\n",
    "urban_arr = np.zeros_like(urban_areas)\n",
    "for row in range(5, urban_areas.shape[0] - 5):\n",
    "    for col in range(4, urban_areas.shape[1] - 4):\n",
    "        win = urban_areas[row - 5:row + 6,\n",
    "                    col - 4:col + 5]\n",
    "        urban_arr[row, col] = win.mean()\n",
    "urban_area_array = np.where(urban_arr == 0, 1, 0)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Water\n",
    "#water_rs = rasterio.open('./data/water_bodies.tif')\n",
    "#waters = water_rs.read(1)\n",
    "water = np.where(water < 0, 0, water)\n",
    "water_arr = np.zeros_like(water)\n",
    "for row in range(5, water.shape[0] - 5):\n",
    "    for col in range(4, water.shape[1] - 4):\n",
    "        win = water[row - 1:row + 6,\n",
    "                   col - 1:col + 5]\n",
    "    water_arr[row, col] = win.mean()\n",
    "water_body_array = np.where(water < 0.02, 1, 0)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Adding arrays\n",
    "suitability_array = np.zeros_like(water_body_array)\n",
    "suitability_array = water_body_array + urban_area_array + slope_array + protected_areas_array + ws80m_array"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "7838847"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "np.sum(suitability_array)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Creatiing 1s and 0s\n",
    "suitability_array = np.where(suitability_array == 5, 1, 0)\n",
    "suitability_array = suitability_array.astype('float32')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "There are 753.0 locations that meet the listed criteria\n"
     ]
    }
   ],
   "source": [
    "# Print Statement\n",
    "final_sites_num = suitability_array.sum()\n",
    "print('There are', final_sites_num, 'locations that meet the listed criteria')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Create GeoTif\n",
    "with rasterio.open(r'./data/data/slope.tif') as dataset:\n",
    "    with rasterio.open('./data/data/suitable_sites.tif' , 'w',\n",
    "                          driver='GTiff',\n",
    "                          height=suitability_array.shape[0],\n",
    "                          width=suitability_array.shape[1],\n",
    "                          count=1,\n",
    "                          dtype=np.float32,\n",
    "                          crs=dataset.crs,\n",
    "                            transform=dataset.transform,\n",
    "                          nodta=dataset.nodata\n",
    "                          ) as out_dataset:\n",
    "        out_dataset.write(suitability_array,1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Station coordinates\n",
    "xs = []\n",
    "ys = []\n",
    "with open(r'./data/data/transmission_stations.txt') as coords:\n",
    "    lines = coords.readlines()[1:]\n",
    "    for l in lines:\n",
    "        x,y = l.split(',')\n",
    "        xs.append(float(x))\n",
    "        #stack_coords (function that doesn't work)\n",
    "        ys.append(float(y))\n",
    "        stations = np.vstack([xs,ys])\n",
    "        stations = stations.T"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Centroides\n",
    "with rasterio.open(r'./data/data/suitable_sites.tif') as file:\n",
    "    bounds = file.bounds\n",
    "    top_left = (bounds[0], bounds[3])\n",
    "    bot_right = (bounds[1], bounds[2])\n",
    "    cellSize = 1000\n",
    "    x_coords = np.arange(top_left[0] + cellSize/2, bot_right[0], cellSize)\n",
    "    y_coords = np.arange(bot_right[1] + cellSize/2, top_left[1], cellSize)\n",
    "    x,y = np.meshgrid(x_coords, y_coords) \n",
    "    coords = np.c_[x.ravel(), y.ravel()]\n",
    "suitable = []\n",
    "for stat_x, stat_y in zip(coords, suitability_array.flatten()):\n",
    "    xdata = np.multiply(stat_x[0], stat_y)\n",
    "    ydata = np.multiply(stat_x[1], stat_y)\n",
    "    if xdata != 0 and ydata !=0:\n",
    "        suitable.append([xdata, ydata])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "The shortest distance is 1838.2666916151093\n",
      "The longest distance is 2954.4083392583366\n"
     ]
    }
   ],
   "source": [
    "# Distance between stations\n",
    "dd, ii = cKDTree(stations).query(suitable)\n",
    "print('The shortest distance is', np.min(dd)/1000)\n",
    "print('The longest distance is', np.max(dd)/1000)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.8"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
