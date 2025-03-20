from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, ConfigDict, BeforeValidator
from typing import List, Dict, Optional, Any, Annotated, cast
import os
import base64
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import json
from google.cloud import texttospeech
from google.cloud import storage
from google.cloud import translate_v2 as translate

# Load environment variables
load_dotenv()

app = FastAPI(title="Translation Service")

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database("translation_db")
phrases_collection = db.get_collection("common_phrases")

# Google Cloud configuration
BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "travelassistant_tts")
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "focal-dolphin-447218-v5")
SERVICE_ACCOUNT_KEY_PATH = os.getenv("SERVICE_ACCOUNT_KEY_PATH", "D:\\projects\\gcp_key.json")
AUDIO_FOLDER = "tts_audio"

# Helper function for ObjectId conversion
def convert_object_id(id: Any) -> str:
    if isinstance(id, ObjectId):
        return str(id)
    if isinstance(id, str):
        return id
    raise ValueError("Invalid ObjectId")

# Use Annotated with BeforeValidator for ObjectId
PyObjectId = Annotated[str, BeforeValidator(convert_object_id)]

# Models
class TranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str

class TranslationResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str

class TTSRequest(BaseModel):
    text: str
    language_code: str
    voice_name: Optional[str] = None
    speaking_rate: Optional[float] = 1.0
    pitch: Optional[float] = 0.0

class TTSResponse(BaseModel):
    audio_content_base64: str
    duration_seconds: float
    audio_url: Optional[str] = None

class TranslationDetails(BaseModel):
    translatedPhrase: str
    ttsUrl: str
    pronunciation: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class CommonPhrase(BaseModel):
    id: PyObjectId = Field(alias="_id", default=None)
    phrase: str
    category: str
    translations: Dict[str, TranslationDetails]
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "phrase": "Hello",
                "category": "Greetings",
                "translations": {
                    "es": {
                        "translatedPhrase": "Hola",
                        "pronunciation": "O-la",
                        "ttsUrl": "http://example.com/tts/es/hola.mp3"
                    }
                }
            }
        }
    )

# Get port from environment
PORT = int(os.getenv("SERVICE_PORT", "8001"))

# Comprehensive language mapping
SUPPORTED_LANGUAGES = {
    "en": "English",
    "es-ES": "Spanish (Spain)",
    "fr-FR": "French",
    "de-DE": "German",
    "it-IT": "Italian",
    "ja-JP": "Japanese",
    "ko-KR": "Korean",
    "cmn-CN": "Chinese (Mandarin)",
    "ru-RU": "Russian",
    "hi-IN": "Hindi",
    "gu-IN": "Gujarati"
}

# Language to Voice Mapping from TTS.py
LANGUAGE_VOICES = {
    'hi-IN': 'hi-IN-Chirp3-HD-Puck',
    'gu-IN': 'gu-IN-Chirp3-HD-Leda',
    'ja-JP': 'ja-JP-Chirp3-HD-Aoede',
    'es-ES': 'es-ES-Chirp3-HD-Charon',
    'fr-FR': 'fr-FR-Chirp3-HD-Aoede',
    'ko-KR': 'ko-KR-Chirp3-HD-Leda',
    'cmn-CN': 'cmn-CN-Chirp3-HD-Charon',
    'ru-RU': 'ru-RU-Chirp3-HD-Orus',
    'de-DE': 'de-DE-Chirp3-HD-Charon'
}

# Initialize Google Cloud clients
try:
    print(f"Initializing Google Cloud clients with key path: {SERVICE_ACCOUNT_KEY_PATH}")
    tts_client = texttospeech.TextToSpeechClient.from_service_account_json(SERVICE_ACCOUNT_KEY_PATH)
    translate_client = translate.Client.from_service_account_json(SERVICE_ACCOUNT_KEY_PATH)
    print("Successfully initialized Google Cloud clients")
except Exception as e:
    print(f"Error initializing Google Cloud clients: {str(e)}")
    print(f"Error type: {type(e).__name__}")
    raise RuntimeError(f"Failed to initialize Google Cloud clients: {str(e)}")

# Translation function using Google Cloud Translate API
def translate_text(text: str, source_language: str, target_language: str) -> str:
    try:
        # Convert language codes if needed (API uses 'en', not 'en-US', etc.)
        source = source_language.split('-')[0] if '-' in source_language else source_language
        target = target_language.split('-')[0] if '-' in target_language else target_language
        
        result = translate_client.translate(
            text, 
            target_language=target,
            source_language=source
        )
        
        return result["translatedText"]
    except Exception as e:
        print(f"Error in translation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

# Real TTS function using Google Cloud TTS
def text_to_speech(text: str, language_code: str, voice_name: Optional[str], 
                   speaking_rate: float, pitch: float) -> tuple:
    try:
        # Use the proper voice mapping if available
        selected_voice = voice_name
        if not selected_voice and language_code in LANGUAGE_VOICES:
            selected_voice = LANGUAGE_VOICES[language_code]
        
        input_text = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=selected_voice
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=speaking_rate,
            pitch=pitch
        )
        
        response = tts_client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )
        
        # Return the audio content and estimated duration directly without storing in GCS
        audio_content_base64 = base64.b64encode(response.audio_content).decode('utf-8')
        # Estimate duration (Google doesn't provide this directly)
        estimated_duration = len(response.audio_content) / 16000  # Rough estimate
        
        return audio_content_base64, estimated_duration, None
        
    except Exception as e:
        print(f"Error in TTS processing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"TTS processing failed: {str(e)}")

@app.get("/")
async def root():
    return {
        "service": "Translation Service",
        "version": "1.0.0",
        "endpoints": [
            "/translate/text",
            "/translate/tts",
            "/translate/languages",
            "/translate/voices/{language_code}",
            "/translate/common-phrases",
            "/translate/common-phrases/categories",
            "/translate/common-phrases/by-category/{category}"
        ]
    }

@app.get("/languages")
async def get_supported_languages():
    return SUPPORTED_LANGUAGES

@app.get("/voices/{language_code}")
async def get_voices_for_language(language_code: str):
    if language_code in LANGUAGE_VOICES:
        return {language_code: LANGUAGE_VOICES[language_code]}
    raise HTTPException(status_code=404, detail=f"No voices available for language code: {language_code}")

@app.post("/translate/text", response_model=TranslationResponse)
async def translate_text_endpoint(request: TranslationRequest):
    # Validate language codes
    if request.source_language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Source language not supported: {request.source_language}")
    if request.target_language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Target language not supported: {request.target_language}")
    
    # Call the translation function
    translated_text = translate_text(
        request.text,
        request.source_language,
        request.target_language
    )
    
    return TranslationResponse(
        translated_text=translated_text,
        source_language=request.source_language,
        target_language=request.target_language
    )

@app.post("/translate/tts", response_model=TTSResponse)
async def text_to_speech_endpoint(request: TTSRequest):
    # Validate language code
    if request.language_code not in SUPPORTED_LANGUAGES and request.language_code not in LANGUAGE_VOICES:
        raise HTTPException(status_code=400, detail=f"Language not supported: {request.language_code}")
    
    # Validate voice if provided
    voice_name = request.voice_name
    if not voice_name and request.language_code in LANGUAGE_VOICES:
        voice_name = LANGUAGE_VOICES[request.language_code]
    
    # Call the TTS function
    audio_content_base64, duration_seconds, audio_url = text_to_speech(
        request.text,
        request.language_code,
        voice_name,
        request.speaking_rate,
        request.pitch
    )
    
    return TTSResponse(
        audio_content_base64=audio_content_base64,
        duration_seconds=duration_seconds,
        audio_url=audio_url
    )

# New endpoints for common phrases

@app.get("/common-phrases", response_model=List[CommonPhrase])
async def get_common_phrases(limit: int = 50, skip: int = 0):
    """
    Retrieve a list of common phrases with their translations.
    """
    phrases = []
    cursor = phrases_collection.find().skip(skip).limit(limit)
    
    async for document in cursor:
        phrases.append(CommonPhrase.model_validate(document))
    
    return phrases

@app.get("/common-phrases/categories")
async def get_phrase_categories():
    """
    Get all available categories of common phrases.
    """
    categories = await phrases_collection.distinct("category")
    return {"categories": categories}

@app.get("/common-phrases/by-category/{category}", response_model=List[CommonPhrase])
async def get_phrases_by_category(category: str):
    """
    Get all phrases for a specific category.
    """
    phrases = []
    cursor = phrases_collection.find({"category": category})
    
    async for document in cursor:
        phrases.append(CommonPhrase.model_validate(document))
    
    if not phrases:
        raise HTTPException(status_code=404, detail=f"No phrases found for category: {category}")
    
    return phrases

@app.get("/common-phrases/{phrase_id}", response_model=CommonPhrase)
async def get_phrase_by_id(phrase_id: str):
    """
    Get a specific phrase by its ID.
    """
    try:
        document = await phrases_collection.find_one({"_id": ObjectId(phrase_id)})
        if document:
            return CommonPhrase.model_validate(document)
        raise HTTPException(status_code=404, detail=f"Phrase with ID {phrase_id} not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid phrase ID format: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT) 