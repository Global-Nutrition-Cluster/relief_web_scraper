import pandas as pd 
import requests
import json


url = "https://api.reliefweb.int/v1/jobs?appname=rwint-user-0&preset=latest&fields[include][]=source"
all_data = []

def getDataAllData():
    pageLimit = 1000
    param = {"limit":pageLimit}
    # Get the first 1000 rows
    response = requests.get(url, params=param)
    data = response.json()

    totalCount = data['totalCount']
    #all_data.extend(data.get("data", []))

    try:
        numberOfIterations = int(totalCount / 1000) + 1
    except Exception as e:
        print(e)
    
    for page in range(numberOfIterations):
        params = {
            "limit":pageLimit,
            "offset":pageLimit*page
        }
        response = requests.get(url, params=params)
        # test status
        dt = response.json()
        data = dt.get("data",[])
        for item in data:
            fields = item.get('fields',[])
            all_data.append(
                {
                    'id': item['id'],
                    'Organisation': fields['source'][0].get('name',None),
                    'Acronym': fields['source'][0].get('shortname',None),
                    'Type':  fields['source'][0]['type'].get('name', None),
                    'Website': fields['source'][0].get('homepage',None)
                }
            )

        # all_data.extend(dt.get("data", []))
    
    df = pd.DataFrame(all_data)
    df.to_excel('relief_web_orgs_data.xlsx', index=False)
    return 0


if __name__ == "__main__":
    getDataAllData()