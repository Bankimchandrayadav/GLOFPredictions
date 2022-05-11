# %% [markdown]
## About 
# This code does the following:
# > 1. Prepares the tables of error plots for regions 1-10



# %% [markdown]
## Libraries
import pandas as pd, numpy as np, matplotlib.pyplot as plt, rasterio as rio, glob, time, string
from osgeo import gdal
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from tqdm.notebook import tqdm as td 
from scipy import stats
start = time.time()
from sklearn.cluster import KMeans



# %% [markdown]
## Read error files 
csvFiles = glob.glob("../06_Excel_Files/*.csv")
dc = {}
for i in td(range(len(csvFiles)), desc='Reading files'):
    dc[i] = pd.read_csv(csvFiles[i])
    dc[i].drop(columns=['Unnamed: 0'], inplace=True)  # redundant col dropped

    

# %% [markdown]
## Read 'before' and 'after' DEMs into dictionaries
# 1 Get file names
rasBeforeNames = glob.glob(r"..\02_Data\03_Processed_Data\02_Rasters\01_Clipped_Areas\*Resampled.tif")
rasAfterNames = glob.glob(r"..\02_Data\03_Processed_Data\02_Rasters\01_Clipped_Areas\*After.tif")  

# 2.1 Define empty dictionaries
rasBefore = {}                                          
rasAfter = {}

# 2.2 Read files into dictionaries 
for i in td(range(len(rasBeforeNames)), desc='Reading raster files'):                    
    rasBefore[i] = rio.open(rasBeforeNames[i]).read(1)  
    rasAfter[i] = rio.open(rasAfterNames[i]).read(1) 
    
# 2.3 Assign 'np.nan' to no-data pixels
for i in td(range(len(rasBeforeNames)), desc='Setting np.nan values'):
    rasBefore[i][rasBefore[i]<0] = np.nan
    rasAfter[i][rasAfter[i]<0] = np.nan



# %% [markdown]
## Prepare error table
# 1 Declare dataframe 
df = pd.DataFrame(columns=['Land_Per_Before', 'Land_Per_After', 'Count', 'Min Error', 'Max Error', 'Mean Error', 'Std', 'Percentile25', 'Percentile50', 'Percentile75'], index=range(10))

# 2 Get values into dataframe
for i in td(range(len(dc)), desc='Preparing error table'):

    # 1 Land Percentage before GLOF
    Land_Per_Before = (np.count_nonzero(~np.isnan(rasBefore[i]))/rasBefore[i].size)*100
    df['Land_Per_Before'][i] = Land_Per_Before

    # 2 Land Percentage after GLOF
    Land_Per_After = (np.count_nonzero(~np.isnan(rasAfter[i]))/rasAfter[i].size)*100
    df['Land_Per_After'][i] = Land_Per_After

    # 3 Error stats 
    df['Count'][i] = dc[i].abs().describe().T['count'][-1] 
    df['Min Error'][i] = dc[i].abs().describe().T['min'][-1] 
    df['Max Error'][i] = dc[i].abs().describe().T['max'][-1] 
    df['Mean Error'][i] = dc[i].abs().describe().T['mean'][-1] 
    df['Std'][i] = dc[i].abs().describe().T['std'][-1] 
    df['Percentile25'][i] = dc[i].abs().describe().T['25%'][-1] 
    df['Percentile50'][i] = dc[i].abs().describe().T['50%'][-1] 
    df['Percentile75'][i] = dc[i].abs().describe().T['75%'][-1] 


    
# %% [markdown] 
## Add slope info to error table 
# 1 Get file names
slopeBeforeNames = glob.glob("../02_Data/03_Processed_Data/02_Rasters/02_Slope_And_Aspect_Maps/01_Slope_Maps/*Before_Resampled_slope.tif")
slopeAfterNames = glob.glob("../02_Data/03_Processed_Data/02_Rasters/02_Slope_And_Aspect_Maps/01_Slope_Maps/*After_slope.tif")

# 2.1 Define empty dictionaries
slopeBefore = {}                                          
slopeAfter = {}

# 2.2 Read files into dictionaries 
for i in td(range(len(slopeBeforeNames)), desc='Reading files'):                    
    slopeBefore[i] = rio.open(slopeBeforeNames[i]).read(1)  
    slopeAfter[i] = rio.open(slopeAfterNames[i]).read(1) 
    

# %% [markdown]
dfTemp = pd.DataFrame()
dfTemp['Slope_Before'] = slopeBefore[0].flatten('F')
dfTemp['Slope_After'] = slopeAfter[0].flatten('F')
dfTemp['dff'] = dfTemp['Slope_Before'] - dfTemp['Slope_After']
dfTemp.dropna(inplace=True)


# %%
model=KMeans(4)
model.fit(dfTemp.dff.values.reshape(-1,1))
dfTemp['cl'] = model.labels_
dfTemp['dff'].plot(c='cl', colormap='gist_rainbow')
# %%
