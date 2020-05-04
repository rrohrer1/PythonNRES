# 1. Use Pandas to repeat the Week 5 Exercise 5.7
# Hint1: Use pd.read_csv(url, ...) to read the USGS online gauge data.
# Hint2: Use df.set_index() to set the datetime column and df.resample() to calculate the monthly and annual statistics

import pandas as pd
import os


##############################################################################
# 1) generate the url for a given list of gage numbers
##############################################################################
myGageNums = ['06803495', '06803486']
myDates = ['2000-10-10', '2019-09-30']


# generate URL
def myURL(gageList, Dates):
    gages = ('&site_no={}' * len(gageList)).format(*gageList)
    period = f'&period=&begin_date={Dates[0]}&end_date={Dates[1]}'
    return f'https://waterdata.usgs.gov/nwis/dv?&cb_00060=on&format=rdb{gages}&referred_module=sw{period}'


##############################################################################
# 2) read this url and download the data to csv file
##############################################################################
# retrieve stream flow data from URL
# skip the first 29 rows as these rows are not data rows
# use tab '\t' delimiter
# from the remaining data rows, use the first row as the header
# add new header names
raw_df = pd.read_csv(myURL(myGageNums, myDates), skiprows=29, delimiter='\t', header=0, names=['Agency','Site','Date','Discharge_cfs','QualCode'])

raw_df.head(20)
raw_df.info()

# filter the dataframe so it includes only rows with 'USGS' data
df = raw_df[(raw_df['Agency']=='USGS')].copy()
df.head(20)

# create file path to save .csv file in current working directory
# dirPath = os.getcwd()
dirPath = r'C:\Users\rrohrer2\PythonNRES_WD\week 7'
fileName = 'USGS_Streamflow_Data.csv'
fullPath = os.path.join(dirPath, fileName)
print(fullPath)


# save fitered dataframe to .csv file
df.to_csv(fullPath, index=False)


##############################################################################
# 3) based on the downloaded data calculate the monthly stasticstics including
# maximum, minimum and average of the streamflow data and save it to another csv file.
# The data need to be formatted to 2 decimal digits. 
##############################################################################

# convert Date to datetime data type
df['Date']= pd.to_datetime(df['Date'])

df.info()
# change data frame index to 'Date'
# https://www.dataquest.io/blog/tutorial-time-series-analysis-with-pandas/
df = df.set_index(['Date'])

#https://datatofish.com/convert-string-to-float-dataframe/
df['Discharge_cfs'] = pd.to_numeric(df['Discharge_cfs'], errors='coerce')


###############################################################################
################ Calculate monthly statistics & write to file #################
###############################################################################
# https://chrisalbon.com/python/data_wrangling/pandas_group_data_by_time/
# http://benalexkeen.com/resampling-time-series-data-with-pandas/
# http://benalexkeen.com/resampling-time-series-data-with-pandas/
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.core.groupby.GroupBy.mean.html


# create dataframe for monthly statistics
monthlyStats = pd.DataFrame(columns=['Min','Max','Mean'])

monthlyStats.Min = df.Discharge_cfs.groupby(df['Site']).resample('M').min()
monthlyStats.Max = df.Discharge_cfs.groupby(df['Site']).resample('M').max()
monthlyStats.Mean = df.Discharge_cfs.groupby(df['Site']).resample('M').mean()


# pd.options.display.float_format = '{:.2f}'.format


monthlyStats.head(20)

# create file path to save .csv file in current working directory
# dirPath = os.getcwd()
fileName = 'monthlyStreamflowStats.csv'
fullPath = os.path.join(dirPath, fileName)

print(fullPath)

# save fitered dataframe to .csv file
monthlyStats.to_csv(fullPath, float_format='%.2f')


###############################################################################
############### Calculate average annual runoff for each gage #################
###############################################################################

#convert from 'cubic feet per second' to 'acre feet per day'
df['acreFeetPerDay'] = df['Discharge_cfs']*24*60*60/43560

yearlyTotal = pd.DataFrame(columns=['acreFeet'])
yearlyTotal.acreFeet = df.acreFeetPerDay.groupby(df['Site']).resample('A').sum()
yearlyTotal

# create file path to save .csv file in current working directory
# dirPath = os.getcwd()
fileName = 'annualAcreFeet.csv'
fullPath = os.path.join(dirPath, fileName)

print(fullPath)

# save fitered dataframe to .csv file
yearlyTotal.to_csv(fullPath, float_format='%.2f')



