from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from crud import create_user
from db import Base, engine
import models

import json
app = FastAPI()


Base.metadata.create_all(bind=engine)

app.add_middleware(
     CORSMiddleware,
     allow_origins = ["*"],
     allow_credentials = True,
     allow_methods = ["*"],
     allow_headers =["*"]
)
@app.get("/help")
async def help():
    return {"status": "ok", "message": "Backend is alive!"}

@app.post("/api/register")
async def register(request: Request):
    data = await request.json()
    print("📩 Data received from frontend:")
    print(json.dumps(data, ensure_ascii=False, indent=2))  
    result = create_user(data)   # קריאה לפונקציית CRUD ששומרת את המשתמש ב-DB
    return result
   