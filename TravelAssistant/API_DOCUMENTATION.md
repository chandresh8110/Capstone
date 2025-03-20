# Travel Assistant Translation Service API Guide

## Authentication

All API requests require authentication using a bearer token.

### Getting an Authentication Token

**Endpoint:** `POST /token`

**Request Format:**
```
Content-Type: application/x-www-form-urlencoded

username=testuser&password=testpassword
```

**Response Format:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## Translation Endpoints

### 1. Translate Text

Translates text from one language to another using Google Cloud Translation API.

**Endpoint:** `POST /translate/text`

**Headers:**
```
Authorization: Bearer {your_token}
Content-Type: application/json
```

**Request Format:**
```json
{
  "text": "Hello, how are you?",
  "source_language": "en",
  "target_language": "hi-IN"
}
```

**Response Format:**
```json
{
  "translated_text": "नमस्ते, आप कैसे हैं?",
  "source_language": "en",
  "target_language": "hi-IN"
}
```

**Supported Language Codes:**
- `en` - English
- `es-ES` - Spanish (Spain)
- `fr-FR` - French
- `de-DE` - German
- `it-IT` - Italian
- `ja-JP` - Japanese
- `ko-KR` - Korean
- `cmn-CN` - Chinese (Mandarin)
- `ru-RU` - Russian
- `hi-IN` - Hindi
- `gu-IN` - Gujarati

### 2. Text-to-Speech

Converts text to spoken audio using Google Cloud Text-to-Speech API.

**Endpoint:** `POST /translate/tts`

**Headers:**
```
Authorization: Bearer {your_token}
Content-Type: application/json
```

**Request Format:**
```json
{
  "text": "Hello, this is a test",
  "language_code": "hi-IN",
  "speaking_rate": 1.0,
  "pitch": 0.0
}
```

**Response Format:**
```json
{
  "audio_content_base64": "base64_encoded_audio_data",
  "duration_seconds": 2.5,
  "audio_url": null
}
```

**Notes:**
- `audio_content_base64` contains the audio data encoded in base64 format
- `duration_seconds` is an estimated duration of the audio in seconds
- `speaking_rate` accepts values between 0.25 and 4.0 (1.0 is normal speed)
- `pitch` accepts values between -20.0 and 20.0 (0.0 is normal pitch)

### 3. Get Available Languages

Returns a list of all supported languages.

**Endpoint:** `GET /translate/languages`

**Headers:**
```
Authorization: Bearer {your_token}
```

**Response Format:**
```json
{
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
```

### 4. Get Available Voices for a Language

Returns available voice options for a specific language.

**Endpoint:** `GET /translate/voices/{language_code}`

**Headers:**
```
Authorization: Bearer {your_token}
```

**Response Format (example for hi-IN):**
```json
{
  "hi-IN": "hi-IN-Chirp3-HD-Puck"
}
```

## Common Phrases Endpoints

### 1. Get All Common Phrases

Returns a list of common phrases with their translations.

**Endpoint:** `GET /translate/common-phrases`

**Headers:**
```
Authorization: Bearer {your_token}
```

**Query Parameters:**
- `limit` (optional): Maximum number of phrases to return (default: 50)
- `skip` (optional): Number of phrases to skip (for pagination)

**Response Format:**
```json
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "phrase": "Hello",
    "category": "Greetings",
    "translations": {
      "es-ES": {
        "translatedPhrase": "Hola",
        "pronunciation": "O-la",
        "ttsUrl": "http://example.com/tts/es/hola.mp3"
      },
      "hi-IN": {
        "translatedPhrase": "नमस्ते",
        "pronunciation": "Namaste",
        "ttsUrl": "http://example.com/tts/hi/namaste.mp3"
      }
    }
  },
  // More phrases...
]
```

### 2. Get Phrase Categories

Returns a list of all available phrase categories.

**Endpoint:** `GET /translate/common-phrases/categories`

**Headers:**
```
Authorization: Bearer {your_token}
```

**Response Format:**
```json
{
  "categories": ["Greetings", "Dining", "Transportation", "Emergency", "Shopping"]
}
```

### 3. Get Phrases by Category

Returns all phrases for a specific category.

**Endpoint:** `GET /translate/common-phrases/by-category/{category}`

**Headers:**
```
Authorization: Bearer {your_token}
```

**Response Format:**
```json
[
  {
    "_id": "507f1f77bcf86cd799439011",
    "phrase": "Hello",
    "category": "Greetings",
    "translations": {
      "es-ES": {
        "translatedPhrase": "Hola",
        "pronunciation": "O-la",
        "ttsUrl": "http://example.com/tts/es/hola.mp3"
      }
    }
  },
  // More phrases in the same category...
]
```

### 4. Get Phrase by ID

Returns a specific phrase by its ID.

**Endpoint:** `GET /translate/common-phrases/{phrase_id}`

**Headers:**
```
Authorization: Bearer {your_token}
```

**Response Format:**
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "phrase": "Hello",
  "category": "Greetings",
  "translations": {
    "es-ES": {
      "translatedPhrase": "Hola",
      "pronunciation": "O-la",
      "ttsUrl": "http://example.com/tts/es/hola.mp3"
    }
  }
}
```

## Working with Text-to-Speech Audio

The TTS endpoint returns the audio data in base64 format. To use this:

1. Extract the `audio_content_base64` from the response
2. Decode the base64 string to get the binary audio data
3. Save as an MP3 file or play it directly

### Example (JavaScript):
```javascript
// After receiving the response from the TTS endpoint
const audioBase64 = response.audio_content_base64;
const audioData = atob(audioBase64); // Decode base64
const audioBlob = new Blob([audioData], { type: 'audio/mp3' });
const audioUrl = URL.createObjectURL(audioBlob);

// Play the audio
const audioElement = new Audio(audioUrl);
audioElement.play();
```

### Example (Python):
```python
import base64

# After receiving the response from the TTS endpoint
audio_base64 = response_json["audio_content_base64"]
audio_data = base64.b64decode(audio_base64)

# Save as MP3 file
with open("output.mp3", "wb") as file:
    file.write(audio_data)
```

## Error Handling

The API uses standard HTTP status codes:

- `200 OK`: The request was successful
- `400 Bad Request`: Invalid parameters or unsupported language
- `401 Unauthorized`: Missing or invalid authentication token
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

Error responses include a detail message:

```json
{
  "detail": "Error message describing the issue"
}
```

## Notes and Limitations

1. Translation API requires an active Google Cloud account with the Translation API enabled
2. Text-to-Speech API requires an active Google Cloud account with the Text-to-Speech API enabled
3. Language codes must match the supported formats listed above
4. Large translation requests may be subject to Google API quotas and limits

## Example Curl Commands

### Authentication
```bash
curl -X POST http://localhost:8000/token \
  -d "username=testuser&password=testpassword" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

### Translate Text
```bash
curl -X POST http://localhost:8000/translate/text \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "source_language": "en", "target_language": "hi-IN"}'
```

### Text-to-Speech
```bash
curl -X POST http://localhost:8000/translate/tts \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, this is a test", "language_code": "hi-IN", "speaking_rate": 1.0, "pitch": 0.0}'
```

### Get Available Languages
```bash
curl -X GET http://localhost:8000/translate/languages \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Get Common Phrases
```bash
curl -X GET http://localhost:8000/translate/common-phrases \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```
