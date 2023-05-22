from pymongo import MongoClient

class MongoDBInterface:
    def __init__(self, host, port, database_name, collection_name):
        self.client = MongoClient(host, port)
        self.database = self.client[database_name]
        self.collection = self.database[collection_name]

    def create_document(self, document):
        result = self.collection.insert_one(document)
        return result.inserted_id

    def delete_document(self, document_id):
        result = self.collection.delete_one({"_id": document_id})
        return result.deleted_count > 0

    def update_document(self, document_id, updates):
        result = self.collection.update_one({"_id": document_id}, {"$set": updates})
        return result.modified_count > 0

    def retrieve_documents(self, filter=None):
        if filter is None:
            filter = {}
        documents = self.collection.find(filter)
        return list(documents)