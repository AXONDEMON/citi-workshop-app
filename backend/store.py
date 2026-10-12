import os
import uuid


class MemoryStore:
    def __init__(self):
        self.notes = {}

    def list(self):
        return list(self.notes.values())

    def create(self, title, content):
        note = {"id": str(uuid.uuid4()), "title": title, "content": content}
        self.notes[note["id"]] = note
        return note

    def delete(self, note_id):
        return self.notes.pop(note_id, None) is not None
    
    def update(self, note_id, title, content):
        note = self.notes.get(note_id)
        if note is None:
            return None
        note["title"] = title
        note["content"] = content
        return note


class MongoStore:
    def __init__(self, uri):
        from pymongo import MongoClient
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        db_name = os.environ.get("DB_NAME", "notesdb")
        self.col = client[db_name]["notes"]

    def list(self):
        return list(self.col.find({}, {"_id": 0}))   # hide Mongo's internal _id

    def create(self, title, content):
        note = {"id": str(uuid.uuid4()), "title": title, "content": content}
        self.col.insert_one(dict(note))              # copy: insert_one adds _id to the dict
        return note

    def delete(self, note_id):
        return self.col.delete_one({"id": note_id}).deleted_count == 1
    def update(self, note_id, title, content):
        from pymongo import ReturnDocument
        return self.col.find_one_and_update(
            {"id": note_id},
            {"$set": {"title": title, "content": content}},
            projection={"_id": 0},
            return_document=ReturnDocument.AFTER,   # return the updated doc
        )        


# Created once per Lambda container and reused across requests
_uri = os.environ.get("MONGO_URI")
store = MongoStore(_uri) if _uri else MemoryStore()