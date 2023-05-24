from prometheus_client import Counter, Histogram
from mongo import MongoDBInterface, MongoError
from models import User
from fastapi import APIRouter, Request, Response
from logger import Logger
import json


ROUTER = APIRouter()

REQUEST_COUNT = Counter('http_requests_total', 'Total number of HTTP requests', ['status_code'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration', ['path', 'method'])
REQUEST_SIZE = Histogram('http_request_size_bytes', 'HTTP request size', ['path'])
RESPONSE_SIZE = Histogram('http_response_size_bytes', 'HTTP response size', ['path'])


def _connect():
    mongo = MongoDBInterface("localhost", 27017, "testdatabase", "testcollection")
    mongo.ping()
    return mongo


def _retrieve_logger(request: Request) -> Logger:
    return request.state.logger


@ROUTER.get("/data")
async def get_data(request: Request):
    logger = _retrieve_logger(request)

    try:
        mongo = _connect()
        documents = mongo.retrieve_documents()
        return documents
    except MongoError as err:
        logger.error("Error retrieving documents", error=err, status_code=500, remote_addr=request.client.host, url=request.url, method=request.method)
        return Response(json.dumps({"error": "Failed retrieving documents"}), status_code=500)

@ROUTER.post("/data")
async def create_data(request: Request):
    # logger = _retrieve_logger(request)
    json = await request.json()
    # HACK : this is a hack becuase for some reason when calling call_next in the middleware with this func having 2 parameters, it indefinitely hangs with no further information. This is only a demo
    user: User = User(json)

    try:
        mongo = _connect()
        document_id = mongo.create_document(user.dict())
        return {"created": True, "document_id": str(document_id)}
    except Exception as err:
        # logger.error("Error creating document", error=err, status_code=500, remote_addr=request.client.host, url=request.url, method=request.method)
        return Response(json.dumps({"error": "Failed creating document"}), status_code=500)


@ROUTER.put("/data/{document_id}")
async def update_data(document_id: str, request: Request):
    logger = _retrieve_logger(request)

    try:
        mongo = _connect()
        request_data = await request.json()
        # TODO : what does updated equal?
        updated = mongo.update_document(document_id, request_data)
        return {"updated": True, "document_id": str(document_id)}
    except Exception as err:
        logger.error("Error updating document", error=err, status_code=500, remote_addr=request.client.host, url=request.url, method=request.method)
        return Response(json.dumps({"error": "Failed updating document"}), status_code=500)


@ROUTER.delete("/data/{id}")
def delete_data(document_id: str, request: Request):
    logger = _retrieve_logger(request)

    try:
        mongo = _connect()
        # TODO : what does deleted equal?
        deleted = mongo.delete_document(document_id)
        return {"deleted": True, "document_id": str(document_id)}
    except Exception as err:
        logger.error("Error deleting document", error=err, status_code=500, remote_addr=request.client.host, url=request.url, method=request.method)
        return Response(json.dumps({"error": "Failed deleting document"}), status_code=500)