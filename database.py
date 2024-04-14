import firebase_admin
from firebase_admin import firestore, credentials
from flask import Flask
from flask import request,g
import uuid


def get_db():
    if 'db' not in g:
        g.db = firestore.client()
    return g.db

def generateID():
    id = uuid.uuid1()
    return id

def containsSimilarPreferences(potentialPreferences, preferences):
    containsAny = False
    for p in potentialPreferences:
        if p in preferences:
            return True
    return False


