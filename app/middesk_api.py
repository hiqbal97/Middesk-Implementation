import requests
import json
import os
from urllib.parse import urlparse
import pandas
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def createBusiness(name, address1, address2, city, state, zip, website, tin):
    headers = {
    # Already added when you pass json=
    # 'Content-Type': 'application/json',
    }

    json_data = {
        'name': name,
        'tin': {
            'tin': int(tin),
        },
        'website': {
            'url': website,
        },
        'addresses': [
            {
                'address_line1': address1,
                'address_line2': address2,
                'city': city,
                'state': state,
                'postal_code': zip,
            },
        ],
    }
    response = requests.post('https://api-sandbox.middesk.com/v1/businesses', headers=headers, json=json_data, auth=(os.environ.get('API_KEY'), ''))
    data = response.json()
    return(response.text)

def getBusinesses():
    
    headers = {
    'Accept': 'application/json',
    }

    params = {
        'page': '1',
        'per_page': '10',
    }

    response = requests.get('https://api-sandbox.middesk.com/v1/businesses', params=params, headers=headers, auth=('mk_test_acd91c5b005a7de3a7304874', ''))
    data = response.json()
    data = data['data']
    df = pandas.DataFrame.from_dict(data, orient='columns')
    df = df.iloc[:, 3:7]
    df.rename(columns = {'name':'Business', 'created_at':'Signed Up', 'updated_at':'Last Updated', 'status': 'Status'}, inplace = True)
    return(df)