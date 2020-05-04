import pandas as pd
import os

# 2. Use Pandas to:

###############################################################################
# 1. Read data in users.zip (using Pandas' the on-the-fly decompression capability)
###############################################################################

# create file path to save .csv file in current working directory
dirPath = os.getcwd()
# dirPath = r'C:\Users\rrohrer2\PythonNRES_WD\week 7'
fileName = 'users.zip'
fullPath = os.path.join(dirPath, fileName)

# read text file from zip file
userData = pd.read_csv(fullPath, compression= 'zip', sep='|')
userData = userData.set_index('user_id')

userData.info()
###############################################################################
# # 2. Identify all the occupations and compare the user numbers between STEM-related occupations and non-STEM occupations.
###############################################################################

stemList = ('engineer','programmer','scientist','technician')

stemTotal = 0
for item in stemList:    
    num = len(userData[userData["occupation"] == item])
    print(f'{item} = {num}')
    stemTotal += num

totalAll = len(userData.index)
nonStemTotal = totalAll - stemTotal

print('total = ', totalAll)  
print('total STEM-related = ', stemTotal)
print('non STEM-related = ', nonStemTotal)

###############################################################################
# 3. Identify the lcoations of the user that are programmers and above 35. How many male and female programmers, respecively?
#    Is this ratio the same for the age under 35?
###############################################################################

# create dataframe for monthly statistics
programmerAgeHigh = userData.query('occupation == "programmer" & age > 35').groupby(userData['gender']).count()
maleProgrammersAgeHigh = programmerAgeHigh['gender']['M']
femaleProgrammersAgeHigh = programmerAgeHigh['gender']['F']
programmersAgeHighRatio = f'{maleProgrammersAgeHigh/femaleProgrammersAgeHigh:.2f}'

print(f"number of male programmers over 35 = {maleProgrammersAgeHigh}")
print(f"number of male programmers over 35 = {femaleProgrammersAgeHigh}")
print(f"ratio of male to femail programmers over 35 = {programmersAgeHighRatio}\n")


programmerAgeLow = userData.query('occupation == "programmer" & age <= 35').groupby(userData['gender']).count()
maleProgrammersAgeLow = programmerAgeLow['gender']['M']
femaleProgrammersAgeLow = programmerAgeLow['gender']['F']
programmersAgeLowRatio = f'{maleProgrammersAgeLow/femaleProgrammersAgeLow:.2f}'

print(f"number of male programmers 35 & under= {maleProgrammersAgeLow}")
print(f"number of male programmers 35 & under = {femaleProgrammersAgeLow}")
print(f"ratio of male to femail programmers 35 & under = {programmersAgeLowRatio}\n")

###############################################################################
# 4. Compare the numbers of male and female for each occupation
###############################################################################

programmerOccupationStats = userData.groupby(['occupation','gender'])['gender'].count()
# programmerOccupationStats.rename(columns = {'age':'count'}, inplace=True)
# programmerOccupationStats = programmerOccupationStats.drop(['zip_code'], axis='columns')
print(programmerOccupationStats)

###############################################################################
# 5. Find the occupations with the youngest and oldest 'mean' ages, respectively
###############################################################################

meanAges = userData.groupby(['occupation'])['age'].mean()
print(meanAges.sort_values().round(decimals=2),'\n')

print(f'{meanAges.idxmin()} is the occupation with the youngest mean age of {meanAges.min():.1f} years')
print(f'{meanAges.idxmax()} is the occupation with the oldest mean age of {meanAges.max():.1f} years\n')

###############################################################################
# 6. Based on the first two digits of the zip codes, find the area with the largest numbers of users.
###############################################################################

# sortByZip = userData.sort_values(by=['zip_code'])
userData['shortZip'] = userData['zip_code'].str[:2]
numUsers = userData.groupby(['shortZip'])['occupation'].count()
print(f"the largest number of users is in zip code prefix '{numUsers.idxmax()}'")
