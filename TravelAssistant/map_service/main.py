from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional, Any, Annotated
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

# Load environment variables
load_dotenv()

app = FastAPI(title="Map Service")

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database("map_db")
places_collection = db.get_collection("places")

# Get port from environment
PORT = int(os.getenv("SERVICE_PORT", "8002"))

# Helper function for ObjectId conversion
def convert_object_id(id: Any) -> str:
    if isinstance(id, ObjectId):
        return str(id)
    if isinstance(id, str):
        return id
    raise ValueError("Invalid ObjectId")

# Models
class Place(BaseModel):
    id: Optional[Annotated[str, Field(alias="_id")]] = None
    name: str
    description: str
    latitude: float
    longitude: float
    rating: Optional[float] = None
    photo_url: Optional[str] = None
    tags: List[str] = []
    location: str
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "name": "Eiffel Tower",
                "description": "Iconic iron lattice tower in Paris",
                "latitude": 48.8584,
                "longitude": 2.2945,
                "rating": 4.7,
                "photo_url": "https://example.com/eiffel_tower.jpg",
                "tags": ["landmark", "tower", "tourism"],
                "location": "paris"
            }
        }
    )

class Direction(BaseModel):
    distance: str
    duration: str
    steps: List[str]
    polyline: str

# Mock directions function (in production, use an actual mapping API)
def get_mock_directions(origin: str, destination: str) -> Direction:
    # In a real implementation, you would call a mapping API like Google Maps
    return Direction(
        distance="10 km",
        duration="20 minutes",
        steps=[
            f"Start from {origin}",
            "Head north on Main Street",
            "Turn right onto First Avenue",
            "Continue for 5 km",
            "Turn left onto Park Road",
            "Destination will be on your right",
            f"Arrive at {destination}"
        ],
        polyline="encoded_polyline_string_here"
    )

@app.get("/")
async def root():
    return {
        "service": "Map Service",
        "version": "1.0.0",
        "endpoints": [
            "/places",
            "/directions",
            "/locations"
        ]
    }

@app.get("/locations")
async def get_available_locations():
    """Get all available locations in the database"""
    locations = await places_collection.distinct("location")
    return {"locations": locations}

@app.get("/places", response_model=List[Place])
async def get_places(location: str = Query(..., description="City or location name")):
    """Get all places for a specific location"""
    location_lower = location.lower()
    
    # Find places matching the location
    places = []
    cursor = places_collection.find({"location": location_lower})
    
    async for document in cursor:
        places.append(Place.model_validate(document))
    
    if not places:
        raise HTTPException(status_code=404, detail=f"No places found for: {location}")
    
    return places

@app.get("/directions", response_model=Direction)
async def get_directions_endpoint(
    origin: str = Query(..., description="Origin location"),
    destination: str = Query(..., description="Destination location")
):
    # Here, in a real implementation, you would call a mapping API
    return get_mock_directions(origin, destination)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT) 