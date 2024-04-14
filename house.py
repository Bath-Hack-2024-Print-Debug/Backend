from flask import Blueprint, Flask
from flask import request
import json
from database import get_db, containsSimilarPreferences
from auth import login
bp = Blueprint('house', __name__, url_prefix='/house')


@bp.route('/getHouses')
@login(required=True)
def getHouses():
    db = get_db()
    houses_ref = db.collection("houses")
    docs = houses_ref.stream()
    houses = []
    for doc in docs:
        dictionary = doc.to_dict()
        houses.append(dictionary)
    json_string = json.dumps(houses)
    return json_string

@bp.route('/addHouseDetails')
@login(required=True)
def addHouseDetails():
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
    db = get_db()
    doc_ref = db.collection("houses").document(generateID().__str__())
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

@bp.route('/getFilteredHouses',methods=['GET', 'PUSH'])
@login(required=True)
def getFilteredHouses():
    data = request.json
    minPrice = data.get('minPrice')
    maxPrice = data.get('maxPrice')
    



