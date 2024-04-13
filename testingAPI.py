import http.client
import json

conn = http.client.HTTPSConnection("zoopla.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "18ce59c615mshb3a5125e65228e1p1f1e23jsn8973327a4591",
    'X-RapidAPI-Host': "zoopla.p.rapidapi.com"
}

conn.request("GET", "/properties/v2/list?locationValue=Oxford%2C%20Oxfordshire&locationIdentifier=oxford&furnishedState=Any&sortOrder=newest_listings&page=1", headers=headers)

res = conn.getresponse()
data = res.read()
decoded = data.decode("utf-8")
unpacked = json.loads(decoded)

print("stop")