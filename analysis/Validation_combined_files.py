
import pandas as pd
import os
import glob
#update directory
os.chdir("C:/Users/*/Documents/Asthma SRO work/Combined QOF achievement/Raw")

#Create list of filenames to be appended
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

#read in the csv name list and add a column with the filename for al files in the folder selected above
df = pd.concat([pd.read_csv(all_filenames).assign(year=os.path.basename(all_filenames)) for all_filenames in all_filenames])

totals=df.groupby(['year','INDICATOR_CODE','MEASURE'])['VALUE'].sum()

totals_frame=totals.to_frame().reset_index()
totals_frame.columns=['Year','Indicator_code','Measure','Value']

##denom=totals_frame[(totals_frame['Measure'] == 'DENOMINATOR') & (totals_frame['Indicator_code'] == 'AST004')]
##num=totals_frame[(totals_frame['Measure'] == 'NUMERATOR') & (totals_frame['Indicator_code'] == 'AST007')]

#update directory
os.chdir("C:/Users/*/Documents/Asthma SRO work/Combined QOF achievement/")
totals_frame.to_csv('Combined_indicators_1819_1920_2021.csv',sep=',',header=True, index = False)




