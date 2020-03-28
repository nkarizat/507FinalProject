# Uniqname: nkarizat
# Name: Nadia Karizat

import requests


def total_tested():
    url = "https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/testing-in-us.html?CDC_AA_refVal=https%3A%2F%2Fwww.cdc.gov%2Fcoronavirus%2F2019-ncov%2Ftesting-in-us.html"

    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)

    print(response.text.encode('utf8'))
    
total_tested()
