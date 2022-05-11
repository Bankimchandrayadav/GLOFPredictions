# %% [markdown]
## About 
# This code does the following:
# > 1. Creates relationship between before and after flood LULC conditions 
# > 2. Predicts after LULC conditions based on before conditions over the test data



# %% [markdown]
## Libraries
import pandas as pd, numpy as np, matplotlib.pyplot as plt, rasterio as rio, glob, time
from osgeo import gdal
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from tqdm.notebook import tqdm as td 
start = time.time()



# %% [markdown]
## Read 'before' and 'after' DEMs into dictionaries
# 1 Get file names
rasBeforeNames = glob.glob(r"..\02_Data\03_Processed_Data\02_Rasters\01_Clipped_Areas\*Resampled.tif")
rasAfterNames = glob.glob(r"..\02_Data\03_Processed_Data\02_Rasters\01_Clipped_Areas\*After.tif")  

# 2.1 Define empty dictionaries
rasBefore = {}                                          
rasAfter = {}

# 2.2 Read files into dictionaries 
for i in range(len(rasBeforeNames)):                    
    rasBefore[i] = rio.open(rasBeforeNames[i]).read(1)  
    rasAfter[i] = rio.open(rasAfterNames[i]).read(1) 
    


# %% [markdown]
## Assign 'np.nan' to no-data pixels
for i in range(len(rasBeforeNames)):
    rasBefore[i][rasBefore[i]<0] = np.nan
    rasAfter[i][rasAfter[i]<0] = np.nan



# %% [markdown]
## Predict post GLOF conditions
for i in td(range(len(rasBeforeNames)), desc='Saving results'):

    # 1 Prepare 'X' and 'y'
    # 1.1 Get the row, col in array form
    X = pd.DataFrame()
    row = np.zeros((rasBefore[i].shape[0], rasBefore[i].shape[1]))
    col = np.zeros((rasBefore[i].shape[0], rasBefore[i].shape[1]))
    for a in range(rasBefore[i].shape[0]):
        for b in range(rasBefore[i].shape[1]):
            row[a,b] = a
            col[a,b] = b

    # 1.2 Get the row, col into 'X'
    X['Row'] = row.flatten('F')  
    X['Col'] = col.flatten('F') 

    # 1.3 Add 'before' Land elevation values to 'X'
    X['Land_Before'] = rasBefore[i].flatten('F')

    # 1.4 Prepare 'y'
    y = pd.DataFrame()
    y['Land_After'] = rasAfter[i].flatten('F')


    # 2 Remove NaNs from 'X' and 'y'
    # 2.1 Combine 'X' and 'y' to remove nans
    Xy = X.merge(y, left_index=True, right_index=True)  
    Xy.dropna(inplace=True)  
    Xy.reset_index(drop=True, inplace=True)

    # 2.2 Split back 'X' and 'y'
    X = Xy[['Row', 'Col', 'Land_Before']]
    y = Xy[['Land_After']]

    # 3 Train and run and the models
    # 3.1 Train model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)
    regressor = DecisionTreeRegressor(random_state=0)
    regressor.fit(X_train,y_train)

    # 3.2 Run model
    yPred = regressor.predict(X_test)

    # 3.3 Save results 
    df = pd.DataFrame()
    df['yPred'] = yPred
    df['yTest'] = y_test['Land_After'].values
    df['diff'] = df['yPred'] - df['yTest']
    df.to_csv("../06_Excel_Files/{}_Area_{}_error.csv".format(str(i+1).zfill(2), str(i+1).zfill(2)))
    
    # 4 Error Analysis - Overall plot
    def plot1():
        plt.figure(dpi=100)
        df['diff'].plot(color='firebrick')
        plt.ylim([-0.8,0.8])
        plt.title("Predicted vs actual elevation over the flood area") 
        plt.xlabel("Pixel number")  
        plt.ylabel("Error (m)")
        plt.grid(b=True, which='major', color='k', linestyle='--', alpha=0.50)
        plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.50)
        plt.savefig("../05_Images/01_Land_Elevation_Changes/Area_{}_01_Overall.png".format(str(i+1).zfill(2)), bbox_inches='tight', facecolor='w')
        plt.close()
    # plot1()

    # 5 Error Analysis - Overall plot after removing outliers
    def plot2():
        # 1 Remove outliers
        # 1.1 z-score method 
        from scipy import stats
        df1 = df['diff'][(np.abs(stats.zscore(df)) < 3).all(axis=1)].to_frame()

        # 1.2 quantile method (both give very similar results)
        # q_low = df["diff"].quantile(0.01)
        # q_hi  = df["diff"].quantile(0.99)
        # df1 = df[(df["diff"] < q_hi) & (df["diff"] > q_low)]

        # 2 Plot
        plt.figure(dpi=100)
        df1['diff'].plot(color='firebrick')
        plt.ylim([-0.2,0.2])
        plt.title("Predicted vs actual elevation over the flood area") 
        plt.xlabel("Pixel number")  
        plt.ylabel("Error (m)")
        plt.grid(b=True, which='major', color='k', linestyle='--', alpha=0.50)
        plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.50)
        plt.savefig("../05_Images/01_Land_Elevation_Changes/Area_{}_02_Overall_Filtered.png".format(str(i+1).zfill(2)), bbox_inches='tight', facecolor='w')
        plt.close()

        return df1
    # df1 = plot2()

    # 6 Error Analysis - Plot of 100 random values before removing outliers
    def plot3():
        # 1 Get 100 random rows
        df100 = df['diff'].sample(n=100).reset_index(drop=True)

        # 2 Plot the above random rows
        plt.figure(dpi=100)
        plt.ylim([-0.04,0.04])
        df100.plot(color='k')
        plt.title("Errors for 100 random samples") 
        plt.xlabel("Pixel number")  
        plt.ylabel("Error (m)")
        plt.grid(b=True, which='major', color='k', linestyle='--', alpha=0.50)
        plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.50)
        plt.savefig("../05_Images/01_Land_Elevation_Changes/Area_{}_03_100.png".format(str(i+1).zfill(2)), bbox_inches='tight', facecolor='w')
        plt.close()
    # plot3()

    # 7 Error Analysis - Plot of 100 random values after removing outliers 
    def plot4():


        # 1 Get 100 random rows
        df100_1 = df1['diff'].sample(n=100).reset_index(drop=True)

        # 2 Plot the above random rows
        plt.figure(dpi=100)
        df100_1.plot(color='k')
        plt.ylim([-0.03,0.03])
        plt.title("Errors for 100 random samples after filtering") 
        plt.xlabel("Pixel number")  
        plt.ylabel("Error (m)")
        plt.grid(b=True, which='major', color='k', linestyle='--', alpha=0.50)
        plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.50)
        plt.savefig("../05_Images/01_Land_Elevation_Changes/Area_{}_04_100_filtered.png".format(str(i+1).zfill(2)), bbox_inches='tight', facecolor='w')
        plt.close()

        
    # plot4()

print('Time elapsed: ', np.round((time.time()-start)/60), 'mins')


# %%
