# %% [markdown]
## About 
### This code resamples the input files to same resolution and extent



# %% [markdown]
## Libraries 
import pandas as pd, numpy as np, matplotlib.pyplot as plt, rasterio as rio, glob
from osgeo import gdal
from tqdm.notebook import tqdm as td 



# %% [markdown]
## Read files 
# 1 Get list of files 
rasBeforeNames = glob.glob("../02_Data/03_Processed_Data/02_Rasters/01_Clipped_Areas/*Before.tif")
rasAfterNames = glob.glob("../02_Data/03_Processed_Data/02_Rasters/01_Clipped_Areas/*After.tif")

# 2 Read them into dictionaries
rasBefore = {}
for i in range(len(rasBeforeNames)):
    rasBefore[i] = rio.open(rasBeforeNames[i]).read(1)
rasAfter = {}
for i in range(len(rasAfterNames)):
    rasAfter[i] = rio.open(rasAfterNames[i]).read(1)



# %% [markdown]
## Resample 
for i in td(range(len(rasBeforeNames)), desc='Resampling'):
    temp = gdal.Open(rasAfterNames[i])
    result = gdal.Warp(
        destNameOrDestDS=rasBeforeNames[i].split('.tif')[0]+'_Resampled'+'.tif',
        srcDSOrSrcDSTab=rasBeforeNames[i],
        width=temp.RasterXSize,
        height=temp.RasterYSize
        # xRes=temp.GetGeoTransform()[1],
        # yRes=temp.GetGeoTransform()[5],
    )
    result=None



# %% [markdown] 
## Validate
# 1 Get the list of output rasters (i.e. resampled 'before' rasters)
outputRasters = glob.glob("../02_Data/03_Processed_Data/02_Rasters/01_Clipped_Areas/*_Resampled.tif")

# 2 Define dataframes to compare the  resampled-'before' and 'after' rasters 
dfBefore = pd.DataFrame(columns=['width', 'height', 'xRes','yRes'], index=range(10))
dfAfter = pd.DataFrame(columns=['width', 'height', 'xRes','yRes'], index=range(10))

# 3 Get raster attributes into dataframes
for i in td(range(len(outputRasters)), desc='Verifying'):

    # 3.1 Read the raster into temp file
    temp1 = gdal.Open(outputRasters[i])
    temp2 = gdal.Open(rasAfterNames[i])

    # 3.2 Get the attributes of 'before_resampled' rasters
    dfBefore.width[i] = temp1.RasterXSize 
    dfBefore.height[i] = temp1.RasterYSize
    dfBefore.xRes[i] = temp1.GetGeoTransform()[1]
    dfBefore.yRes[i] = temp1.GetGeoTransform()[5]

    # 3.2 Get the attributes of 'after' rasters
    dfAfter.width[i] = temp1.RasterXSize 
    dfAfter.height[i] = temp1.RasterYSize
    dfAfter.xRes[i] = temp1.GetGeoTransform()[1]
    dfAfter.yRes[i] = temp1.GetGeoTransform()[5]

# 4 Compare the two dataframes
dfBefore == dfAfter

# %%
