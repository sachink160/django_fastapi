from fastapi import FastAPI, Depends, Header, HTTPException
import os
import httpx
from dotenv import load_dotenv
import jwt

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"  # or "RS256" depending on your Django config
API_KEY_SECRET = os.getenv("API_KEY_SECRET")

app = FastAPI()

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(
    authorization: str = Header(..., alias="Authorization"),
    api_key: str = Header(..., alias="api-key")
):
    if api_key != API_KEY_SECRET:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    
    token = authorization.split(" ")[1]
    user_data = decode_jwt_token(token)
    return user_data

@app.get("/secure-data")
async def secure_data(user=Depends(get_current_user)):
    return {"message": "Access granted", "user": user}


# API_KEY_SECRET = os.getenv("API_KEY_SECRET")
# DJANGO_AUTH_URL = os.getenv("DJANGO_AUTH_URL")  # e.g., http://localhost:8000/api/user/

# app = FastAPI()

# # Dependency to validate token + API key
# async def get_auth_headers(
#     authorization: str = Header(..., alias="Authorization"),
#     api_key: str = Header(..., alias="api-key")
# ):
#     if api_key != API_KEY_SECRET:
#         raise HTTPException(status_code=403, detail="Invalid API Key")

#     # Call Django API to verify JWT token
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.get(
#                 DJANGO_AUTH_URL,
#                 headers={"Authorization": authorization}
#             )
#             if response.status_code != 200:
#                 raise HTTPException(status_code=401, detail="Invalid JWT Token")
#         except httpx.RequestError as e:
#             raise HTTPException(status_code=500, detail=f"Django auth service unavailable: {e}")

#     return {
#         "Authorization": authorization,
#         "api-key": api_key
#     }

# @app.post("/secure-data")
# async def secure_data(headers: dict = Depends(get_auth_headers)):
#     return {"message": "Authorized access", "headers": headers}



