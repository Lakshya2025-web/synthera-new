from fastapi import FastAPI, HTTPException, Depends 
from pydantic import BaseModel
from agents.graph import app
import traceback
from auth import CustomAuth, get_current_user
from fastapi.middleware.cors import CORSMiddleware
from tasks.notification_tasks import send_email
from redis import Redis 
import hashlib
import os
import json
from dotenv import load_dotenv
load_dotenv()

redis_client = Redis(
    host=os.getenv("REDIS_URL"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True
)

class Query(BaseModel):
    user_input: str


fast_app = FastAPI()
@fast_app.post("/agent-run")
async def run_agent(payload: Query, user=Depends(get_current_user)):
    try:
        content_hash = hashlib.sha256(payload.user_input.encode("utf-8")).hexdigest()
        cached = redis_client.get(content_hash)
        if cached:
            print("CACHE HIT: ", content_hash)
            cached_json = json.loads(cached)
            return {"status": "success", "data" : cached_json}
        print("CACHE MISS: ", content_hash)
        result = app.invoke({"user_input": payload.user_input, "user_email" : user["email"] , "user_id" : user["sub"] })
        send_email.delay(
            to_email=user["email"],
            subject="Your Synthera Intelligence Report",
            body=f"Your report is ready (Note: This link expires in 1 hour).\nDownload here:\n{result['pdf_url']}"
        )
        redis_client.set(content_hash, json.dumps(result), ex=60 * 60 * 24)
        return {"status": "success", "data": result}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Agent execution failed: {str(e)}"
        )

fast_app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

