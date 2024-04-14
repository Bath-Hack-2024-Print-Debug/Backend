from flask import Blueprint, Flask, jsonify
from flask import request
import http.client
import json
import pydoc
import os
import sys
import pandas as pd
import infer

# current = os.path.dirname(os.path.realpath(__file__))
# parent = os.path.dirname(current)
# sys.path.append(parent.replace("Semester 2", "Semester_2"))
import Preferences
from flask import g

from auth import login

bp = Blueprint('zoopla', __name__, url_prefix='/zoopla')

# Set api keys and http connection
conn = http.client.HTTPSConnection("zoopla4.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "c58fc50e81msh979c198ee7ad8f0p1ba71bjsn06e05cb7c4ab",
    'X-RapidAPI-Host': "zoopla4.p.rapidapi.com"
}

# # Get sample list of properties in new-haw
# conn.request("GET", "/properties/rent?locationKey=new-haw&minPrice=100&page=1&maxBeds=4&sort=recent&maxPrice=10000", headers=headers)

# res = conn.getresponse()
# data = res.read()
# unpacked = json.loads(data.decode("utf-8"))

@bp.route('/getLocationKeys')
def getLocationKeys(location, num_results=1):
    '''
    Function to get the location,key dict for user inputted area name. 
    (can return x number of results if needed)
    arguments:
        location: the area name you want to search for (user enters)
        num_results: the number of results you want to return

    returns:
        a list of dictionaries containing the location and key

        example:
        [{'location': 'New Haw', 'key':new-haw}]
    '''
    
    conn.request("GET", f"/locations?location={location}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    unpacked = json.loads(data.decode("utf-8"))['data']

    # grab requested number of results if possible
    if num_results > len(unpacked):
        num_results = len(unpacked)
    out = unpacked[:num_results]
    return out

@bp.route('/getPropertyIds')
def getPropertyIds(location_key, min_price=20, max_price=25000,
                     min_beds=1, max_beds=9, sort="recent", page="1",fetch_all=False):
    '''
    Function to get the property ids for a given location key and preferences.
    arguments:
        location_key: the location key for the area you want to search
        min_price: the minimum price of the property
        max_price: the maximum price of the property
        min_beds: the minimum number of bedrooms
        max_beds: the maximum number of bedrooms
        sort: the sorting method for the results (options: "recent", 
                                                    "highest", "lowest")
        page: the page number of the results
        fetch_all: whether to fetch all the results or just the given page

    returns:
        a list of property ids that match the given criteria

        example:
        [123456, 123457, 123458, 123459]
    '''
    # get the properties on each page until there are no more

    # get the first page
    conn.request("GET", f"/properties/rent?locationKey={location_key}" + 
                 f"&minPrice={min_price}&page={page}&maxBeds={max_beds}" + 
                 f"&sort={sort}&maxPrice={max_price}&minBeds={min_beds}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    unpacked = json.loads(data.decode("utf-8"))['data']
    out = [x['id'] for x in unpacked]

    # if we want to fetch all the results
    while fetch_all and len(unpacked) > 0:
        page = int(page) + 1
        conn.request("GET", f"/properties/rent?locationKey={location_key}" + 
                     f"&minPrice={min_price}&page={page}&maxBeds={max_beds}" + 
                     f"&sort={sort}&maxPrice={max_price}&minBeds={min_beds}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        if unpacked == []:
            break
        unpacked = [x['id'] for x in json.loads(data.decode("utf-8"))['data']]
        out += unpacked

    return out

@bp.route('/getPropertyDetails')
def getPropertyDetails(property_id):
    '''
    Function to get the property details for a given property id.
    arguments:
        property_id: the id of the property you want to get the details for

    returns:
        a dictionary containing the property details

        example:
        ###see apis in discord###
    '''

    try:
        conn.request("GET", f"/properties/{property_id}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        unpacked = json.loads(data.decode("utf-8"))['data']
    except:
        unpacked = None
    return unpacked

@bp.route('/getPropertiesDetailsJSON')
@login(required=True)
def getPropertiesDetailsJSON():
    prefs = Preferences.getUserPreferences()
    locationId = getLocationKeys(prefs['city'],num_results=1)[0]['key']
 
    if locationId == 'bath' or locationId == 'bristol':
        print(locationId, prefs['minPrice'], prefs['maxPrice'], prefs['maxHousemates'])
        propertyIds = getPropertyIds(locationId,min_price=prefs['minPrice'],max_price=prefs['maxPrice'],
                                    max_beds=prefs['maxHousemates'],
                                    sort="recent",page="1",fetch_all=False)
        df = pd.read_csv(f'{locationId}_property_details.csv')
        df.set_index('id', inplace=True)
        propertyIds = [int(id) for id in propertyIds]
        print(propertyIds)
        df = df[df.index.isin(propertyIds)][['images','price','address','description']]
        df['images'] = df['images'].apply(lambda x: x.split(",")[0][2:-1].strip("'"))
        print(df.columns)
        df['predPrice'] = df.index.map(lambda x: infer.inferRent(x)[0])
        print(df[['predPrice','price']])
        #jsons = []
        # add all rows of df to jsons as jsons
        #for index, row in df.iterrows():
        #    jsons.append(row.to_json())

        jsons = df.to_json(orient='records')
        #jsons = jsonify({"data":jsons})
        print(jsons)
        return jsons


    # add api grabbing functionality
    else:
        print("nooooo")
        propertyIds = getPropertyIds(locationId,min_price=prefs['minPrice'],max_price=prefs['maxPrice'],
                                    max_beds=prefs['maxHousemates'],
                                    sort="recent",page="1",fetch_all=True)
    jsons = []
    return None

#getLocationKeys("new-haw",num_results=20)
#getPropertyIds("walton-on-thames",min_price=100,max_price=10000,min_beds=2,max_beds=4,sort="recent",page="1",fetch_all=True)
#getPropertyDetails(66703015)

# create pydocs for the functions
# pydoc.writedoc(getLocationKeys)
# pydoc.writedoc(getPropertyIds)
# pydoc.writedoc(getPropertyDetails)

print("stop")