from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import ReturnDocument
from dotenv import load_dotenv
from bson import ObjectId
from bson.errors import InvalidId
import os

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri, server_api=ServerApi('1'))
db = client["vef2-e1"]
collection = db["studyAssistant"]

async def insertIntoDB(doc):
    try:
        collection.insert_one(doc)
        print("Successful db insert")
    except Exception as e:
        print(e)

async def queryDB(doc):
    query = {}
    try:
        query = list(collection.find(doc))
    except Exception as e:
        print(e)
    
    for item in query:
        item["_id"] = str(item["_id"])

    return query

async def updateDB(id_str: str, update_dict: dict):
    try:
        object_id = ObjectId(id_str)
    except InvalidId:
        return {"status": "error", "message": "Invalid ObjectId format"}, 400
    
    result = collection.find_one_and_update(
        {"_id": object_id},
        {"$set": update_dict},
        upsert=False,
        return_document=ReturnDocument.AFTER
    )

    if result:
        result["_id"] = str(result["_id"])
        return {"status": "success", "message": "Document updated", "updated_document": result}, 200
    else:
        return {"status": "not_found", "message": "Document not found"}, 404



async def deleteFromDB(id_str: str):
    try:
        object_id = ObjectId(id_str)
    except InvalidId:
        return {"status": "error", "message": "Invalid ObjectId format"}, 400

    result = collection.delete_one({"_id": object_id})

    if result.deleted_count == 1:
        return {"status": "success", "message": "Document deleted"}, 200
    else:
        return {"status": "not_found", "message": "Document not found"}, 404