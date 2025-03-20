from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
import httpx
import os
from typing import Optional

# Configuration
SECRET_KEY = "CHANGE_THIS_TO_A_SECURE_SECRET_KEY"  # In production, use a secure key and store it safely
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Service URLs from environment variables
TRANSLATION_SERVICE_URL = os.getenv("TRANSLATION_SERVICE_URL", "http://localhost:8001")
MAP_SERVICE_URL = os.getenv("MAP_SERVICE_URL", "http://localhost:8002")
PACKING_SERVICE_URL = os.getenv("PACKING_SERVICE_URL", "http://localhost:8003")

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Sample user database (in production, use a proper database)
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "full_name": "Test User",
        "email": "testuser@example.com",
        "hashed_password": pwd_context.hash("testpassword"),
        "disabled": False,
    }
}

# Auth functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Initialize FastAPI
app = FastAPI(title="Travel Assistant API Gateway")

# Authentication endpoints
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# Translation Service Routes
@app.post("/translate/text")
async def translate_text(data: dict, current_user: User = Depends(get_current_active_user)):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{TRANSLATION_SERVICE_URL}/translate/text", json=data)
        return response.json()

@app.post("/translate/tts")
async def text_to_speech(data: dict, current_user: User = Depends(get_current_active_user)):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{TRANSLATION_SERVICE_URL}/translate/tts", json=data)
        return response.json()

@app.get("/translate/languages")
async def get_languages(current_user: User = Depends(get_current_active_user)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TRANSLATION_SERVICE_URL}/languages")
        return response.json()

@app.get("/translate/voices/{language_code}")
async def get_voices(language_code: str, current_user: User = Depends(get_current_active_user)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TRANSLATION_SERVICE_URL}/voices/{language_code}")
        return response.json()

@app.get("/translate/common-phrases")
async def get_common_phrases(limit: int = 50, skip: int = 0, current_user: User = Depends(get_current_active_user)):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{TRANSLATION_SERVICE_URL}/common-phrases", 
            params={"limit": limit, "skip": skip}
        )
        return response.json()

@app.get("/translate/common-phrases/categories")
async def get_phrase_categories(current_user: User = Depends(get_current_active_user)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TRANSLATION_SERVICE_URL}/common-phrases/categories")
        return response.json()

@app.get("/translate/common-phrases/by-category/{category}")
async def get_phrases_by_category(
    category: str, 
    current_user: User = Depends(get_current_active_user)
):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{TRANSLATION_SERVICE_URL}/common-phrases/by-category/{category}"
        )
        return response.json()

@app.get("/translate/common-phrases/{phrase_id}")
async def get_phrase_by_id(
    phrase_id: str, 
    current_user: User = Depends(get_current_active_user)
):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{TRANSLATION_SERVICE_URL}/common-phrases/{phrase_id}"
        )
        return response.json()

# Map Service Routes
@app.get("/map/places")
async def get_famous_places(location: str, current_user: User = Depends(get_current_active_user)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{MAP_SERVICE_URL}/places", params={"location": location})
        return response.json()

@app.get("/map/directions")
async def get_directions(origin: str, destination: str, current_user: User = Depends(get_current_active_user)):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{MAP_SERVICE_URL}/directions", 
            params={"origin": origin, "destination": destination}
        )
        return response.json()

# Packing List Service Routes
@app.post("/packing/generate")
async def generate_packing_list(data: dict, current_user: User = Depends(get_current_active_user)):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{PACKING_SERVICE_URL}/generate", json=data)
        return response.json()

@app.get("/")
async def root():
    return {
        "service": "Travel Assistant API Gateway",
        "version": "1.0.0",
        "endpoints": {
            "authentication": ["/token"],
            "translation": [
                "/translate/text",
                "/translate/tts",
                "/translate/languages",
                "/translate/voices/{language_code}",
                "/translate/common-phrases",
                "/translate/common-phrases/categories",
                "/translate/common-phrases/by-category/{category}",
                "/translate/common-phrases/{phrase_id}"
            ],
            "map": [
                "/map/places",
                "/map/directions"
            ],
            "packing": [
                "/packing/generate"
            ]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 