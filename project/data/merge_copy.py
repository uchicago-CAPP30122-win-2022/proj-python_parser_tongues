import pandas as pd
import numpy as np
from cdc_api import cdc_county as c

# Build classifier matching state names to state codes
df_abb = pd.read_csv("abbreviations.csv")
state_abb = {}
for _, row in df_abb.iterrows():
    if row["Abbreviation"] not in state_abb:
        state_abb[row["Abbreviation"]] = row["State"]

# Build FIPS classifier to categorize counties
df_fips = pd.read_csv("fips_codes.csv",dtype=str)
fips_classifier = {}
for _, row in df_fips.iterrows():
    if row["County"] not in state_abb:
        fips_classifier[row["County"]] = row["FIPS"]

#Retrieve CDC data from API
c.get_vax_data("cdc_data.csv")
vax_data = pd.read_csv("cdc_data.csv")
#Replace state abbreviations with state names using classifier
for state in state_abb:
    vax_data = vax_data.replace([state],state_abb[state])
# Remove string "County"
vax_data["County"] = vax_data["County"].map(lambda x: x.lstrip('County'))

#Retrieve election data
elect_data = pd.read_csv("ken_test.csv")
#Add FIPS code to facilitate merging
elect_data["FIPS"] = elect_data["County"]
for county in fips_classifier:
    elect_data["FIPS"] = np.where((elect_data.FIPS == county),fips_classifier[county],elect_data.FIPS)
  
#Merge datasets
# Generates 4444 rows
df_2 = pd.merge(vax_data, elect_data, how='inner', on = "FIPS")
df_2 = df_2.rename(columns={"State_x":"State","County_x":"County"})
# Generates 2961 rows
df_3 = pd.merge(vax_data, elect_data, how='left', on = "FIPS")
df_3 = df_3.rename(columns={"State_x":"State","County_x":"County"})

#Convert to csv
df_2.to_csv('merged_data.csv')
df_3.to_csv('merged_data_duplicates.csv')