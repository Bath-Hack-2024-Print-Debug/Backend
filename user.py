from flask import Blueprint, Flask
from flask import request,g
import json
from auth import login
from database import get_db, generateID, containsSimilarPreferences

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/getUserDetails')
@login(required=True)
def getUserDetails():
    data = request.json
    email = data.get("email")
    db = get_db()
    user = db.collection("user").document(email).get()
    json_string = json.dumps(user.to_dict())
    return json_string


@bp.route('/addUserDetails', methods=["POST"])
@login(required=True)
def addUserDetails():
    data = request.json
    name = data.get("name")
    gender = data.get("gender")
    description = data.get("description")
    DoB = data.get("dob")
    db = get_db()
    doc_ref = db.collection("user").document(g.user)
    doc_ref.set({"name" : name, "description" : description, "dob":DoB, "gender":gender})
    return json.dumps({"status":"success"})

@bp.route('/getSimilarStudents')
@login(required=True)
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
@login(required=True)
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



