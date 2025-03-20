import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Sample places data
sample_places = {
    "paris": [
        {
            "name": "Eiffel Tower",
            "description": "Iconic iron lattice tower on the Champ de Mars in Paris, France.",
            "latitude": 48.8584,
            "longitude": 2.2945,
            "rating": 4.7,
            "photo_url": "https://example.com/eiffel_tower.jpg",
            "tags": ["landmark", "tower", "tourism"]
        },
        {
            "name": "Louvre Museum",
            "description": "World's largest art museum and a historic monument in Paris, France.",
            "latitude": 48.8606,
            "longitude": 2.3376,
            "rating": 4.8,
            "photo_url": "https://example.com/louvre.jpg",
            "tags": ["museum", "art", "history"]
        },
        {
            "name": "Notre-Dame Cathedral",
            "description": "Medieval Catholic cathedral on the Île de la Cité in the 4th arrondissement of Paris.",
            "latitude": 48.8530,
            "longitude": 2.3499,
            "rating": 4.7,
            "photo_url": "https://example.com/notre_dame.jpg",
            "tags": ["cathedral", "architecture", "history"]
        }
    ],
    "rome": [
        {
            "name": "Colosseum",
            "description": "An oval amphitheatre in the centre of the city of Rome, Italy.",
            "latitude": 41.8902,
            "longitude": 12.4922,
            "rating": 4.8,
            "photo_url": "https://example.com/colosseum.jpg",
            "tags": ["amphitheatre", "history", "archaeology"]
        },
        {
            "name": "Roman Forum",
            "description": "A rectangular forum surrounded by the ruins of several important ancient government buildings at the center of the city of Rome.",
            "latitude": 41.8925,
            "longitude": 12.4853,
            "rating": 4.7,
            "photo_url": "https://example.com/roman_forum.jpg",
            "tags": ["ruins", "history", "archaeology"]
        },
        {
            "name": "Vatican City",
            "description": "City-state surrounded by Rome, Italy, and headquarters of the Roman Catholic Church.",
            "latitude": 41.9029,
            "longitude": 12.4534,
            "rating": 4.9,
            "photo_url": "https://example.com/vatican.jpg",
            "tags": ["city-state", "religion", "architecture"]
        }
    ],
    "new york": [
        {
            "name": "Statue of Liberty",
            "description": "Colossal neoclassical sculpture on Liberty Island in New York Harbor.",
            "latitude": 40.6892,
            "longitude": -74.0445,
            "rating": 4.7,
            "photo_url": "https://example.com/statue_of_liberty.jpg",
            "tags": ["statue", "landmark", "tourism"]
        },
        {
            "name": "Central Park",
            "description": "Urban park in Manhattan, New York City.",
            "latitude": 40.7812,
            "longitude": -73.9665,
            "rating": 4.8,
            "photo_url": "https://example.com/central_park.jpg",
            "tags": ["park", "recreation", "nature"]
        },
        {
            "name": "Empire State Building",
            "description": "Art Deco skyscraper in Midtown Manhattan, New York City.",
            "latitude": 40.7484,
            "longitude": -73.9857,
            "rating": 4.7,
            "photo_url": "https://example.com/empire_state.jpg",
            "tags": ["skyscraper", "landmark", "observation deck"]
        }
    ],
    "tokyo": [
        {
            "name": "Tokyo Skytree",
            "description": "Broadcasting and observation tower in Sumida, Tokyo, Japan.",
            "latitude": 35.7101,
            "longitude": 139.8107,
            "rating": 4.6,
            "photo_url": "https://example.com/skytree.jpg",
            "tags": ["tower", "observation deck", "landmark"]
        },
        {
            "name": "Meiji Shrine",
            "description": "Shinto shrine dedicated to Emperor Meiji and Empress Shōken.",
            "latitude": 35.6763,
            "longitude": 139.6993,
            "rating": 4.7,
            "photo_url": "https://example.com/meiji_shrine.jpg",
            "tags": ["shrine", "religion", "garden"]
        },
        {
            "name": "Senso-ji Temple",
            "description": "Ancient Buddhist temple located in Asakusa, Tokyo, Japan.",
            "latitude": 35.7147,
            "longitude": 139.7966,
            "rating": 4.7,
            "photo_url": "https://example.com/sensoji.jpg",
            "tags": ["temple", "religion", "history"]
        }
    ]
}

async def seed_database():
    """Seed the MongoDB database with initial places data"""
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    
    # Connect to MongoDB
    print("Connecting to MongoDB...")
    client = AsyncIOMotorClient(MONGO_URI)
    db = client.get_database("map_db")
    places_collection = db.get_collection("places")
    
    # Check if collection already has data
    count = await places_collection.count_documents({})
    if count > 0:
        print("Database already contains data. Skipping seed.")
        return
    
    # Insert sample data
    print("Inserting sample places data...")
    
    # Process and insert each location's places
    for location, places in sample_places.items():
        for place in places:
            place["location"] = location  # Add location field to each place
            await places_collection.insert_one(place)
    
    print("Sample places data inserted successfully!")
    
    # Create index on location for faster queries
    await places_collection.create_index("location")
    print("Index created on 'location' field")

async def main():
    print("Seeding the database with initial places data...")
    await seed_database()
    print("Database seeding completed!")

if __name__ == "__main__":
    asyncio.run(main()) 