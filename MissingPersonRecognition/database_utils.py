from pymongo import MongoClient
from gridfs import GridFS
from bson.objectid import ObjectId

# Connect to MongoDB
def connect_to_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["MissingPersonDB"]
    fs = GridFS(db)
    return db, fs

# Store image and metadata
def store_person(image_path, name, metadata):
    _, fs = connect_to_db()
    with open(image_path, "rb") as f:
        file_id = fs.put(f, filename=name, metadata=metadata)
    return file_id

# List metadata for missing persons
def list_missing_persons():
    _, fs = connect_to_db()
    return [{"id": str(file._id), "name": file.filename, "metadata": file.metadata} for file in fs.find()]

# Fetch all missing persons
def fetch_missing_persons():
    _, fs = connect_to_db()
    missing_persons = []
    for file in fs.find():
        image_data = file.read()
        metadata = file.metadata
        missing_persons.append({
            "name": file.filename,
            "image": image_data,
            "metadata": metadata
        })
    return missing_persons
