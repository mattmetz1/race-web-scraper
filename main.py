import json

def data():
    from scrapers import runsignup, runwashington, ultrasignup

    
    # do runsignup
    runsignup = runsignup.parse()

    # do runningintheusa
    runwashington = runwashington.parse()

    ultrasignup = ultrasignup.parse()

    all = runsignup + ultrasignup + runwashington

    
    
    
    
    return all

print(data())