from pymongo import MongoClient
from bson import ObjectId


class MongoError(Exception):
    pass


class MongoDBInterface:
    def __init__(self, host, port, database_name, collection_name):
        self.client = MongoClient(host, port)
        self.database = self.client[database_name]
        self.collection = self.database[collection_name]

    def ping(self):
        try:
            self.client.admin.command('ping')
        except Exception as err:
            raise MongoError(err) from None

    def create_document(self, document):
        try:
            result = self.collection.insert_one(document)
        except Exception as err:
            raise MongoError(err) from None
        
        return result.inserted_id

    def delete_document(self, document_id):
        try:
            result = self.collection.delete_one({"_id": ObjectId(document_id)})
        except Exception as err:
            raise MongoError(err) from None
        return result.deleted_count > 0

    def update_document(self, document_id, updates):
        try:
            result = self.collection.update_one({"_id": ObjectId(document_id)}, {"$set": updates})
        except Exception as err:
            raise MongoError(err) from None
        return result.modified_count > 0

    def retrieve_documents(self, filter=None):
        if filter is None:
            raise MongoError("Filter cannot be None")
            filter = {}
        try:
            documents = list(self.collection.find(filter))
            for document in documents:
                document['_id'] = str(document['_id'])
        except Exception as err:
            raise MongoError(err) from None
            
        return list(documents)