import requests
import json
import re
from datetime import datetime

#https://ultrasignup.com/service/events.svc/closestevents?past=1&lat=39.7004&lng=-75.858&mi=200&mo=12&on

# this one is a litte bit different. based on some googles and inpsecting the website, it looks up the coordiantes of
# the location typed into the search. it then puts those coordinated into an service url used below.
# it returns json so not much scraping just json processing.
# to figure out the filters I had to inspect the code and html in the browser when picking options.
# notes on this can be found in the README

def parse():
   
    ## TODO: hone results by doing smaller radius with multiple locations
    # Lynchburg, DC, Annapolis, Baltimore, ...

    # final results in array of dictionary objects
    final = []

    URL = "https://ultrasignup.com/service/events.svc/closestevents?past=1&open=0&lat=39.0840&lng=-76.7002&mi=50&mo=12&on"
    
    page = requests.get(URL)
    
    races = page.json()
    
    for race in races:
        name = race["EventName"]
        #location = race["City"]+", "+race["State"]
        city = race["City"]
        state = race["State"]
        date = race["EventDate"]
        # format date object
        date_object = datetime.strptime(date, "%m/%d/%Y")
        distance=race["Distances"].split(",")
        
        final.append({"name": name, "distance":distance, "state":state, "city":city, "date": date_object, "website": "ultrasignup"})

    return final