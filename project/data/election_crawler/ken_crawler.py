'''
CAPP30122 W'22: Final Project - Election Site Crawler

Author: Ken Kliesner
3/16/2022
'''

import csv
import requests
import bs4


GENERAL_ELECTION = "https://uselectionatlas.org/RESULTS/data.php?year= \
                    2020&datatype=national&def=1&f=1&off=0&elect=0"
DOMAIN_URL = "https://uselectionatlas.org/RESULTS/"


def scrape(desired_filename="election_results.csv"):
    '''
    Run a report from scraping across all of the 2020 US Election Data from
    uselectionatlas.org and grab all of the results per state and per county
    to then be output in a CSV file.

    Input:
      desired_filename (str): a string containing the filename the user would
        like their csv to be saved as (must end in .csv). This is set with a
        default of "election_results.csv" if the user does not provide their
        own filename.
    
    Output:
      CSV file saved to the current directory, with name input to function.
    '''
    assert desired_filename.endswith(".csv")

    state_urls = find_state_urls(GENERAL_ELECTION)
    election_results = get_election_results(state_urls)
    write_csv(election_results, desired_filename)


#################### AUXILIARY FUNCTIONS ####################
def find_state_urls(url):
    '''
    Scrapes 2020 US Presidential Election full-country data map to find the
    urls for the pages of each individual state map.

    Input:
      url (str): url to scrape (GEN_ELECT: full 2020 US Election Results)
    
    Output:
      state_urls (dict): a dictionary mapping state keys to a url of their
        election results (states are full written-out words, not abbreviation).
    '''
    state_urls = {}
    soup = get_soup(url)
    if soup:
        all_state_data = soup.find_all("div")[1].form.table.tbody.tr.td. \
                         table.tbody.find_all("tr")
        for state_data in all_state_data:
            state = state_data.find_all("td", class_="name")[0].a.text
            each_st_url = state_data.find_all("td", class_="name")[0].a["href"]
            state_urls[state] = "".join((DOMAIN_URL, each_st_url))

    return state_urls


def get_election_results(state_urls):
    '''
    Main function to process each state's URL. It will take the state's URL and
    parse through each of the state's counties to find each candidate's results
    in percentage form.

    Input:
      state_urls (dict): a dictionary mapping state keys to a url of their
        election results (states are full written-out words, not abbreviation).

    Output:
      all_election_results (dict): a dictionary of nested dictionaries mapping
        each state to another dictionary of its counties, which are then mapped
        to a final dictionary of candidate keys mapped to their election
        results (in percentage form).
    '''
    all_election_results = {}
    for state, state_url in state_urls.items():
        state_gen_elections_soup = get_soup(state_url)
        if state_gen_elections_soup:
            state_gen_elect = state_gen_elections_soup.find_all("div")[1]. \
                              div.find_all("a")[1]["href"]
            state_gen_elections_link = "".join((DOMAIN_URL, state_gen_elect))
            all_state_county_data_soup = get_soup(state_gen_elections_link)
            if all_state_county_data_soup:
                st_cnty_data = all_state_county_data_soup.find_all("div")[1]. \
                               find_all("table")[0].find_all("table")[6]. \
                               find_all("li")[1].a["href"]
                all_st_cnty_data_link = "".join((DOMAIN_URL, st_cnty_data))
                individual_county_data_soup = get_soup(all_st_cnty_data_link)
                if individual_county_data_soup:
                    counties = individual_county_data_soup.div. \
                               div.find_all("table")
                    state_results = {}
                    for county in counties:
                        county_name = county.b.text
                        county_results = get_county_data(county)
                        state_results[county_name] = county_results
                    all_election_results[state] = state_results

    return all_election_results


def get_county_data(county):
    '''
    A helper function for get_election_results(), which goes down to the level
    of each candidate and extracts the necessary data, adding each candidate
    key mapped with their results to the output dictionary.

    Input:
      county ("table" tag): an HTML "table" tag for a given state that contains
        the election results for that county.

    Output:
      county_results (dict): a dictionary of candidate keys mapped to their
        election results (in percentage form).
    '''
    county_results = {}
    pierce_perc = 0.0
    for i, result in enumerate(county.tbody.find_all("tr")):
        if i == 0:  # Only for Biden, need bc of how programmer wrote HTML page
            cand_name = result.find_all("td", class_="cnd")[i].text
            cand_perc = float(result.find_all("td", class_="per")[i]. \
                              text.strip("%"))
        else:  # For all other candidates
            cand_name = result.td.text
            cand_perc = float(result.find_all("td", class_="per")[0]. \
                              text.strip("%"))
        
        if cand_name == "Pierce":
            pierce_perc = cand_perc
        elif cand_name == "Other":
            county_results[cand_name] = round(cand_perc + pierce_perc, 1)
        else:
            county_results[cand_name] = cand_perc
        
    if "Other" not in county_results:
        county_results["Other"] = pierce_perc
    
    county_winner = max(county_results, key=county_results.get)
    if county_winner == "Biden":
        county_results["Winner Dem?"] = 1
    else:
        county_results["Winner Dem?"] = 0
    
    return county_results


def get_soup(url):
    '''
    A helper function to find the bs4 soup object. It opens a connection to the
    specified URL, reads the data, and returns the needed soup.

    Input:
        url (str): the string of a specified URL.

    Output:
        soup (soup object): the HTML soup object or None if connection failed.
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
    Creates a CSV file in the current directory with the name provided to the
    scape() function. Contents will include each state, county, candidate
    results, and whether or not the winner of that county was a democrat (this
    is for purposes later in our color-coded map visualization).

    Input:
      election_dict (dict): a dictionary of nested dictionaries mapping each
        state to another dictionary of its counties, which are then mapped to a
        final dictionary of candidate keys mapped to their election results (in
        percentage form).
      output_filename (str): the name for the CSV to be created.

    Output:
      CSV file saved to the current directory, with name input to function.
    '''
    with open(output_filename, "w", newline="") as csvfile:
        elec_data = csv.writer(csvfile, delimiter = ",")
        elec_data.writerow(["State", "County", "Biden Vote %", "Trump Vote %", 
                            "Other Vote %", "Was Winner Democrat?"])
        for state, counties in election_dict.items():
            for county, results in counties.items():                
                elec_data = csv.writer(csvfile, delimiter=",")
                elec_data.writerow([state, county, results["Biden"], 
                                    results["Trump"], results["Other"], 
                                    results["Winner Dem?"]])
