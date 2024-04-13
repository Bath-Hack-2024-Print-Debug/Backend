# To cache data from zoopla, find and replace all single backslashes with double backslashes in the saved json file.

import json
import pandas as pd
import zoopla as zoopla

to_search = ['bath-and-n-e-somerset','bath', 'bath-city-centre','bathwick',
             'somerset/bathpool','bathampton','bathford',
             'bathford','batheaston']
bath_houses = set()
for location in to_search:
    temp = set(zoopla.getPropertyIds(location,min_price=0,max_price=25000,
                              min_beds=1,sort="recent",page="1",
                              fetch_all=True))
    bath_houses = bath_houses.union(temp)


# add unique ids not already in the csv file
df = pd.DataFrame(columns=['id'], data=list(bath_houses))
# overwrite the csv file
df.to_csv('bath_ids.csv', index=False)
print("stop")