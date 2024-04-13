from flask import Blueprint, Flask
from flask import request,g
import json
from database import get_db, generateID, containsSimilarPreferences
from auth import check_account

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/getUserDetails',)
@check_account(required=True)
def getUserDetails():
    db = get_db()
    user = db.collection("user").document(g.user).get()
    json_string = json.dumps(user.to_dict())
    return json_string

@check_account(required=True)
@bp.route('/addUserDetails')
def addUserDetails():
    data = request.json
    name = data.get("name")
    phone = data.get("phone")
    dob = data.get("dob")
    gender = data.get("gender")
    desc = data.get("desc")
    db = get_db()
    doc_ref = db.collection("user").document(g.user)
    doc_ref.set({"name": name, "phone": phone, "dob": dob, "gender": gender, "desc": desc})

@check_account(required=True)
@bp.route('/getSimilarStudents')
def getSimilarStudents():
    data = request.json
    email = data.get(g.user)
    db = get_db()
    user_docs = db.collection("preferences").stream()

    preferences =  db.collection("preferences").document(g.user).get().to_dict()

    preferences_docs = db.collection("preferences").stream()

    similarUsers = []
    for preference_set in preferences_docs:
        potential = preference_set.to_dict()

        potentialPreferences = potential["preferences"]
        if potential["studentID"] != g.user and containsSimilarPreferences(potentialPreferences, preferences):
            similarUsers.append(potential)

@check_account(required=True)
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

    db = get_db()
    doc_ref = db.collection("preferences").document(g.user).set({
        "locationKeys":locationKeys,
        "maxHousemates":maxHousemates,
        "maxPrice":maxPrice,
        "minHousemates":minHousemates,
        "minPrice":minPrice,
        "shareHouse":shareHouse,
        "studentHouse":studentHouse,
        "studentID":email
    })



