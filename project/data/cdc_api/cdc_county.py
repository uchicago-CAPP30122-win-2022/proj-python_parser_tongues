from sodapy import Socrata
import pandas as pd
import csv


def get_results(limit):
    '''
    Given a limit of data to retrieve, produces result object from CDC API.
    Input:
        (int): the limit
    Output:
        (list): list of dictionaries with retrieved data
    '''

    client = Socrata("data.cdc.gov", "smYunORlSM3IrVMYZLiu6jfav") #Connection to CDC portal
    results = client.get("8xkx-amqh",limit=limit) #Get list of dicts(each row is a dict)

    return results 


def get_vax_data(output_filename, limit=3200):
    '''
    Connects to CDC Data Portal and extracts vaccine data into a csv file.
    Limit set to default of 3500 to retrieve data from all counties in the US.
    Input:
        (str): csv file name 
        (int): limit of data to retrieve
    '''
    results = get_results(limit)
    latest_week, latest_date, _ = find_recent_date(results)
    
    with open(output_filename, "w") as csvfile:
        vax_data = csv.writer(csvfile, delimiter = ",")
        vax_data.writerow(["FIPS", "STATE", "COUNTY", "GEN_VAX_RATE", "COUN_VAX_RATE", 
        "COMP_RATE_18UP", "COMP_RATE_65UP","BOOSTER_RATE", "BOOSTER_RATE_18UP", 
        "BOOSTER_RATE_65UP", "SVI", "IS_METRO", "POP", "POP_18UP", "POP_65UP"])

        for row in results:
            if int(row["mmwr_week"]) == latest_week and int(row["date"][8:10]) == latest_date:
                fips = row["fips"]
                state = row["recip_state"]
                county = row["recip_county"]
                state_complete = row["completeness_pct"]
                county_complete = row["series_complete_pop_pct"]
                complete_18plus_pct = row["series_complete_18pluspop_pct"]
                complete_65plus_pct = row["series_complete_65pluspop_pct"]
                if "booster_doses_vax_pct" in row:
                    booster_pct = row["booster_doses_vax_pct"]
                else:
                    booster_pct = None
                if "booster_doses_18plus_vax_pct" in row:
                    booster_18plus_pct = row["booster_doses_18plus_vax_pct"] 
                else:
                    booster_18plus_pct = None
                if "booster_doses_65plus_vax_pct" in row:
                    booster_65plus_pct = row["booster_doses_65plus_vax_pct"]
                else:
                    booster_65plus_pct = None
                if "svi_ctgy" in row:
                    svi = row["svi_ctgy"]
                else:
                    svi = None
                if "metro_status" in row:
                    if row["metro_status"] == "Metro":
                        metro_status = 1
                    else:
                        metro_status = 0
                else:
                    metro_status = None
                if "census2019" in row:
                    pop = row["census2019"]
                else:
                    pop = None
                if "census2019_18pluspop" in row:
                    pop_18plus = row["census2019_18pluspop"]
                else:
                    pop_18plus = None
                if "census2019_65pluspop" in row:
                    pop_65plus = row["census2019_65pluspop"]
                else:
                     pop_65plus = None
                vax_data.writerow([fips, state, county, state_complete, county_complete, 
                complete_18plus_pct,complete_65plus_pct, booster_pct, booster_18plus_pct, 
                booster_65plus_pct, svi, metro_status, pop, pop_18plus, pop_65plus]) 


def find_recent_date(results):
    '''
    Finds the most recent week and date of available data in the 
    CDC API.
    Input:
        (lst): list of dictionaries
    Output:
        (tuple): latest week, latest date
    '''

    latest_week = 0
    latest_date = 0
    data = {}

    for row in results:
        county = row["recip_county"]
        if county not in data:
             data[county] = {}
        if int(row["mmwr_week"]) > latest_week:
            latest_week = int(row["mmwr_week"])
        if int(row["date"][8:10]) > latest_date:
            latest_date = int(row["date"][8:10])
         

    return latest_week, latest_date, data


def get_sample_data(limit):
    '''
    Connects to CDC Data Portal and extracts vaccine data for the project.
    Input:
        (int): limit of data to retrieve
    Output:
        (pd DataFrame): dataframe sorted in ascending order by county.
    '''
    results = get_results(limit)
    latest_week, latest_date, data = find_recent_date(results)

    
    for county in data:
        for row in results:
            if int(row["mmwr_week"]) == latest_week and int(row["date"][8:10]) == latest_date and row["recip_county"] == county:
                data[county]["FIPS"] = row["fips"]
                data[county]["State"] = row["recip_state"]
                data[county]["Day"] = row["date"][8:10]
                data[county]["Month"] = row["date"][5:7]
                data[county]["Year"] = row["date"][:4]
                data[county]["Week"] = row["mmwr_week"]
                data[county]["Completeness Percent"] = row["series_complete_pop_pct"]
                data[county]["Complete 18 Plus Percent"] = row["series_complete_18pluspop_pct"]
                data[county]["Complete 65 Plus Percent"] = row["series_complete_65pluspop_pct"]
                data[county]["Booster Percent"] = row["booster_doses_vax_pct"]
                data[county]["Booster 18 Plus Percent"] = row["booster_doses_18plus_vax_pct"] 
                data[county]["Booster 65 Plus Percent"] = row["booster_doses_65plus_vax_pct"]
                if "svi_ctgy" in row:
                    data[county]["SVI"] = row["svi_ctgy"]
                else:
                    data[county]["SVI"] = None
                data[county]["Metro Status"] = row["metro_status"]
                data[county]["Population"] = row["census2019"]
                data[county]["Population 18 Plus"] = row["census2019_18pluspop"]
                data[county]["Population 65 Plus"] = row["census2019_65pluspop"]

    return pd.DataFrame.from_dict(data).T.sort_index(ascending=True)
