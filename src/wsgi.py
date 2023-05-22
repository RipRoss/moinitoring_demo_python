from fastapi import FastAPI
from endpoints import router

APP = FastAPI()

APP.include_router(router)
