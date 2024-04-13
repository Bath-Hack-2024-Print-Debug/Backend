# To cache data from zoopla, find and replace all single backslashes with double backslashes in the saved json file.

import json
import pandas as pd

# Description: This file is used to read the cache file and return the data in a dictionary format.
f = open("C:\\Users\\USER\\Documents\\Uni\\CompSci\\Semester 2\\Hackathon\\Backend\\SampleData\\Lists\\oxfordListTest.json")
unpacked = json.load(f)
print("stop")