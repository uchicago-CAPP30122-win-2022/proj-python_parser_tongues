from matplotlib.style import library
from sodapy import Socrata
from vaccines import Vaccines
import pandas as pd


class DataCollector: 

    def __init__(self):
        self.client = Socrata("data.cdc.gov", None) #Connection to CDC portal
        #self.client = Socrata("data.cdc.gov", "smYunORlSM3IrVMYZLiu6jfav") #Connection to CDC portal

    def get_data(self, limit):
        data = [] 
        results = self.client.get("unsk-b7fc",limit=limit) #Get list of dicts(each row is a dict)
        #print(results)
        # Convert to pandas DataFrame
        #results_df = pd.DataFrame.from_records(results)
        for dic in results: 
            vax_info = _decode_cdc_data(dic)
            data.append(vax_info)

        return data


# Decode into library object
def _decode_cdc_data(dct): 
    #Check all required attributes are inside the dictionary 
    if all (key in dct for key in ["date","location","distributed","dist_per_100k"]): #True if all attributes are present
        return Vaccines(dct["date"],dct["location"], dct["distributed"],dct["dist_per_100k"])
    return dct  
