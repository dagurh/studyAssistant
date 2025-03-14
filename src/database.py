from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://dagur:Dagur99einar@cluster0.gcjxu.mongodb.net/?retryWrites=true&w=majority&appName=cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))
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