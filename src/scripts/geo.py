import requests
import json
import urllib

addr = [
    "3610+Hacks+Cross+Rd+Memphis+TN",  # depot
    "1921+Elvis+Presley+Blvd+Memphis+TN",
    "149+Union+Avenue+Memphis+TN",
    "1034+Audubon+Drive+Memphis+TN",
    "1532+Madison+Ave+Memphis+TN",
    "706+Union+Ave+Memphis+TN",
    "3641+Central+Ave+Memphis+TN",
    "926+E+McLemore+Ave+Memphis+TN",
    "4339+Park+Ave+Memphis+TN",
    "600+Goodwyn+St+Memphis+TN",
    "2000+North+Pkwy+Memphis+TN",
    "262+Danny+Thomas+Pl+Memphis+TN",
    "125+N+Front+St+Memphis+TN",
    "5959+Park+Ave+Memphis+TN",
    "814+Scott+St+Memphis+TN",
    "1005+Tillman+St+Memphis+TN",
]

for a in addr:
    request = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{a}.json?access_token=pk.eyJ1IjoieGF0aXNoYXl4IiwiYSI6ImNrdHR5OTl0aDA1YnEyb3A4MDQwNnY1MGQifQ.IhGx_ZkJaKRpzrhZu62iXg"
    jsonResult = urllib.request.urlopen(request).read()
    response = json.loads(jsonResult)
    # print("response: ", response)
    s = list(map(str, response["features"][0]["center"]))
    print(s, end=",")
