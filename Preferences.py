from flask import Blueprint, Flask
from flask import request, jsonify, g
import json
from database import get_db, containsSimilarPreferences, generateID
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import traceback
from auth import login

def cosine_similarity(A, B):
    dot_product = np.dot(A, B)
    norm_a = np.linalg.norm(A)
    norm_b = np.linalg.norm(B)
    return dot_product / (norm_a * norm_b)

# http://127.0.0.1:5000/Preferences/getSimilarStudents?userID=anlf@gmail.com

bp = Blueprint('Preferences', __name__, url_prefix='/Preferences')

# flask run --debugger --reload

def getUserPreferences():
    preferences = get_db().collection("preferences").stream()

    for preference_set in preferences:
        current = preference_set.to_dict()

        if current["userID"] == g.user:
            return current

        #if current["userID"] == "4wfR0mYphMZWRlAHK3S6ngOMFp53":
        #    return current



def getDetails(userID):
    db = get_db()
    user = db.collection("user").document(userID).get().to_dict()
    return user


@bp.route('/getSimilarStudents', methods=["GET"])
@login(required=True)
def getSimilarStudents():
    print("test")
    userID = g.user

    #userID = data.get("userID")
    if not userID:
        return jsonify({"error": "userID is required"}), 400

    try:
        print(userID)
        # Get user preferences
        userPreferences = getUserPreferences()
        similarUsers = []
        preferences = get_db().collection("preferences").stream()

        for preference_set in preferences:
            current = preference_set.to_dict()

            genderPreference = 0

            if userPreferences["gender"] == "Mixed" and current["gender"] == "Mixed":
                genderPreference = 1
            else:
                genderPreference = int(userPreferences["gender"] == current["gender"])

            if current["userID"] != userID:
                # Count number of similar locations

                userVector = np.array([
                    int(userPreferences["city"] == current["city"]),
                    int(userPreferences['maxHousemates']),
                    float(userPreferences['maxPrice']),
                    float(userPreferences['minPrice']),
                    int(genderPreference)
                ])

                currentVector = np.array([
                    int(userPreferences["city"] == current["city"]),
                    int(current['maxHousemates']),
                    float(current['maxPrice']),
                    float(current['minPrice']),
                    int(genderPreference)
                ])

                similarity = cosine_similarity(userVector, currentVector)
                similarUsers.append({"user": current, "similarity":similarity})

                print(f"Similarity: {similarity}")

        sortedUsers = sorted(similarUsers, key=lambda x: x["similarity"], reverse=True)

        print(f"SortedUsers: {sortedUsers}")

        users = []
        for user in sortedUsers:
            currentUser = user['user']
            currentUserID = currentUser["userID"]

            print(f"CurrentUserID: {currentUserID}")

            # Get user details
            user = getDetails(currentUserID)
            users.append(user)

        print(f"Users: {users}")

        return jsonify({"users": users})


    except Exception as e:

        traceback_string = traceback.format_exc()

        print(traceback_string)  # You can log this to a file if print is not suitable

        return jsonify({"error": str(e), "trace": traceback_string}), 500
@bp.route('/setPreferences', methods=['POST'])
@login(required=True)
def setPreferences():
    data = request.json

    city = data.get("city", "")
    maxHousemates = data.get("maxHousemates",0)
    maxPrice = data.get("maxPrice",0)
    minPrice = data.get("minPrice",0)
    gender = data.get("gender","")
    userID = g.user


    doc_ref = get_db().collection("preferences").document(str(generateID())).set({
        "city":city,
        "maxHousemates":maxHousemates,
        "maxPrice":maxPrice,
        "minPrice":minPrice,
        "userID":userID,
        "gender":gender
    })

    return jsonify({"success":True}), 201


#
# curl -X POST "http://127.0.0.1:5000/Preferences/getSimilarStudents" \
# -H "Content-Type: application/json" \
# -d '{"userID": "4wfR0mYphMZWRlAHK3S6ngOMFp53"}'


