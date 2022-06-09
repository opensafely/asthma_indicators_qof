import pandas as pd
import os
import glob
from cohortextractor import Measure
from utilities import *
#update directory
os.chdir("C:/Users/higginsr/Documents/GitHub/asthma_indicators_qof/output")

measures_dict = {}
for m in measures:
    measures_dict[m.id] = m

#Create list of filenames to be appended
extension = 'csv'
all_filenames = [i for i in glob.glob('rate_table_{value.group_by[0]}.csv'.format(extension))]

#read in the csv name list and add a column with the filename for al files in the folder selected above
df = pd.concat([pd.read_csv(all_filenames).assign(file_name=os.path.basename(all_filenames)) for all_filenames in all_filenames])

df.head(5)









