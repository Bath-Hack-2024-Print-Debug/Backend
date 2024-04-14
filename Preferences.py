from flask import Blueprint, Flask
from flask import request, jsonify, g
import json
from database import get_db, containsSimilarPreferences, generateID
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import traceback


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

        # if current["userID"] == g.user:
        #     return current

        if current["userID"] == "anlf@gmail.com":
            return current



def getDetails(userID):
    db = get_db()
    user = db.collection("user").document(userID).get().to_dict()
    return user


@bp.route('/getSimilarStudents', methods=["POST"])
def getSimilarStudents():
    data = request.json
    # userID = g.user
    userID = data.get("userID")
    if not userID:
        return jsonify({"error": "userID is required"}), 400

    try:

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
                    userPreferences['maxHousemates'],
                    userPreferences['maxPrice'],
                    userPreferences['minPrice'],
                    genderPreference
                ])

                currentVector = np.array([
                    int(userPreferences["city"] == current["city"]),
                    current['maxHousemates'],
                    current['maxPrice'],
                    current['minPrice'],
                    genderPreference
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
def setPreferences():
    data = request.json

    city = data.get("city", "")
    maxHousemates = data.get("maxHousemates",0)
    maxPrice = data.get("maxPrice",0)
    minPrice = data.get("minPrice",0)
    gender = data.get("gender","")
    userID = g.user


    doc_ref = get_db().collection("preferences").document(generateID).set({
        "city":city,
        "maxHousemates":maxHousemates,
        "maxPrice":maxPrice,
        "minPrice":minPrice,
        "userID":userID,
        "gender":gender
    })

    return jsonify({"success":True}), 201


#
# curl -X POST "http://127.0.0.1:8080/Preferences/getSimilarStudents" \
# -H "Content-Type: application/json" \
# -d '{"userID": "anlf@gmail.com"}'

