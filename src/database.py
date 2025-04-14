from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import ReturnDocument
from dotenv import load_dotenv
from bson import ObjectId
from bson.errors import InvalidId
import os

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
coll = os.getenv("COLL")
users_coll = os.getenv("USERS_COLL")

client = MongoClient(mongo_uri, server_api=ServerApi('1'))
db = client["vef2-e1"]
collection = db[coll]
users_collection = db[users_coll]

def sanitize_input(data: dict) -> dict:
    safe_data = {}
    for key, value in data.items():
        if key.startswith("$"):
            continue

        if isinstance(value, dict):
            safe_data[key] = sanitize_input(value)
        else:
            safe_data[key] = value
    return safe_data

async def insertIntoDB(doc):
    try:
        safe_doc = sanitize_input(doc)
        collection.insert_one(safe_doc)
        print("Successful db insert")
    except Exception as e:
        print(e)

async def queryDB(doc):
    query = {}
    try:
        safe_doc = sanitize_input(doc)
        query = list(collection.find(safe_doc))
    except Exception as e:
        print(e)
    
    for item in query:
        item["_id"] = str(item["_id"])

    return query

async def updateDB(id_str: str, update_dict: dict):
    try:
        safe_update_dict = sanitize_input(update_dict)
        object_id = ObjectId(id_str)
    except InvalidId:
        return {"status": "error", "message": "Invalid ObjectId format"}, 400
    
    result = collection.find_one_and_update(
        {"_id": object_id},
        {"$set": safe_update_dict},
        upsert=False,
        return_document=ReturnDocument.AFTER
    )

    if result:
        result["_id"] = str(result["_id"])
        return {"status": "success", "message": "Document updated", "updated_document": result}, 200
    else:
        return {"status": "not_found", "message": "Document not found"}, 404



async def deleteFromDB(id_str: str, userEmail: str):
    try:
        object_id = ObjectId(id_str)
    except InvalidId:
        return {"status": "error", "message": "Invalid ObjectId format"}, 400

    result = collection.delete_one({"_id": object_id, "user": userEmail})

    if result.deleted_count == 1:
        return {"status": "success", "message": "Document deleted"}, 200
    else:
        return {"status": "not_found", "message": "Document not found"}, 404
    
async def getUserByEmail(email: str):
    try:
        safe_email = sanitize_input({"email": email})
        user = users_collection.find_one(safe_email)
    except Exception as e:
        print(e)
        return None
    return user

async def saveUser(user_dict: dict):
    try:
        safe_user_dict = sanitize_input(user_dict)
        users_collection.insert_one(safe_user_dict)
        print("User saved successfully")
    except Exception as e:
        print(e)
        return None
