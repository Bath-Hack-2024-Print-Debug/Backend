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

def inferRent(property_id):
  df = pd.read_csv('./final_ml_encoded.csv')
  #df = df[[
        # "id",
        # "propertyType",
        # "name",
        # "publishedOn",
        # "address",
        # "latitude",
        # "longitude",
        # "priceActual",
        # "priceMax",
        # "priceMin",
        # "livingRooms",
        # "beds",
        # "bedsMax",
        # "bedsMin",
        # "isRetirementHome",
        # "isSharedOwnership",
        # "studentFriendly"]]
  df.set_index('id', inplace=True)

  input_row = df.loc[property_id]
  result = series_to_string_list(input_row)

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
      "Column2",
      "propertyType",
      "name",
      "publishedOn",
      "address",
      "latitude",
      "longitude",
      "livingRooms",
      "beds",
      "bedsMax",
      "bedsMin",
      "isRetirementHome",
      "isSharedOwnership",
      "studentFriendly",
      "11 Month &amp; 3 Week Tenancy",
      "2 Bedrooms",
      "3 bedrooms",
      "All Bills Included",
      "All bills included",
      "All bills included!",
      "Allocated Parking Space",
      "Allocated parking",
      "Available 30th August 2024",
      "Available April",
      "Available Now",
      "Available for the next academic year",
      "Available in August 2024",
      "Available now",
      "BS16 Location",
      "Balcony",
      "Bathroom",
      "Big back garden",
      "Bills Included",
      "Bills included",
      "Bills incuded",
      "Brand-New Finish",
      "Burglar Alarm",
      "CGI Photographs, Floorplan &amp; Video Tours",
      "Call to arrange your viewing",
      "Central Heating",
      "Central Location",
      "Central heating",
      "City Centre",
      "City centre",
      "Close to North Street, Bedminster",
      "Close to amenities",
      "Close to bus stop",
      "Close to city centre",
      "Conservatory",
      "Council Tax Band B",
      "Council Tax Band C",
      "Council Tax Band: B",
      "Council tax band B",
      "Deposit equivalent to 5 weeks rent",
      "Dishwasher",
      "Double Glazing",
      "Double bedroom",
      "Double glazing",
      "Driveway",
      "EPC B",
      "EPC C",
      "EPC D",
      "EPC Rating = C",
      "Electricity",
      "First Floor",
      "Four Bedrooms",
      "Four bedrooms",
      "Four double bedrooms",
      "Fridge Freezer",
      "Fully Furnished",
      "Fully equipped",
      "Fully furnished",
      "Furnished",
      "Furnished Home",
      "Garage",
      "Garden",
      "Gas",
      "Gas Central Heating",
      "Gas central heating",
      "Gas, Electric &amp; Water Included",
      "Good access to uwe",
      "Good public transport links",
      "Great Location",
      "Great location",
      "Holding fee equivalent to 1 weeks rent",
      "Internet",
      "Kitchen",
      "Large Garden",
      "Low maintenance back garden",
      "Managed By cj Hole",
      "Managed by cj hole",
      "Modern kitchen",
      "Multiple 1 Beds Available",
      "No Agent Fees",
      "No Smoking",
      "No pets",
      "Off Street Parking",
      "Off street parking",
      "Off street parking for one car",
      "Off street parking for two cars",
      "Offered Furnished",
      "Offered Unfurnished",
      "On Street Parking",
      "On-Street Parking",
      "Only Available to Students",
      "Open Plan Living",
      "Open plan living space",
      "Parking",
      "Part Furnished",
      "Period features",
      "Popular location",
      "Premium Student Accommodation",
      "Private Garden",
      "Private garden",
      "Rear Garden",
      "Short/Medium Term property",
      "Short/medium term",
      "Shower",
      "Six Bedrooms",
      "Six double bedrooms",
      "Sought After Location",
      "Sought after location",
      "Student Home",
      "Student Property",
      "Student property",
      "Students Can Enquire",
      "Students welcome",
      "Three Bathrooms",
      "Three Bedrooms",
      "Three bedrooms",
      "Three double bedrooms",
      "Two Bathrooms",
      "Two Bedrooms",
      "Two Double Bedrooms",
      "Two bathrooms",
      "Two bedrooms",
      "Two double bedrooms",
      "Two reception rooms",
      "Unfurnished",
      "University of bristol",
      "University of west england",
      "Water",
      "White Goods Included",
      "White goods",
      "White goods included",
      "Wi fi"
    ],
      "index": [f"{df.index[0]}"],
      "data": [result]
    }
  }

  body = str.encode(json.dumps(data))

  url = 'https://ethical-infer.uksouth.inference.ml.azure.com/score'
  # Replace this with the primary/secondary key or AMLToken for the endpoint
  api_key = 'cjyI4Y3qTAdV5N2Usyc421LR98uvvxhf'
  if not api_key:
      raise Exception("A key should be provided to invoke the endpoint")

  # The azureml-model-deployment header will force the request to go to a specific deployment.
  # Remove this header to have the request observe the endpoint traffic rules
  headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'infer-rent' }

  req = urllib.request.Request(url, body, headers)

  try:
      response = urllib.request.urlopen(req)

      result = response.read().decode('utf-8')
      return result
  except urllib.error.HTTPError as error:
      print("The request failed with status code: " + str(error.code))

      # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
      print(error.info())
      print(error.read().decode("utf8", 'ignore'))
  
