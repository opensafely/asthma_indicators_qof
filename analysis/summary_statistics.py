from attr import Attribute
import pandas as pd
import numpy as np
from utilities import *
from config import year_end_list, demographics
import glob


# these are not generated in the main generate measures action
# additional_indicators = ["e", "f"]
#  indicators_list.extend(additional_indicators)


# total numerator and denominator values
df_total = pd.read_csv(os.path.join(OUTPUT_DIR, f'rate_table_total.csv'))
df_total_year_end = df_total[(df_total['date'] == '2019-03-01') | (df_total['date'] == '2020-03-01') | (
    df_total['date'] == '2021-03-01') | (df_total['date'] == '2022-03-01')].assign(attribute="Total", category='')

demo_list = []
for i in demographics:

    df = pd.read_csv(os.path.join(
        OUTPUT_DIR, 'joined', f'measure_{i}_rate.csv')).assign(attribute=i)
    df = df.rename(columns={f'{i}': 'category'})
    new_cols = ["attribute", "category",
                "ast007_num", "ast007_denom", "value", "date"]
    df = df.reindex(columns=new_cols)
    demo_list.append(df)

test = pd.concat(demo_list, keys=demographics)
print(test)

# demo_list.append(df)

# test = pd.concat(demo_list, keys=demographics, join='outer')
# print(test)

# run code in a shell in terminal using tw lines of code below
# import code
# code.interact(local=locals())


# Age num and denom
# df_age = pd.read_csv(os.path.join(OUTPUT_DIR, f'rate_table_age_band.csv'))
# df_age_year_end = df_age[(df_age['date'] == '2019-03-01') | (df_age['date'] == '2020-03-01') | (
#     df_age['date'] == '2021-03-01') | (df_age['date'] == '2022-03-01')].assign(attribute='Age')
# df_age_year_end = df_age_year_end.rename(columns={'age_band': 'category'})
# new_age_cols = ["attribute", "category",
#                 "ast007_num", "ast007_denom", "value", "date"]
# df_age_year_end = df_age_year_end.reindex(columns=new_age_cols)


# Sex num and denom
# df_sex = pd.read_csv(os.path.join(OUTPUT_DIR, f'rate_table_sex.csv'))
# df_sex_year_end = df_sex[(df_sex['date'] == '2019-03-01') | (df_sex['date'] == '2020-03-01') | (
#     df_sex['date'] == '2021-03-01') | (df_sex['date'] == '2022-03-01')].assign(attribute='Sex')
# df_sex_year_end = df_sex_year_end.rename(columns={'sex': 'category'})
# new_sex_cols = ["attribute", "category",
#                 "ast007_num", "ast007_denom", "value", "date"]
# df_sex_year_end = df_sex_year_end.reindex(columns=new_sex_cols)


# Combine all tables
# all_tables = [df_age_year_end, df_sex_year_end]

# df_combined = pd.concat(all_tables)

# df_combined.to_csv(os.path.join(
#     OUTPUT_DIR, f'combined_results.csv'), sep=',', header=True, index=False)



# def combined_results_read():
#     df = pd.read_csv(os.path.join(OUTPUT_DIR, f'combined_results.csv')
#                      )
#     return df
