import pandas as pd
import numpy as np
from cdc_api import cdc_county as c

# Build FIPS classifier to categorize counties
df_fips = pd.read_csv("fips_codes.csv",dtype=str)
fips_classifier = {}
for _, row in df_fips.iterrows():
    if row["County"] not in fips_classifier:
        fips_classifier[row["FIPS"]] = (row["State"], row["County"])

#Retrieve CDC data from API
c.get_vax_data("cdc_data.csv")
vax_data = pd.read_csv("cdc_data.csv")


#Retrieve election data
elect_data = pd.read_csv("ken_test.csv")
#Add FIPS code to facilitate merging
elect_data["FIPS"] = elect_data["County"]
for fips, (state, county) in fips_classifier.items():
    elect_data["FIPS"] = np.where((elect_data["State"] == state) & (elect_data["County"] == county),
    fips, elect_data["FIPS"])
elect_data = elect_data.drop(columns=["State", "County"])

#Merge datasets
# Inner Merge
df_1 = pd.merge(vax_data, elect_data, how='inner', on = "FIPS")
df_1 = df_1.rename(columns={"State_x":"State","County_x":"County"})
# Left Merge
df_2 = pd.merge(vax_data, elect_data, how='left', on = "FIPS")
df_2 = df_2.rename(columns={"State_x":"State","County_x":"County"})

#Convert merged df's to csv
df_1.to_csv('inner_merged.csv')
df_2.to_csv('left_merged.csv')
    