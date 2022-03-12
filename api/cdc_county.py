from sodapy import Socrata
import csv


def get_vax_data(output_filename, limit=3200):
    '''
    Connects to CDC Data Portal and extracts vaccine data into a csv file.
    Limit set to default of 3200 to get data from all 3006 counties in the US.
    Input:
        (str): csv file name 
        (int): limit of data to retrieve
    '''

    client = Socrata("data.cdc.gov", "smYunORlSM3IrVMYZLiu6jfav") #Connection to CDC portal
    results = client.get("8xkx-amqh",limit=limit) #Get list of dicts(each row is a dict)
    weeks = set()
    dates = set()
    
    with open(output_filename, "w") as csvfile:
        vax_data = csv.writer(csvfile, delimiter = ",")
        vax_data.writerow(["FIPS", "State", "County", "Day",  "Month", "Year", "Week", 
        "Completeness Percent", "Complete 18 Plus Percent", "Complete 65 Plus Percent",
         "Booster Percent", "Booster 18 Plus Percent", "Booster 65 Plus Percent", "SVI", 
         "Metro Status"])
        
        #Retrieve only most recent data by mmwrk week and date
        for row in results:
            weeks.add(row["mmwr_week"])
            dates.add(row["date"][8:10])
 
        latest_week = max(weeks)
        recent_date = max(dates)

        for row in results:
            if row["mmwr_week"] == latest_week and row["date"][8:10] == recent_date:
                fips = row["fips"]
                state = row["recip_state"]
                county = row["recip_county"]
                day = row["date"][8:10]
                month = row["date"][5:7]
                year = row["date"][:4]
                week = row["mmwr_week"]
                complete_pct = row["completeness_pct"]
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
                    metro_status = row["metro_status"]
                else:
                    metro_status = None
                vax_data.writerow([fips, state, county, day, month, year, week, complete_pct, 
                complete_18plus_pct,complete_65plus_pct, booster_pct, booster_18plus_pct, 
                booster_65plus_pct, svi, metro_status]) 