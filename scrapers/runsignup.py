import requests
from bs4 import BeautifulSoup  
import re
from datetime import datetime

def parse():
    
    # final results in array of dictionary objects
    final = []

    # count of pages of webiste
    page_count = 1

    state = "MD"

    while(True):
        
        # url with page_count
        URL = f"https://runsignup.com/Races?name=&eventType=&radius=5&zipcodeRadius=&country=US&state={state}&distance=&max_distance=&units=K&start_date=2024-12-29&end_date=&page={page_count}"
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")
        
        # looks for element when no results are found, meaning we are at the end and jump out of the while loop
        if (soup.find("p", class_="fs-lg-1 margin-0") != None):
            break
        
        # races lists is in a tbody
        results = soup.tbody
        
        # list of all the races
        races = results.find_all('tr')

        # html_count of results since they added a anti-scraper thing at the end
        html_count=0
        for race in races:

            # we found the anti-scraper html before the end of the loop so break
            if ("Scraper" in race.text):
                break

            # element containing name and distance(s) of the race
            name_distance = race.find("div", class_="flex-1")

            # element containing time and date.
            # get text and clean it
            location_date = race.find_all("td",class_="ta-left fs-sm-2")
            date = location_date[0].text.strip()
            location = location_date[1].text.strip().replace("\n",", ")

            # use regex to get standarzied dates
            Match = re.search(r"(\w{3}) ([0-9\/]*)",date)
            # format date object
            date_object = datetime.strptime(Match.group(2), "%m/%d/%y")
            
            # use regex to get city and state
            Match = re.search(r"([A-Za-z !]+)([,]{1}) ([A-Z]{2}) ([A-Z]{2}), (\d{5})",location)
            city_text = Match.group(1)
            state_text = Match.group(3)

            # name is in an 'a' element
            name_element = name_distance.a

            # distance(s) is in a span element, default to list b/c it can have multiple
            distance_element_list = name_distance.find_all("span", class_="rsuVitamin")
            
            # temp list of distance text(s)
            tmp=[]
            for distance in distance_element_list:
                
                # append text to temp list
                tmp.append(distance.text)
            
            # add dictionary object to final list with name and list of distances
            final.append({"name": name_element.text, "distance":tmp, "state":state_text, "city":city_text, "date": date_object, "website": "runsignup"})
           
            html_count+=1
            
            # break when we've processed 25, since they append a 26th griefer result
            if (html_count == 25):
                break

        page_count += 1

        # for testing to limit number of records
        if page_count == 3:
            break
    
    return final