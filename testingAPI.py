import http.client
import json

# Set api keys and http connection
conn = http.client.HTTPSConnection("zoopla4.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "18ce59c615mshb3a5125e65228e1p1f1e23jsn8973327a4591",
    'X-RapidAPI-Host': "zoopla4.p.rapidapi.com"
}

# Get sample list of properties in new-haw
conn.request("GET", "/properties/rent?locationKey=new-haw&minPrice=100&page=1&maxBeds=4&sort=recent&maxPrice=10000", headers=headers)

res = conn.getresponse()
data = res.read()
unpacked = json.loads(data.decode("utf-8"))

'''
function to get the location,key dict for user inputted area name 
(can return x number of results if needed)
arguments:
    location: the area name you want to search for (user enters)
    num_results: the number of results you want to return
'''
def get_location_keys(location, num_results=1):
    conn.request("GET", f"/locations?location={location}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    unpacked = json.loads(data.decode("utf-8"))['data']

    # grab requested number of results if possible
    if num_results > len(unpacked):
        num_results = len(unpacked)
    out = unpacked[:num_results]
    return out

'''
function to get the property ids for a given location key and preferences
arguments:
    location_key: the location key for the area you want to search
    min_price: the minimum price of the property
    max_price: the maximum price of the property
    min_beds: the minimum number of bedrooms
    max_beds: the maximum number of bedrooms
    sort: the sorting method for the results (options: "recent", 
                                                "highest", "lowest")
    page: the page number of the results
'''
def get_property_ids(location_key, min_price=0, max_price=10000,
                     min_beds=1, max_beds=4, sort="recent", page="1",fetch_all=False):
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

#get_location_keys("new-haw",num_results=20)
get_property_ids("walton-on-thames",min_price=100,max_price=10000,min_beds=2,max_beds=4,sort="recent",page="1",fetch_all=True)
print("stop")