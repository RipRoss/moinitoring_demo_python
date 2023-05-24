from fastapi import FastAPI
from prometheus_client import start_http_server
from endpoints import ROUTER
from logger import Logger
from middleware import middleware


APP = FastAPI()
APP.middleware("http")(middleware)

@APP.on_event("startup")
def startup_event():
    # Code to execute before the application starts
    logger = Logger()
    logger.debug("Starting Prometheus HTTP server")
    start_http_server(port=8081)
    logger.debug("Prometheus HTTP server successfully started")


APP.include_router(ROUTER)
