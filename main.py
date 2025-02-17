import json

def data():
    from scrapers import runsignup, runwashington, ultrasignup

    # TODO: add better try catch blocks to scrapers to prevent full failure
    
    # do runsignup
    runsignup = runsignup.parse()

    # do runningintheusa
    runwashington = runwashington.parse()

    # do ultrasignup
    ultrasignup = ultrasignup.parse()

    all = runsignup + ultrasignup + runwashington

    return all

print(data())