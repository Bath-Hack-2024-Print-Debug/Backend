import firebase_admin
from firebase_admin import firestore, credentials
from flask import Flask
from flask import request
import uuid
import json

app = Flask(__name__)

@app.route('/getHouses')
def getHouses():
    creds = firebase_admin.credentials.Certificate("firebase.json")
    firebase_admin.initialize_app(creds)
    db = firestore.client()
    houses_ref = db.collection("houses")
    docs = houses_ref.stream()
    houses = []
    for doc in docs:
        dictionary = doc.to_dict()
        houses.append(dictionary)
    json_string = json.dumps(houses)
    return json_string

def generateID():
    id = uuid.uuid1()
    return id

@app.route('/getUserDetails')
def getUserDetails():
    data = request.json
    email = data.get("email")
    creds = firebase_admin.credentials.Certificate("firebase.json")
    firebase_admin.initialize_app(creds)
    db = firestore.client()
    user = db.collection("user").document(email).get()
    json_string = json.dumps(user.to_dict())
    return json_string

@app.route('/addHouseDetails')
def addHouseDetails():
    creds = firebase_admin.credentials.Certificate("firebase.json")
    firebase_admin.initialize_app(creds)
    db = firestore.client()
    data = request.json
    addressLine1 = data.get("addressLine1")
    addressLine2 = data.get("addressLine2")
    available = data.get("available")
    bathrooms = data.get("bathrooms")
    billsIncluded = data.get("billsIncluded")
    endDate = data.get("endDate")
    lat = data.get("lat")
    long = data.get("long")
    owner = data.get("owner")
    postcode = data.get("postcode")
    price = data.get("price")
    priceEstimateML = data.get("priceEstimateML")
    singles = data.get("singles")
    startDate = data.get("startDate")
    townCity = data.get("townCity")
    imageURL = data.get("imageURL")
    description = data.get("description")

    doc_ref = db.collection("houses").document(generateID(id))
    doc_ref.set({'addressLine1': addressLine1,
    'addressLine2' : addressLine2,
    'available':available,
    'bathrooms':bathrooms,
    'billsIncluded':billsIncluded,
    'endDate':endDate,
    'lat':lat,
    'long':long,
    'owner':owner,
    'postcode':postcode,
    'price':price,
    'priceEstimateML':priceEstimateML,
    'singles':singles,
    'startDate':startDate,
    'townCity':townCity,
    'description':description,
    'imageURL':imageURL})

@app.route('/addUserDetails')
def addUserDetails():
    creds = firebase_admin.credentials.Certificate("firebase.json")

    firebase_admin.initialize_app(creds)
    db = firestore.client()

    data = request.json
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    type = data.get("type")
    email = data.get("email")
    phone = data.get("phone")
    dob = data.get("dob")
    gender = data.get("gender")

    doc_ref = db.collection("user").document(email)
    doc_ref.set({"firstName" : firstName, "lastName" : lastName, "phone":phone, "type":type, "dob":dob, "gender":gender})