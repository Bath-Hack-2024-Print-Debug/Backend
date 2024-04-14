import urllib.request
import json
import os
import ssl
import pandas as pd

# Preprocess the Bath data
def series_to_string_list(row_series):
    # Convert the Series to a list of values
    values = row_series.tolist()
    
    # Convert each value to a string representation
    string_list = [str(value) for value in values]
    
    # Wrap each value in quotes
    quoted_list = [f"{value}" for value in string_list]
    
    return quoted_list

df = pd.read_csv('bath_ml.csv')
df = df[[
      "id",
      "propertyType",
      "name",
      "publishedOn",
      "address",
      "latitude",
      "longitude",
      "priceActual",
      "priceMax",
      "priceMin",
      "livingRooms",
      "beds",
      "bedsMax",
      "bedsMin",
      "isRetirementHome",
      "isSharedOwnership",
      "studentFriendly"]]
df.set_index('id', inplace=True)

input_row = df.iloc[0]
result = series_to_string_list(input_row)
print(result)

print("pause")


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
data =  {
  "input_data": {
    "columns": [
      "propertyType",
      "name",
      "publishedOn",
      "address",
      "latitude",
      "longitude",
      "priceActual",
      "priceMax",
      "priceMin",
      "livingRooms",
      "beds",
      "bedsMax",
      "bedsMin",
      "isRetirementHome",
      "isSharedOwnership",
      "studentFriendly"
    ],
    "index": [f"{df.index[0]}"],
    "data": [result]
  }
}

body = str.encode(json.dumps(data))

url = 'https://full-hack-bath-infer.uksouth.inference.ml.azure.com/score'
# Replace this with the primary/secondary key or AMLToken for the endpoint
api_key = '4bfCay1HlUXmbSF0s6oHylrxOcQZaD21'
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")

# The azureml-model-deployment header will force the request to go to a specific deployment.
# Remove this header to have the request observe the endpoint traffic rules
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'infer-point' }

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))