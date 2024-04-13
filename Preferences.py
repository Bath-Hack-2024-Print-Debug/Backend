from flask import Blueprint, Flask
from flask import request, jsonify
import json
from database import get_db, containsSimilarPreferences
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

def cosine_similarity(A, B):
    dot_product = np.dot(A, B)
    norm_a = np.linalg.norm(A)
    norm_b = np.linalg.norm(B)
    return dot_product / (norm_a * norm_b)

# http://127.0.0.1:5000/Preferences/getSimilarStudents?userID=anlf@gmail.com

bp = Blueprint('Preferences', __name__, url_prefix='/Preferences')


def getSimilarLocationKeys(x,y):
    count = 0

    for i in range(len(x)):
        if x[i] in y:
            count+=1
    return count


# flask run --debugger --reload


@bp.route('/getSimilarStudents', methods=["POST"])
def getSimilarStudents():
    data = request.json
    userID = data.get('userID')
    if not userID:
        return jsonify({"error": "userID is required"}), 400

    try:
        userDoc = get_db().collection("preferences").document(userID).get().to_dict()
        similarUsers = []
        preferences = get_db().collection("preferences").stream()

        for preference_set in preferences:
            current = preference_set.to_dict()

            if current["studentID"] != userID:
                # Count number of similar locations
                userVector = np.array([
                    getSimilarLocationKeys(userDoc["locationKeys"], current["locationKeys"]),
                    userDoc['maxHousemates'],
                    userDoc['maxPrice'],
                    userDoc['minHousemates'],
                    userDoc['minPrice'],
                    int(userDoc['shareHouse']),
                    int(userDoc['studentHouse'])
                ])

                currentVector = np.array([
                    getSimilarLocationKeys(userDoc["locationKeys"], current["locationKeys"]),
                    current['maxHousemates'],
                    current['maxPrice'],
                    current['minHousemates'],
                    current['minPrice'],
                    int(current['shareHouse']),
                    int(current['studentHouse'])
                ])

                similarity = cosine_similarity(userVector, currentVector)
                print(similarity)
                similarUsers.append({"user": current, "similarity":similarity})
        return jsonify({"users": sorted(similarUsers, key= lambda x: x["similarity"], reverse=True)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500






# http://127.0.0.1:5000/Preferences/setPreferences?locationKeys=
@bp.route('/setPreferences', methods=['POST'])
def setPreferences():
    data = request.json

    locationKeys = data.get("locationKeys", [])
    maxHousemates = data.get("maxHousemates",0)
    maxPrice = data.get("maxPrice",0)
    minHousemates = data.get("minHousemates",0)
    minPrice = data.get("minPrice",0)
    shareHouse = data.get("shareHouse",True)
    studentHouse = data.get("studentHouse",False)
    userID = data.get("userID","anlf@gmail.com")

    doc_ref = get_db().collection("preferences").document(userID).set({
        "locationKeys":locationKeys,
        "maxHousemates":maxHousemates,
        "maxPrice":maxPrice,
        "minHousemates":minHousemates,
        "minPrice":minPrice,
        "shareHouse":shareHouse,
        "studentHouse":studentHouse,
        "studentID":userID
    })

    return jsonify({"success":True}), 201


#
# curl -X POST "http://127.0.0.1:8080/Preferences/setPreferences" \
# -H "Content-Type: application/json" \
# -d '{
#     "studentID": "user123",
#     "locationKeys": ["LHR", "London"],
#     "maxHousemates": 5,
#     "minHousemates": 1,
#     "maxPrice": 1500,
#     "minPrice": 500,
#     "shareHouse": true,
#     "studentHouse": true
# }'


# curl -X POST "http://127.0.0.1:8080/Preferences/getSimilarStudents" \
# -H "Content-Type: application/json" \
# -d '{
#     "userID": "anlf@gmail.com"
# }'

