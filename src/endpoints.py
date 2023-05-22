from prometheus_client import Counter, Histogram
from mongo import MongoDBInterface
from models import User
from fastapi import APIRouter

ROUTER = APIRouter()

request_count = Counter('http_requests_total', 'Total number of HTTP requests', ['status_code'])
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration', ['path', 'method'])
request_size = Histogram('http_request_size_bytes', 'HTTP request size', ['path'])
response_size = Histogram('http_response_size_bytes', 'HTTP response size', ['path'])


def _connect():
    return MongoDBInterface("localhost", 27017, "testdatabase", "testcollection")


@ROUTER.get("/data")
def get_data():
    mongo = _connect()
    documents = mongo.retrieve_documents()
    return documents

@ROUTER.post("/data")
def create_data(user: User):
    mongo = _connect()
    document_id = mongo.create_document(user)
    return {"created": True, "document_id": document_id}

@ROUTER.put("/data/{id}")
def update_data(document_id: int):
    mongo = _connect()
    updated = mongo.update_document(document_id, update_data)
    return {"updated": updated}

@ROUTER.delete("/data/{id}")
def delete_data(document_id: int):
    mongo = _connect()
    deleted = mongo.delete_document(document_id)