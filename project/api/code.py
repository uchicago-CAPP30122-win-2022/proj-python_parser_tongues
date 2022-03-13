c.get_vax_data("cdc_data.csv", 1489959)
c.get_vax_data("cdc_data.csv")


from sodapy import Socrata
import csv
import pandas as pd 


def get_data(limit=3200):
    '''
    Connects to CDC Data Portal and extracts vaccine data into a csv file.
    Limit set to default of 3500 to retrieve data from all counties in the US.
    Input:
        (str): csv file name 
        (int): limit of data to retrieve
    '''

    client = Socrata("data.cdc.gov", "smYunORlSM3IrVMYZLiu6jfav") #Connection to CDC portal
    results = client.get("8xkx-amqh",limit=limit) #Get list of dicts(each row is a dict)
    data, latest_week, latest_date = find_recent_date(results)

    for county in data:
        for row in results:
            if int(row["mmwr_week"]) == latest_week and int(row["date"][8:10]) == latest_date:
                data[county]["fips"] = row["fips"]
                data[county]["state"] = row["recip_state"]
                data[county]["day"]= row["date"][8:10]
                data[county]["month"] = row["date"][5:7]
                data[county]["year"] = row["date"][:4]
                data[county]["week"] = row["mmwr_week"]
                data[county]["complete_pct"] = row["completeness_pct"]
                data[county]["complete_18plus_pct"] = row["series_complete_18pluspop_pct"]
                data[county]["complete_65plus_pct"] = row["series_complete_65pluspop_pct"]
                if "booster_doses_vax_pct" in row:
                    data[county]["booster_pct"] = row["booster_doses_vax_pct"]
                else:
                    data[county]["booster_pct"] = None
                if "booster_doses_18plus_vax_pct" in row:
                    data[county]["booster_18plus_pct"] = row["booster_doses_18plus_vax_pct"] 
                else:
                    data[county]["booster_18plus_pct"] = None
                if "booster_doses_65plus_vax_pct" in row:
                    data[county]["booster_65plus_pct"] = row["booster_doses_65plus_vax_pct"]
                else:
                    data[county]["booster_65plus_pct"] = None
                if "svi_ctgy" in row:
                    data[county]["svi"] = row["svi_ctgy"]
                else:
                    data[county]["svi"] = None
                if "metro_status" in row:
                    if row["metro_status"] == "Metro":
                        data[county]["metro_status"] = 1
                    else:
                        data[county]["metro_status"] = 0
                else:
                    data[county]["metro_status"] = None

    return data


def get_df(limit=3200):
    
    dic = get_data(limit)
    return pd.DataFrame.from_dict(dic)


def find_recent_date(results):
    '''
    Finds the most recent week and date of available data in the 
    CDC API.
    Input:
        (lst): list of dictionaries
    Output:
        (tuple): latest week, latest date
    '''
    data = {}
    latest_week = 0
    latest_date = 0

    for row in results:
        county = row["recip_county"]
        if county not in data:
            data[county] = {}
        if int(row["mmwr_week"]) > latest_week:
            latest_week = int(row["mmwr_week"])
        if int(row["date"][8:10]) > latest_date:
            latest_date = int(row["date"][8:10])

    return data, latest_week, latest_date