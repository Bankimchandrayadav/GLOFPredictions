# %% [markdown]
## About 
# >1. This code prepares 'before' and 'after' slope and aspect maps of regions 1-10



# %% [markdown]
## Libraries 
import pandas as pd, numpy as np, matplotlib.pyplot as plt, rasterio as rio, glob, richdem as rd
from osgeo import gdal
from tqdm.notebook import tqdm as td 



# %% [markdown]
## Get filenames 
rasBeforeNames = glob.glob("../02_Data/03_Processed_Data/02_Rasters/01_Clipped_Areas/*Before_Resampled.tif")
rasAfterNames = glob.glob("../02_Data/03_Processed_Data/02_Rasters/01_Clipped_Areas/*After.tif")



# %% [markdown]
## Prepare slope maps from 'before' and 'after' dems
outDir = "../02_Data/03_Processed_Data/02_Rasters/02_Slope_And_Aspect_Maps/01_Slope_Maps/"
for i in td(range(len(rasBeforeNames)), desc='Preparing slope maps'):

    # 1 Load dem 
    demBefore = rd.LoadGDAL(rasBeforeNames[i])  
    demAfter = rd.LoadGDAL(rasAfterNames[i])

    # 2 Remove nodata values from calculation
    demBefore[demBefore<0] = np.nan
    demAfter[demAfter<0] = np.nan

    # 3 Set outfiles names 
    slopeBeforeName = outDir+rasBeforeNames[i].split('\\')[-1].split('.')[0]+'_slope.tif'
    slopeAfterName = outDir+rasAfterNames[i].split('\\')[-1].split('.')[0]+'_slope.tif'
    
    # 4 Get maps
    slopeBefore = rd.TerrainAttribute(demBefore, attrib='slope_degrees')  
    rd.SaveGDAL(filename=slopeBeforeName, rda=slopeBefore)  # save map
    slopeAfter = rd.TerrainAttribute(demAfter, attrib='slope_degrees')  
    rd.SaveGDAL(filename=slopeAfterName, rda=slopeAfter)  



# %% [markdown]
## Prepare aspect maps from 'before' and 'after' dems
outDir = "../02_Data/03_Processed_Data/02_Rasters/02_Slope_And_Aspect_Maps/02_Aspect_Maps/"
for i in td(range(len(rasBeforeNames)), desc='Preparing slope maps'):

    # 1 Load dem 
    demBefore = rd.LoadGDAL(rasBeforeNames[i])  
    demAfter = rd.LoadGDAL(rasAfterNames[i])

    # 2 Remove nodata values from calculation
    demBefore[demBefore<0] = np.nan
    demAfter[demAfter<0] = np.nan

    # 3 Set outfiles names 
    aspectBeforeName = outDir+rasBeforeNames[i].split('\\')[-1].split('.')[0]+'_aspect.tif'
    aspectAfterName = outDir+rasAfterNames[i].split('\\')[-1].split('.')[0]+'_aspect.tif'
    
    # 4 Get maps
    aspectBefore = rd.TerrainAttribute(demBefore, attrib='aspect')
    rd.SaveGDAL(filename=aspectBeforeName, rda=aspectBefore)
    aspectAfter = rd.TerrainAttribute(demAfter, attrib='aspect')
    rd.SaveGDAL(filename=aspectAfterName, rda=aspectAfter)



# %%
