import os
import sys
import boto3
import logging
import subprocess
from fastapi import FastAPI
# from api.api_v1.api import router1,router2
from api.api_v1.api import router as api_router
# from api.api_v1.api import router2
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger()

app = FastAPI()

    


app.include_router(api_router, prefix="/api/v1")
@app.get("/")
async def root():
    return {"message": "API for question answering bot"}