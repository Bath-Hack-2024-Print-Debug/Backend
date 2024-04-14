from flask import Blueprint, Flask
from flask import request,g
import json
from database import get_db, generateID, containsSimilarPreferences
from auth import login

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/getUserDetails')
@login(required=True)
def getUserDetails():
    db = get_db()
    user = db.collection("user").document(g.user).get()
    json_string = json.dumps(user.to_dict())
    return json_string


@bp.route('/addUserDetails' , methods=["POST"])
@login(required=True)
def addUserDetails():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    dob = data.get("dob")
    gender = data.get("gender")
    db = get_db()
    doc_ref = db.collection("user").document(g.user)
    doc_ref.set({"name" : name, "dob":dob, "gender":gender, "description":description})
    return json.dumps({"status": "success"})

@bp.route('/getSimilarStudents')
@login(required=True)
def getSimilarStudents():
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




