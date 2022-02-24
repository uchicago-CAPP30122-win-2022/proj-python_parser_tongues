from sodapy import Socrata
import pandas as pd
import csv


def get_all_data(limit): # Returns all variables
    '''
    Connects to CDC Data Portal and extracts all vaccine data for the project into
    a Pandas DataFrame.
    Input:
        (int): limit of data to retrieve
    Output:
        (pd DataFrame): extracted vaccine data
    '''
    client = Socrata("data.cdc.gov", "smYunORlSM3IrVMYZLiu6jfav") #Connection to CDC portal
    results = client.get("unsk-b7fc",limit=limit) #Get list of dicts(each row is a dict)
    df = pd.DataFrame.from_records(results)

    return df 


def get_vax_data(limit):
    '''
    Connects to CDC Data Portal and extracts vaccine data for the project.
    Input:
        (int): limit of data to retrieve
    Output:
        (dict): nested dictionary with vaccine data
    '''
    client = Socrata("data.cdc.gov", "smYunORlSM3IrVMYZLiu6jfav") #Connection to CDC portal
    results = client.get("unsk-b7fc",limit=limit) #Get list of dicts(each row is a dict)
    data = {}
    weeks = set()
    dates = set()

    for row in results:
        weeks.add(row["mmwr_week"])
        dates.add(row["date"][8:10])
        state = row["location"]
        if state not in data:
            data[state] = {}
        else:
            pass
        
    latest_week = max(weeks)
    recent_date = max(dates)

    for state in data:
        for row in results:
            if row["mmwr_week"] == latest_week and row["date"][8:10] == recent_date:
                data[state]["date"] = row["date"]
                data[state]["week"] = row["mmwr_week"]
                data[state]["administered"] = row["administered"]
                data[state]["admin_per_100k"] = row["admin_per_100k"]
                data[state]["admin_per_100k_18plus"] = row["admin_per_100k_18plus"]
                data[state]["series_complete_18plus"] = row["series_complete_18plus"]
                data[state]["series_complete_18pluspop"] = row["series_complete_18pluspop"]

    return data


def get_to_pd(limit): # Returns all variables
    '''
    Converts vaccine data from a dictionary to a Pandas DataFrame.
    Input:
        (int): limit of data to retrieve
    Output:
        (pd DataFrame): data frame with vaccine data
    '''
    dic = get_vax_data(limit)
    return pd.DataFrame.from_dict(dic)


def to_csv(output_filename, limit):
    '''
    Connects to CDC Data Portal and extracts vaccine data into a csv file.
    Input:
        (str): csv file name 
        (int): limit of data to retrieve
    '''

    client = Socrata("data.cdc.gov", "smYunORlSM3IrVMYZLiu6jfav") #Connection to CDC portal
    results = client.get("unsk-b7fc",limit=limit) #Get list of dicts(each row is a dict)
    data = {}
    weeks = set()
    dates = set()
    
    with open(output_filename, "w") as csvfile:
        vax_data = csv.writer(csvfile, delimiter = ",")
        vax_data.writerow(["State", "Date", "Week", "Administered", "Admin_per_100k", "Admin_per_100k_18plus", "Series_complete_18plus", "Series_complete_18pluspop"])
        
        for row in results:
            weeks.add(row["mmwr_week"])
            dates.add(row["date"][8:10])
        
        latest_week = max(weeks)
        recent_date = max(dates)

        for row in results:
            if row["mmwr_week"] == latest_week and row["date"][8:10] == recent_date:
                state = row["location"]
                date = row["date"]
                week = row["mmwr_week"]
                administered = row["administered"]
                admin_100k = row["admin_per_100k"]
                admin_100k_18plus = row["admin_per_100k_18plus"]
                complete_18plus = row["series_complete_18plus"]
                complete_18pluspop = row["series_complete_18pluspop"]
                vax_data.writerow([state, date, week, administered, admin_100k,admin_100k_18plus, complete_18plus,complete_18pluspop])     