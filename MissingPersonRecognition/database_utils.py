from pymongo import MongoClient
from gridfs import GridFS
from bson.objectid import ObjectId

# Connect to MongoDB
def connect_to_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["MissingPersonDB"]
    fs = GridFS(db)
    return db, fs

# Store a person in the database
def store_person(name, metadata, image_bytes):
    db, fs = connect_to_db()
    try:
        file_id = fs.put(image_bytes, filename=name)
        db.missing_persons.insert_one({
            "name": name,
            "metadata": metadata,
            "image_file_id": file_id
        })
        print(f"Stored {name} in the database.")
    except Exception as e:
        print(f"Error storing person: {e}")

# Fetch all missing persons from the database
def fetch_missing_persons():
    db, _ = connect_to_db()
    try:
        return list(db.missing_persons.find({}))
    except Exception as e:
        print(f"Error fetching missing persons: {e}")
        return []

# Get an image by file ID
def get_image(file_id):
    _, fs = connect_to_db()
    try:
        file = fs.get(ObjectId(file_id))
        return file.read()
    except Exception as e:
        print(f"Error retrieving file: {e}")
        return None

# Delete a person from the database
def delete_person(name):
    db, fs = connect_to_db()
    try:
        person = db.missing_persons.find_one({"name": name})
        if person:
            file_id = person["image_file_id"]
            fs.delete(ObjectId(file_id))
            db.missing_persons.delete_one({"name": name})
            print(f"Deleted {name} from the database.")
        else:
            print(f"No record found for {name}.")
    except Exception as e:
        print(f"Error deleting person: {e}")
