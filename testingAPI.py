import http.client
import json
import pydoc

# Set api keys and http connection
conn = http.client.HTTPSConnection("zoopla4.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "18ce59c615mshb3a5125e65228e1p1f1e23jsn8973327a4591",
    'X-RapidAPI-Host': "zoopla4.p.rapidapi.com"
}

# # Get sample list of properties in new-haw
# conn.request("GET", "/properties/rent?locationKey=new-haw&minPrice=100&page=1&maxBeds=4&sort=recent&maxPrice=10000", headers=headers)

# res = conn.getresponse()
# data = res.read()
# unpacked = json.loads(data.decode("utf-8"))

def get_location_keys(location, num_results=1):
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

def get_property_ids(location_key, min_price=0, max_price=1000000,
                     min_beds=1, max_beds=4, sort="recent", page="1",fetch_all=False):
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

def get_property_details(property_id):
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

#get_location_keys("new-haw",num_results=20)
#get_property_ids("walton-on-thames",min_price=100,max_price=10000,min_beds=2,max_beds=4,sort="recent",page="1",fetch_all=True)
#get_property_details(66703015)

# create pydocs for the functions
# pydoc.writedoc(get_location_keys)
# pydoc.writedoc(get_property_ids)
# pydoc.writedoc(get_property_details)

print("stop")