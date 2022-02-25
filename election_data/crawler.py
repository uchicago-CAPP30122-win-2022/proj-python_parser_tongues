import csv
import pandas as pd
import requests
import bs4


dem_url = ("https://uselectionatlas.org/RESULTS/party.php?year=2020&type=national&no=1&f=1&off=0&elect=0")
rep_url = ("https://uselectionatlas.org/RESULTS/party.php?year=2020&type=national&no=2&f=1&off=0&elect=0")



def get_elect_data(dem_url, rep_url):
    '''
    Puts together scraped 2020 US Presidential Election data with Democrat and
    Republican results into a csv file.
    Input:
        (str): Democrat results url
        (str): Republican results url
    Output:
        (dict): nested dictionary with election data
    '''

    dem_data = get_party_data(dem_url)
    rep_data = get_party_data(rep_url)

    data = {}

    for list in dem_data:
        state = list[0]
        if state not in data:
            data[state] ={}
        data[state]["Electoral Votes"] = list[1]
        data[state]["Total Votes"] = list[2]
        data[state]["Dem Votes"] = list[4]
    
    for list in rep_data:
        state = list[0]
        data[state]["Rep Votes"] = list[4]

    return data


def data_to_csv(output_filename, dem_url, rep_url):
    '''
    Puts together scraped 2020 US Presidential Election data with Democrat and
    Republican results into a csv file.
    Input:
        (str): csv file name 
        (str): Democrat results url
        (str): Republican results url
    '''
    
    dem_data = get_party_data(dem_url)
    rep_data = get_party_data(rep_url)

    data = {}

    with open(output_filename, "w") as csvfile:
        elec_data = csv.writer(csvfile, delimiter = ",")
        elec_data.writerow(["State", "Electoral Votes", "Total Votes", "Dem Votes", "Rep Votes"])

        for list in dem_data:
            state = list[0]
            if state not in data:
                data[state] ={}
            elec_votes = list[1]
            total_votes = list[2]
            dem_votes = list[4]
            data[state]["Electoral Votes"] = elec_votes
            data[state]["Total Votes"] = total_votes
            data[state]["Dem Votes"] = dem_votes
            elec_data.writerow([state, elec_votes, total_votes, dem_votes])
    
        for list in rep_data:
            state = list[0]
            data[state]["Rep Votes"] = list[4]



def data_to_pd(dem_url, rep_url):
    '''
    Puts together scraped 2020 US Presidential Election data with Democrat and
    Republican results.
    Input:
        (str): Democrat results url
        (str): Republican results url
    Output:
        (pd DataFrame): data frame with election data
    '''
    
    dem_data = get_party_data(dem_url)
    rep_data = get_party_data(rep_url)

    data = {}

    for list in dem_data:
        state = list[0]
        if state not in data:
            data[state] ={}
        data[state]["Electoral Votes"] = list[1]
        data[state]["Total Votes"] = list[2]
        data[state]["Dem Votes"] = list[4]
    
    for list in rep_data:
        state = list[0]
        data[state]["Rep Votes"] = list[4]

    return pd.DataFrame.from_dict(data).T.apply(pd.to_numeric)


def get_party_data(url):
    '''
    Scrapes 2020 US Presidential Election data for a political party.
    Input:
        (str): url to scrape (Democratic or Republican Results)
    Output:
        (lst): a list of lists where each sublist represent data for a 
        particular state.
    '''

    if get_soup(url) is not None:
        soup = get_soup(url)
        
        data = []
        for tag in soup.find_all("table", border="2", cellspacing="1", class_="data"):
            for entry in tag.find_all("tr")[1:]:
                row = []
                for col in entry.find_all("td")[1:6]:
                    row.append(col.text.replace(',', ''))
                data.append(row)

    return data
       

def get_soup(url):
    '''
    Opens a connection to the specified URL, reads data and makes soup.

    Inputs:
        (str): URL

    Outputs:
        (soup object)/ None: Soup or None if connection failed
    '''
  
    r = requests.get(url)
    if r.status_code == 404 or r.status_code == 403:

        return None
    else:
        s = r.text.encode('iso-8859-1')
        soup = bs4.BeautifulSoup(s,  "html5lib")

        return soup