from ninja import NinjaAPI
from .auth import CustomAuth
from .schema import InputSchema, GetSignedUrl
import uuid, boto3, os
from dotenv import load_dotenv
from datetime import datetime 
import json

load_dotenv()
s3 = boto3.client('s3', 
    region_name= os.getenv("COGNITO_REGION"),
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),)


api = NinjaAPI(title="Synthera API docs")

@api.post("/protected-check", auth=CustomAuth())
def protected_check(request, payload: InputSchema):
    return {"input" : payload.text}

@api.post("/get-uploaded-url", auth=CustomAuth())
def get_uploaded_url(request, payload: GetSignedUrl):
    user = request.auth
    user_id = user['sub']
    file_id = str(uuid.uuid4())
    key = f"videos/{user_id}/{file_id}-{payload.file_name}"
    presigned_url = s3.generate_presigned_url(
        ClientMethod = 'put_object', 
        Params = {
            'Bucket': bucket_name, 
            "Key" : key, 
            "ContentType": payload.content_type
        }, 
        ExpiresIn = 600
    )
    data = {
        "user_id": user_id,
        "file_key": key,
        "file_name": payload.file_name,
        "content_type": payload.content_type, 
        "correlation_id": str(uuid.uuid4()), 
        "timestamp": datetime.utcnow().isoformat()
    }
    return {"upload_url": presigned_url, "file_key": key}





