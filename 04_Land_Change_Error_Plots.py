# %% [markdown]
## About 
# This code does the following:
# > 1. Finds the error between the predicted vs actual test values
# > 2. Finds the error between the predicted vs actual test values after outlier removal
# > 1. Finds the error between the predicted vs actual test values over 100 random samples
# > 1. Finds the error between the predicted vs actual test values over 100 random samples after outlier removal



# %% [markdown]
## Libraries
# %% [code]
import pandas as pd, numpy as np, matplotlib.pyplot as plt, rasterio as rio, glob, time, string
from osgeo import gdal
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from tqdm.notebook import tqdm as td 
from scipy import stats
start = time.time()



# %% [markdown]
## Read files 
# %% [code]
csvFiles = glob.glob("../06_Excel_Files/*.csv")
dc = {}
for i in td(range(len(csvFiles)), desc='Reading files'):
    dc[i] = pd.read_csv(csvFiles[i])
    dc[i].drop(columns=['Unnamed: 0'], inplace=True)  # redundant col dropped

    

# %% [markdown]
## Plot 1 - All values
# %% [code]
plt.rcParams["font.family"] = "Century Gothic"  # font of all plots set
plt.rcParams['figure.dpi'] = 300  # dpi of all plots set
for i in td(range(len(dc)), desc='Saving plots'):

    # 1 Plot
    plt.figure()
    dc[i]['diff'].plot(color='firebrick')
    plt.ylim([-0.8,0.8])
    plt.title("Predicted vs actual elevation DEM values") 
    plt.xlabel("Pixel number", fontweight='bold')  
    plt.ylabel("Error (m)", fontweight='bold')
    plt.grid(b=True, which='major', color='k', linestyle='--', alpha=0.50)
    plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.50)

    # 2 Add annotation
    x0, xmax = plt.xlim()
    y0, ymax = plt.ylim()
    data_width = xmax - x0
    data_height = ymax - y0
    plt.text(x0 + data_width, y0 + data_height,'({})'.format(string.ascii_lowercase[i:i+1]), size=14, bbox=dict(boxstyle="square",ec='k',fc='darkgray'))

    # 3 Save fig
    # plt.savefig("../05_Images/01_Land_Elevation_Changes/Area_{}_A_All.png".format(str(i+1).zfill(2)), bbox_inches='tight', facecolor='gainsboro')
    # plt.close()


    
# %% [markdown]
## Plot 2 - All values after outlier removal
for i in td(range(len(dc)), desc='Saving plots'):

    # 1 Remove outliers
    # 1.1 z-score method 
    # dftemp = dc[i]['diff'][(np.abs(stats.zscore(dc[i])) < 3).all(axis=1)].to_frame()

    # 1.2 quantile method (both give very similar results)
    q_low = dc[i]["diff"].quantile(0.01)
    q_hi  = dc[i]["diff"].quantile(0.99)
    dftemp = dc[i][(dc[i]["diff"] < q_hi) & (dc[i]["diff"] > q_low)]

    # 2 Plot
    plt.figure()
    dftemp.plot(color='firebrick', legend=None)
    plt.ylim([-0.2,0.2])
    plt.title("Predicted vs actual DEM values") 
    plt.xlabel("Pixel number", fontweight='bold')  
    plt.ylabel("Error (m)", fontweight='bold')
    plt.grid(b=True, which='major', color='k', linestyle='--', alpha=0.50)
    plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.50)

    # 3 Add annotation
    x0, xmax = plt.xlim()
    y0, ymax = plt.ylim()
    data_width = xmax - x0
    data_height = ymax - y0
    plt.text(x0 + data_width, y0 + data_height,'({})'.format(string.ascii_lowercase[i:i+1]), size=14, bbox=dict(boxstyle="square",ec='k',fc='darkgray'))

    # 4 Save fig
    plt.savefig("../05_Images/01_Land_Elevation_Changes/Area_{}_B_All_Filtered.png".format(str(i+1).zfill(2)), bbox_inches='tight', facecolor='gainsboro')
    plt.close()



# %% [markdown]
## Plot 3 - 100 random values
for i in td(range(len(dc)), desc='Saving plots'):

    # 1 Get 100 random rows
    df100 = dc[i]['diff'].sample(n=100).reset_index(drop=True)

    # 2 Plot the above random rows
    plt.figure()
    plt.ylim([-0.04,0.04])
    df100.plot(color='k')
    plt.title("Errors for 100 random samples") 
    plt.xlabel("Pixel number", fontweight='bold')  
    plt.ylabel("Error (m)", fontweight='bold')
    plt.grid(b=True, which='major', color='k', linestyle='--', alpha=0.50)
    plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.50)

    # 3 Add annotation
    x0, xmax = plt.xlim()
    y0, ymax = plt.ylim()
    data_width = xmax - x0
    data_height = ymax - y0
    plt.text(x0 + data_width, y0 + data_height,'({})'.format(string.ascii_lowercase[i:i+1]), size=14, bbox=dict(boxstyle="square",ec='k',fc='darkgray'))

    # 4 Save fig
    plt.savefig("../05_Images/01_Land_Elevation_Changes/Area_{}_C_100.png".format(str(i+1).zfill(2)), bbox_inches='tight', facecolor='gainsboro')
    plt.close()


    
# %% [markdown]
## Plot 4 - 100 random values after outlier removal
for i in td(range(len(dc)), desc='Saving plots'):

    # 1 Get 100 random rows
    # 1.1 Clean the original dataframes as in Plots -2 
    dftemp = dc[i]['diff'][(np.abs(stats.zscore(dc[i])) < 3).all(axis=1)].to_frame()

    # 1.2 Take 100 random sample rows
    df100Clean = dftemp.sample(n=100).reset_index(drop=True)

    # 2 Plot the above random rows
    plt.figure()
    df100Clean.plot(color='k', legend=None)
    plt.ylim([-0.03,0.03])
    plt.title("Errors for 100 random samples after filtering") 
    plt.xlabel("Pixel number", fontweight='bold')  
    plt.ylabel("Error (m)", fontweight='bold')
    plt.grid(b=True, which='major', color='k', linestyle='--', alpha=0.50)
    plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.50)

    # 3 Add annotation
    x0, xmax = plt.xlim()
    y0, ymax = plt.ylim()
    data_width = xmax - x0
    data_height = ymax - y0
    plt.text(x0 + data_width, y0 + data_height,'({})'.format(string.ascii_lowercase[i:i+1]), size=14, bbox=dict(boxstyle="square",ec='k',fc='darkgray'))

    # 4 Save fig
    plt.savefig("../05_Images/01_Land_Elevation_Changes/Area_{}_D_100_filtered.png".format(str(i+1).zfill(2)), bbox_inches='tight', facecolor='gainsboro')
    plt.close()




# %%
