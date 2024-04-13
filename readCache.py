# To cache data from zoopla, find and replace all single backslashes with double backslashes in the saved json file.

import json
import pandas as pd
import zoopla as zoopla

bath_houses = zoopla.getPropertyDetails("bath-and-n-e-somerset",min_price=100,max_price=10000,min_beds=2,max_beds=4,sort="recent",page="1",fetch_all=True)
pd.DataFrame(bath_houses).to_csv("bath_houses.csv")
print("stop")