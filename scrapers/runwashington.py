import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def parse():
   
    # final results in array of dictionary objects
    final = []

    # while(True):
    URL = "https://www.runwashington.com/race-calendar/"
    page = requests.get(URL)
    
    soup = BeautifulSoup(page.content, "html.parser")
    
    # race list uses article element
    races = soup.find_all("article")
    
    for race in races:
        
        try:
            # date element uses class 'day'
            date_element = race.find("div",class_="day")
            # use contents to ignore the nested elements
            date = date_element.contents[0].strip()
            # get year
            current_year = datetime.now().year
            # format date object
            date_object = datetime.strptime(date + " " + str(current_year), "%B %d %Y")
        except:
            date_object = []

        # name element uses h3 
        name_element = race.h3
        name = name_element.text

        # location uses separate 'p' elements for street, city, and zip code
        location_element = race.find("div",class_="address").find_all("p")
        # we only want the city and want want to ignore nested elements with link to google maps
        location = location_element[2].contents[0].strip()

        try:
            # use regex to get city and state
            Match = re.search(r"([A-Za-z ]+)[,]{1} ([A-Za-z.]*) (\d{5})",location)
            print(name)
            print(Match)
            city_text = Match.group(1)
        
            match Match.group(2):
                case "Maryland":
                    state_text = "MD"
                case "Virginia":
                    state_text = "VA"
                case "D.C.":
                    state_text = "DC"
                case _:
                    state_text = ""

        except:
            city_text = "N/A"
            state_text = "N/A"
        
        try:
            # distances are in 'a' elements inside a div with class category
            distance_element_list = race.find("div",class_="category").find_all("a")
        except:
            distance_element_list = []

        # loop through list of distances and append them to tmp list
        tmp=[]
        for distance in distance_element_list:
            tmp.append(distance.text)
            
        # append everything to the dictionary obejct
        final.append({"name": name, "distance":tmp, "state":state_text, "city":city_text, "date": date_object, "website": "runwashington"})
        
        # for testing to limit number of records
        if len(races) == 3:
            break
    
    return(final)