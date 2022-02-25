import csv
import requests
import bs4


def get_data():

    url = ("https://www.presidency.ucsb.edu/statistics/elections/2020")
    #limiting_domain = "presidency.ucsb.edu"

    if get_soup(url) is not None:
        soup = get_soup(url)
        links = soup.find_all("a")
        #divs = links = soup.find_all("div")
        div = soup.find_all("div", class_ = 'field-body')
        td = soup.find_all("td")
        tr = soup.find_all("tr")
    
    dic = {} #Get states
    for t in td:
        if t.a is not None:
            for state in t.a:
                if state not in dic:
                    dic[state] = {}
    
    for parent in dic.keys():
        pass

    for t in td:
        if t.a is not None and state in dic.keys:
            for state in t.a:
                print(state)
                parent = state
                print(parent.next_sibling)

    for t in td:
        if t.find("p", align = 'right') is not None:
            t.find("p", align = 'right').text
    
    for t in td:
        for data in t:
            print(data)
 

        


    for i in links:
        for string in i:
            if string == "Alabama":
                print(string)
        

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
    
    