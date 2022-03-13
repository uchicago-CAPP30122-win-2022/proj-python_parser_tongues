import pandas as pd
import numpy as np
from cdc_api import cdc_county as c


# Build FIPS classifier to categorize counties
df_fips = pd.read_csv("fips_codes.csv",dtype=str)
fips_classifier = {}
for _, row in df_fips.iterrows():
    if row["County"] not in fips_classifier:
        fips_classifier[row["County"]] = row["FIPS"]

#Retrieve CDC data from API
c.get_vax_data("cdc_data.csv")
vax_data = pd.read_csv("cdc_data.csv")

#Retrieve election data
elect_data = pd.read_csv("ken_test.csv")
#Add FIPS code to facilitate merging
elect_data["FIPS"] = elect_data["County"]
for county in fips_classifier:
    elect_data["FIPS"] = np.where((elect_data.FIPS == county),fips_classifier[county],elect_data.FIPS)
  
#Merge datasets
# Generates 4444 rows
df_2 = pd.merge(vax_data, elect_data, how='inner', on = "FIPS")
# Generates 2961 rows
df_3 = pd.merge(vax_data, elect_data, how='left', on = "FIPS")

#Convert to csv
df_2.to_csv('merged_data.csv')
df_3.to_csv('merged_data_duplicates.csv')
    