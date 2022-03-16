import pandas as pd
import numpy as np

# Build FIPS classifier to categorize counties
df_fips = pd.read_csv("data/fips_codes.csv",dtype=str)
fips_classifier = {}
for _, row in df_fips.iterrows():
    if row["County"] not in fips_classifier:
        fips_classifier[row["FIPS"]] = (row["State"], row["County"])

#Retrieve CDC data from API
vax_data = pd.read_csv("data/cdc_data.csv", dtype=str)

#Retrieve election data
elect_data = pd.read_csv("data/2020_election_results.csv",dtype=str).rename(columns={"Biden Vote %": "DEM", 
"Trump Vote %": "REP", "Was Winner Democrat?": "DEM_WON"})

#Add FIPS code to facilitate merging
elect_data["FIPS"] = elect_data["County"]
for fips, (state, county) in fips_classifier.items():
    elect_data["FIPS"] = np.where((elect_data["State"] == state) & (elect_data["County"] == county),
    fips, elect_data["FIPS"])
elect_data = elect_data.drop(columns=["State", "County"])

# Retrieve controls dataset
controls = pd.read_csv("data/controls.csv", dtype=str).drop(columns=["POP", "Unnamed: 4"])
controls["INCOME"] = controls["INCOME"].str.replace(',','')

#Merge datasets
# Left Merge
df = pd.merge(vax_data, elect_data, how='left', on = "FIPS")
df = df.rename(columns={"State_x":"State","County_x":"County"}).sort_values("FIPS")
df.drop(df[df["FIPS"] == "UNK"].index, inplace = True) # Drop observations with unknown FIPS codes
df2 = pd.merge(df, controls, how='left', on = "FIPS")

#Convert merged df's to csv
df2.to_csv('data.csv')
    
