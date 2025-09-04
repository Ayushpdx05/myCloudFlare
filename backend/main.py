from typing import Union
import configparser
from fastapi import FastAPI, Request
import subprocess
import psutil
import time
import hashlib



app = FastAPI()
config = configparser.RawConfigParser()
config.read('config.yaml')


#read config file to see which hugging face model to read
last_request_time = None

@app.get("/entropy")
async def entropy(request: Request):
    global last_request_time
    now = time.time_ns()
    
    jitter = None
    if last_request_time is not None:
        diff = now - last_request_time
        
        jitter = diff % 1_000_000_000  # remainder under 1s window
    
    last_request_time = now
    
    raw = f"{request.client.host}-{now}-{jitter}".encode()
     
    seed = hashlib.sha256(raw).hexdigest()
    
    return seed







@app.get("/dummyurl")
async def authenticate_hf(request:Request):
    
    result = await entropy(request)
    print(result)
    



    



