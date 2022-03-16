############### Ken's Implementation ##############


import csv
import pandas as pd
import requests
import bs4


dem_url = ("https://uselectionatlas.org/RESULTS/party.php?year=2020&type=national&no=1&f=1&off=0&elect=0")
rep_url = ("https://uselectionatlas.org/RESULTS/party.php?year=2020&type=national&no=2&f=1&off=0&elect=0")
############### Ken's Implementation ##############

# Come back to this commented out one later to add complexity
#GEN_ELECT_RESULTS = "https://uselectionatlas.org/RESULTS/national.php?year=2020&f=1&off=0&elect=0"
GEN_ELECT = "https://uselectionatlas.org/RESULTS/data.php?year=2020&datatype=national&def=1&f=1&off=0&elect=0"
DOMAIN_URL = "https://uselectionatlas.org/RESULTS/"


def go(desired_filename="election_results.csv", url=GEN_ELECT):
    '''
    Placeholder Docstring
    '''
    state_urls = find_state_urls(url)
    election_results = get_election_results(state_urls)
    write_csv(election_results, desired_filename)


##### MAIN SCRAPING FUNCTIONS #####

# Function to get each individual state's URL
def find_state_urls(url):
    '''
    Scrapes 2020 US Presidential Election data for a political party.

    Input:
        url (str): url to scrape (GEN_ELECT: full US 2020 US Election Results)
    Output:
      state_urls (dict): a dictionary mapping state keys to a url of their
        election results (states are full written-out words).
    '''

    # USE GEN_ELECT GLOBAL VARIABLE AS STARTING URL
    state_urls = {}
    soup = get_soup(url)
    if soup:
        all_state_data = soup.find_all("div")[1].form.table.tbody.tr.td.table.tbody.find_all("tr")
        for state_data in all_state_data:
            state = state_data.find_all("td", class_="name")[0].a.text
            each_state_url = state_data.find_all("td", class_="name")[0].a["href"]
            state_urls[state] = DOMAIN_URL + each_state_url

    return state_urls


# Main function to process URL
def get_election_results(state_urls):
    '''

    Input:
      state_urls (dict): a dictionary mapping state keys to a url of their election results. 

    Output:
      all_election_results (dict): a dictionary mapping each state to another
        dictionary of its counties, which are then mapped to candidates and
        their election results. 

    Example Output: 
      {
      'State1': 
        {'County1': {'Biden': '19.5%', 'Trump': '78.6%', 'Other': '1.7%'}, 
         'County2': {'Biden': '19.5%', 'Trump': '78.6%', 'Other': '1.7%'}}
      'Pennsylvania': 
        {'Teton': {'Biden': '67.1%', 'Trump': '29.6%', 'Other': '2.7%'},
         'Uinta': {'Biden': '16.9%', 'Trump': '79.7%', 'Other': '2.5%'}}
      }
    '''
    all_election_results = {}  # ALL OF THE US ELECTION RESULTS BY STATE
    for state, state_url in state_urls.items():
        state_gen_elections_soup = get_soup(state_url)
        if state_gen_elections_soup:
            state_gen_elections_link = DOMAIN_URL + state_gen_elections_soup.find_all("div")[1].div.find_all("a")[1]["href"]
            all_state_county_data_soup = get_soup(state_gen_elections_link)
            if all_state_county_data_soup:
                all_state_county_data_link = DOMAIN_URL + all_state_county_data_soup.find_all("div")[1].find_all("table")[0].find_all("table")[6].find_all("li")[1].a["href"]
                individual_county_data_soup = get_soup(all_state_county_data_link)
                if individual_county_data_soup:
                    counties = individual_county_data_soup.div.div.find_all("table")
                    state_results = {}  # ALL OF AN INDIVIDUAL STATE'S RESULTS BY COUNTY
                    for county in counties:
                        county_name = county.b.text
                        county_results = get_county_data(county)                      
                        state_results[county_name] = county_results
                    all_election_results[state] = state_results
                    
    return all_election_results


def get_county_data(county):
    '''
    '''
    county_results = {}  # ALL OF AN INDIVIDUAL COUNTY'S RESULTS BY CANDIDATE/PERCENTAGE
    default_perc = 0.0
    for i, result in enumerate(county.tbody.find_all("tr")):
        if i == 0:  # Biden, need bc of how page is written
            cand_name = result.find_all("td", class_="cnd")[i].text
            cand_perc = float(result.find_all("td", class_="per")[i].text.strip("%"))
        else:  # All other candidates
            cand_name = result.td.text
            cand_perc = float(result.find_all("td", class_="per")[0].text.strip("%"))
        
        if cand_name == "Pierce":
            default_perc = cand_perc
        elif cand_name == "Other":
            county_results[cand_name] = round(cand_perc + default_perc, 1)
        else:
            county_results[cand_name] = cand_perc
   
    default_perc = 0.0
    if "Other" not in county_results:
        county_results["Other"] = default_perc
    
    county_winner = max(county_results, key=county_results.get)
    if county_winner == "Biden":
        county_results["Winner Dem?"] = 1
    else:
        county_results["Winner Dem?"] = 0
    
    return county_results


# Helper just to get Soup
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
        soup = bs4.BeautifulSoup(s, "html5lib")
        return soup

def write_csv(election_dict, output_filename):
    '''
    Creates CSV file with the name provided to the function and with contents
    of the course identifier word indices.

    Puts together scraped 2020 US Presidential Election data with Democrat and
    Republican results into a csv file.


    Inputs:
        index_filename: the name for the CSV of the index.
        index_dict: dictionary mapping course identifiers to words

    Outputs:
        No outputs except for the creation of a new csv file with the 
        index_filename provided that is saved within the current directory.
    Input:
        (str): csv file name 
        (str): Democrat results url
        (str): Republican results url


    Example Dict Input:

    {'Rhode Island': {'Bristol': {'Biden': 63.5, 'Trump': 34.3, 'Other': 2.2},      
    'Kent': {'Biden': 52.8, 'Trump': 45.1, 'Other': 2.1},
    'Newport': {'Biden': 63.9, 'Trump': 34.1, 'Other': 2.0},
    'Providence': {'Biden': 60.5, 'Trump': 37.6, 'Other': 1.9},
    'Washington': {'Biden': 58.6, 'Trump': 39.2, 'Other': 2.2}},
    'Delaware': {'Kent': {'Biden': 51.2, 'Trump': 47.1, 'Other': 1.7},
    'New Castle': {'Biden': 67.8, 'Trump': 30.7, 'Other': 1.5},
    'Sussex': {'Biden': 43.8, 'Trump': 55.1, 'Other': 1.1}}}
    '''
    with open(output_filename, "w", newline="") as csvfile:
        #elec_data = csv.DictWriter(csvfile, delimiter = ",")
        elec_data = csv.writer(csvfile, delimiter = ",")
        elec_data.writerow(["State", "County", "Biden Vote %", "Trump Vote %", "Other Vote %", "Was Winner Democrat?"])

        for state, counties in election_dict.items():
            for county, results in counties.items():                
                elec_data = csv.writer(csvfile, delimiter=",")
                elec_data.writerow([state, county, results["Biden"], results["Trump"], results["Other"], results["Winner Dem?"]])
