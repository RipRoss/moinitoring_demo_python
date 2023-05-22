from fastapi import FastAPI
from prometheus_client import start_http_server
from endpoints import ROUTER
from logger import logging

APP = FastAPI()

@APP.on_event("startup")
async def startup_event():
    # Code to execute before the application starts
    logging.debug("Starting Prometheus HTTP server")
    start_http_server(port=8081)
    logging.debug("Prometheus HTTP server successfully started")
    

APP.include_router(ROUTER)
