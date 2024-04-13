from flask import Blueprint, Flask
from flask import request,g
import json
from database import get_db, generateID, containsSimilarPreferences

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/getUserDetails')
def getUserDetails():
    data = request.json
    email = data.get("email")
    db = get_db()
    user = db.collection("user").document(email).get()
    json_string = json.dumps(user.to_dict())
    return json_string


@bp.route('/addUserDetails')
def addUserDetails():
    data = request.json
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    type = data.get("type")
    email = data.get("email")
    phone = data.get("phone")
    dob = data.get("dob")
    gender = data.get("gender")
    db = get_db()
    doc_ref = db.collection("user").document(email)
    doc_ref.set({"firstName" : firstName, "lastName" : lastName, "phone":phone, "type":type, "dob":dob, "gender":gender})

@bp.route('/getSimilarStudents')
def getSimilarStudents():
    data = request.json
    email = data.get("email")
    db = get_db()
    user_docs = db.collection("preferences").stream()

    preferences =  db.collection("preferences").document(email).get().to_dict()

    preferences_docs = db.collection("preferences").stream()

    similarUsers = []
    for preference_set in preferences_docs:
        potential = preference_set.to_dict()

        potentialPreferences = potential["preferences"]
        if potential["studentID"] != email and containsSimilarPreferences(potentialPreferences, preferences):
            similarUsers.append(potential)

@bp.route('/setPreferences')
def setPreferences():
    data = request.json

    locationKeys = data.get("locationKeys")
    maxHousemates = data.get("maxHousemates")
    maxPrice = data.get("maxPrice")
    minHousemates = data.get("minHousemates")
    minPrice = data.get("minPrice")
    shareHouse = data.get("shareHouse")
    studentHouse = data.get("studentHouse")
    email = data.get("email")

    id = generateID().__str__()
    db = get_db()
    doc_ref = db.collection("preferences").document(id).set({
        "locationKeys":locationKeys,
        "maxHousemates":maxHousemates,
        "maxPrice":maxPrice,
        "minHousemates":minHousemates,
        "minPrice":minPrice,
        "shareHouse":shareHouse,
        "studentHouse":studentHouse,
        "studentID":email
    })



