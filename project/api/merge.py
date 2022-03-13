import pandas as pd
from api import cdc_county as c
from election_data import

#Retrieve CDC data from API
c.get_vax_data("cdc_data.csv")
#Convert csv files to pandas data frame
vax_data = pd.read_csv("cdc_data.csv")
elect_data = pd.read_csv("")

#result = pd.concat([vax_data, election_data], axis=1)
#result = pd.concat([vax_data, election_data], axis=1, join="inner")

#Merge datasets
df = pd.merge(vax_data, elect_data, on=["County", "key2"])
df.to_csv('merged_data.csv')