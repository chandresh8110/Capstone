from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import os

app = FastAPI(title="Packing List Service")

# Get port from environment
PORT = int(os.getenv("SERVICE_PORT", "8003"))

# Models
class PackingListRequest(BaseModel):
    destination: str
    duration: int  # in days
    season: str
    trip_type: str = "leisure"
    activities: List[str] = []
    gender: Optional[str] = None
    age_group: Optional[str] = None

class PackingItem(BaseModel):
    name: str
    category: str
    quantity: int
    essential: bool = False
    notes: Optional[str] = None

class PackingListResponse(BaseModel):
    items: List[PackingItem]
    destination: str
    duration: int
    season: str
    trip_type: str

# Base packing items for all trips
BASE_ITEMS = [
    PackingItem(name="Passport", category="documents", quantity=1, essential=True),
    PackingItem(name="Wallet", category="documents", quantity=1, essential=True),
    PackingItem(name="Phone Charger", category="electronics", quantity=1, essential=True),
    PackingItem(name="Toothbrush", category="toiletries", quantity=1, essential=True),
    PackingItem(name="Toothpaste", category="toiletries", quantity=1, essential=True),
    PackingItem(name="Deodorant", category="toiletries", quantity=1, essential=True),
    PackingItem(name="Hand Sanitizer", category="toiletries", quantity=1, essential=True),
    PackingItem(name="Face Mask", category="health", quantity=5),
    PackingItem(name="Travel Insurance Info", category="documents", quantity=1, essential=True),
    PackingItem(name="Emergency Contact Info", category="documents", quantity=1, essential=True),
    PackingItem(name="Pain Reliever", category="medication", quantity=1),
    PackingItem(name="Band-Aids", category="health", quantity=1),
]

# Items by climate/season
SEASON_ITEMS = {
    "summer": [
        PackingItem(name="T-shirts", category="clothing", quantity=5),
        PackingItem(name="Shorts", category="clothing", quantity=3),
        PackingItem(name="Sandals", category="footwear", quantity=1),
        PackingItem(name="Sunglasses", category="accessories", quantity=1),
        PackingItem(name="Sunscreen", category="toiletries", quantity=1, essential=True),
        PackingItem(name="Hat", category="accessories", quantity=1),
        PackingItem(name="Insect Repellent", category="toiletries", quantity=1),
        PackingItem(name="Light Pajamas", category="clothing", quantity=1),
        PackingItem(name="Swimwear", category="clothing", quantity=1),
    ],
    "winter": [
        PackingItem(name="Sweaters", category="clothing", quantity=3),
        PackingItem(name="Thermal Underwear", category="clothing", quantity=2),
        PackingItem(name="Winter Coat", category="clothing", quantity=1, essential=True),
        PackingItem(name="Gloves", category="accessories", quantity=1),
        PackingItem(name="Scarf", category="accessories", quantity=1),
        PackingItem(name="Winter Hat", category="accessories", quantity=1),
        PackingItem(name="Boots", category="footwear", quantity=1, essential=True),
        PackingItem(name="Thick Socks", category="clothing", quantity=3),
        PackingItem(name="Lip Balm", category="toiletries", quantity=1),
        PackingItem(name="Hand Warmers", category="accessories", quantity=2),
        PackingItem(name="Warm Pajamas", category="clothing", quantity=1),
    ],
    "spring": [
        PackingItem(name="Light Sweaters", category="clothing", quantity=2),
        PackingItem(name="Long Sleeve Shirts", category="clothing", quantity=3),
        PackingItem(name="Light Jacket", category="clothing", quantity=1),
        PackingItem(name="Umbrella", category="accessories", quantity=1),
        PackingItem(name="Allergy Medicine", category="medication", quantity=1),
        PackingItem(name="Rain Jacket", category="clothing", quantity=1),
        PackingItem(name="Waterproof Shoes", category="footwear", quantity=1),
    ],
    "fall": [
        PackingItem(name="Light Sweaters", category="clothing", quantity=2),
        PackingItem(name="Long Sleeve Shirts", category="clothing", quantity=3),
        PackingItem(name="Medium Jacket", category="clothing", quantity=1),
        PackingItem(name="Scarf", category="accessories", quantity=1),
        PackingItem(name="Closed Shoes", category="footwear", quantity=1),
        PackingItem(name="Light Gloves", category="accessories", quantity=1),
        PackingItem(name="Warm Hat", category="accessories", quantity=1),
    ],
    "rainy": [
        PackingItem(name="Rain Jacket", category="clothing", quantity=1, essential=True),
        PackingItem(name="Waterproof Shoes", category="footwear", quantity=1, essential=True),
        PackingItem(name="Umbrella", category="accessories", quantity=1, essential=True),
        PackingItem(name="Quick-dry Clothing", category="clothing", quantity=3),
        PackingItem(name="Waterproof Phone Case", category="accessories", quantity=1),
        PackingItem(name="Waterproof Backpack Cover", category="accessories", quantity=1),
    ],
    "tropical": [
        PackingItem(name="Lightweight Clothing", category="clothing", quantity=5),
        PackingItem(name="Insect Repellent", category="toiletries", quantity=1, essential=True),
        PackingItem(name="Anti-malarial Medication", category="medication", quantity=1, essential=True, notes="If required for destination"),
        PackingItem(name="High SPF Sunscreen", category="toiletries", quantity=1, essential=True),
        PackingItem(name="Aloe Vera Gel", category="toiletries", quantity=1),
        PackingItem(name="Mosquito Net", category="accessories", quantity=1, notes="If accommodations don't provide"),
    ],
}

# Items by trip type
TRIP_TYPE_ITEMS = {
    "business": [
        PackingItem(name="Business Suits", category="clothing", quantity=2, essential=True),
        PackingItem(name="Dress Shirts", category="clothing", quantity=3, essential=True),
        PackingItem(name="Dress Shoes", category="footwear", quantity=1, essential=True),
        PackingItem(name="Ties", category="accessories", quantity=2),
        PackingItem(name="Laptop", category="electronics", quantity=1, essential=True),
        PackingItem(name="Business Cards", category="documents", quantity=1),
        PackingItem(name="Portfolio/Notebook", category="accessories", quantity=1),
        PackingItem(name="Portable Charger", category="electronics", quantity=1),
        PackingItem(name="Presentation Materials", category="documents", quantity=1, notes="If needed"),
    ],
    "leisure": [
        PackingItem(name="Casual Clothes", category="clothing", quantity=4),
        PackingItem(name="Comfortable Shoes", category="footwear", quantity=1, essential=True),
        PackingItem(name="Book/E-Reader", category="entertainment", quantity=1),
        PackingItem(name="Camera", category="electronics", quantity=1),
        PackingItem(name="Day Bag/Backpack", category="accessories", quantity=1),
        PackingItem(name="Snacks", category="food", quantity=1),
        PackingItem(name="Reusable Water Bottle", category="accessories", quantity=1),
    ],
    "beach": [
        PackingItem(name="Swimsuits", category="clothing", quantity=2, essential=True),
        PackingItem(name="Beach Towel", category="accessories", quantity=1),
        PackingItem(name="Flip Flops", category="footwear", quantity=1),
        PackingItem(name="Sunscreen", category="toiletries", quantity=1, essential=True, notes="High SPF"),
        PackingItem(name="After-Sun Lotion", category="toiletries", quantity=1),
        PackingItem(name="Beach Bag", category="accessories", quantity=1),
        PackingItem(name="Beach Cover-up", category="clothing", quantity=1),
        PackingItem(name="Snorkeling Gear", category="accessories", quantity=1, notes="Or rent at destination"),
        PackingItem(name="Waterproof Phone Case", category="accessories", quantity=1),
    ],
    "adventure": [
        PackingItem(name="Hiking Boots", category="footwear", quantity=1, essential=True),
        PackingItem(name="Backpack", category="accessories", quantity=1, essential=True),
        PackingItem(name="Water Bottle", category="accessories", quantity=1, essential=True),
        PackingItem(name="First Aid Kit", category="health", quantity=1, essential=True),
        PackingItem(name="Insect Repellent", category="toiletries", quantity=1),
        PackingItem(name="Multi-tool", category="tools", quantity=1),
        PackingItem(name="Headlamp/Flashlight", category="tools", quantity=1),
        PackingItem(name="Quick-dry Towel", category="accessories", quantity=1),
        PackingItem(name="Compass", category="tools", quantity=1),
        PackingItem(name="Energy Bars", category="food", quantity=5),
        PackingItem(name="Water Purification Tablets", category="health", quantity=1),
    ],
    "camping": [
        PackingItem(name="Tent", category="equipment", quantity=1, essential=True),
        PackingItem(name="Sleeping Bag", category="equipment", quantity=1, essential=True),
        PackingItem(name="Sleeping Pad", category="equipment", quantity=1),
        PackingItem(name="Camping Stove", category="equipment", quantity=1),
        PackingItem(name="Cookware", category="equipment", quantity=1),
        PackingItem(name="Headlamp", category="tools", quantity=1, essential=True),
        PackingItem(name="Multi-tool", category="tools", quantity=1),
        PackingItem(name="Insect Repellent", category="toiletries", quantity=1, essential=True),
        PackingItem(name="Fire Starter", category="tools", quantity=1),
        PackingItem(name="Toilet Paper", category="toiletries", quantity=1),
        PackingItem(name="Trash Bags", category="equipment", quantity=3),
    ],
    "cruise": [
        PackingItem(name="Formal Attire", category="clothing", quantity=1, notes="For formal nights"),
        PackingItem(name="Motion Sickness Medication", category="medication", quantity=1),
        PackingItem(name="Light Jacket", category="clothing", quantity=1, notes="For windy deck"),
        PackingItem(name="Day Bag", category="accessories", quantity=1),
        PackingItem(name="Swimwear", category="clothing", quantity=2),
        PackingItem(name="Sunscreen", category="toiletries", quantity=1, essential=True),
        PackingItem(name="Cash for Ports", category="documents", quantity=1, notes="Small bills"),
    ],
}

# Special items by destination
DESTINATION_ITEMS = {
    "paris": [
        PackingItem(name="Universal Power Adapter", category="electronics", quantity=1, essential=True),
        PackingItem(name="French Phrase Book", category="documents", quantity=1),
        PackingItem(name="Comfortable Walking Shoes", category="footwear", quantity=1, essential=True),
        PackingItem(name="RFID-Blocking Wallet", category="accessories", quantity=1, notes="For pickpocket protection"),
        PackingItem(name="Museum Pass", category="documents", quantity=1, notes="Consider purchasing in advance"),
    ],
    "tokyo": [
        PackingItem(name="Universal Power Adapter", category="electronics", quantity=1, essential=True),
        PackingItem(name="Japanese Phrase Book", category="documents", quantity=1),
        PackingItem(name="Portable Wifi", category="electronics", quantity=1),
        PackingItem(name="Hand Sanitizer", category="toiletries", quantity=1),
        PackingItem(name="Slip-on Shoes", category="footwear", quantity=1, notes="Easy to remove at temples/homes"),
        PackingItem(name="Comfortable Walking Shoes", category="footwear", quantity=1, essential=True),
        PackingItem(name="Cash", category="documents", quantity=1, notes="Japan is still cash-heavy"),
    ],
    "new york": [
        PackingItem(name="Subway Map", category="documents", quantity=1),
        PackingItem(name="Comfortable Walking Shoes", category="footwear", quantity=1, essential=True),
        PackingItem(name="City Pass", category="documents", quantity=1, notes="Consider for attractions"),
        PackingItem(name="Umbrella", category="accessories", quantity=1),
        PackingItem(name="Light Layers", category="clothing", quantity=3, notes="Weather can change quickly"),
    ],
    "rome": [
        PackingItem(name="Universal Power Adapter", category="electronics", quantity=1, essential=True),
        PackingItem(name="Italian Phrase Book", category="documents", quantity=1),
        PackingItem(name="Modest Clothing for Vatican", category="clothing", quantity=1, notes="Covers shoulders and knees"),
        PackingItem(name="Comfortable Walking Shoes", category="footwear", quantity=1, essential=True),
        PackingItem(name="Water Bottle", category="accessories", quantity=1, notes="Can refill at public fountains"),
        PackingItem(name="Sun Hat", category="accessories", quantity=1),
    ],
    "bali": [
        PackingItem(name="Universal Power Adapter", category="electronics", quantity=1, essential=True),
        PackingItem(name="Sarong", category="clothing", quantity=1, notes="Required for temple visits"),
        PackingItem(name="Insect Repellent", category="toiletries", quantity=1, essential=True),
        PackingItem(name="Light, Modest Clothing", category="clothing", quantity=3, notes="For temples"),
        PackingItem(name="Sunscreen", category="toiletries", quantity=1, essential=True),
        PackingItem(name="Indonesian Phrase Book", category="documents", quantity=1),
    ],
    "london": [
        PackingItem(name="Universal Power Adapter", category="electronics", quantity=1, essential=True),
        PackingItem(name="Umbrella", category="accessories", quantity=1, essential=True),
        PackingItem(name="Oyster Card", category="documents", quantity=1, notes="For public transport"),
        PackingItem(name="Rain Jacket", category="clothing", quantity=1),
        PackingItem(name="Layered Clothing", category="clothing", quantity=3, notes="Weather changes frequently"),
    ],
    "sydney": [
        PackingItem(name="Universal Power Adapter", category="electronics", quantity=1, essential=True),
        PackingItem(name="High SPF Sunscreen", category="toiletries", quantity=1, essential=True, notes="Australian sun is strong"),
        PackingItem(name="Insect Repellent", category="toiletries", quantity=1),
        PackingItem(name="Sunglasses", category="accessories", quantity=1, essential=True),
        PackingItem(name="Swimwear", category="clothing", quantity=1),
        PackingItem(name="Rain Jacket", category="clothing", quantity=1),
    ],
    "dubai": [
        PackingItem(name="Universal Power Adapter", category="electronics", quantity=1, essential=True),
        PackingItem(name="Modest Clothing", category="clothing", quantity=3, essential=True, notes="Covers shoulders and knees"),
        PackingItem(name="Sunscreen", category="toiletries", quantity=1, essential=True),
        PackingItem(name="Sunglasses", category="accessories", quantity=1, essential=True),
        PackingItem(name="Scarf for Women", category="accessories", quantity=1, notes="For mosque visits"),
        PackingItem(name="Water Bottle", category="accessories", quantity=1, essential=True),
    ],
    "bangkok": [
        PackingItem(name="Universal Power Adapter", category="electronics", quantity=1, essential=True),
        PackingItem(name="Modest Clothing", category="clothing", quantity=2, notes="For temple visits"),
        PackingItem(name="Insect Repellent", category="toiletries", quantity=1, essential=True),
        PackingItem(name="Thai Phrase Book", category="documents", quantity=1),
        PackingItem(name="Hand Sanitizer", category="toiletries", quantity=1),
        PackingItem(name="Toilet Paper", category="toiletries", quantity=1, notes="Not always available"),
    ],
}

# Items by activity
ACTIVITY_ITEMS = {
    "swimming": [
        PackingItem(name="Swimsuit", category="clothing", quantity=2, essential=True),
        PackingItem(name="Goggles", category="accessories", quantity=1),
        PackingItem(name="Swim Cap", category="accessories", quantity=1),
        PackingItem(name="Waterproof Sunscreen", category="toiletries", quantity=1, essential=True),
        PackingItem(name="Beach Towel", category="accessories", quantity=1),
        PackingItem(name="Flip Flops", category="footwear", quantity=1),
        PackingItem(name="Ear Plugs", category="accessories", quantity=1),
    ],
    "hiking": [
        PackingItem(name="Hiking Boots", category="footwear", quantity=1, essential=True),
        PackingItem(name="Walking Stick", category="accessories", quantity=1),
        PackingItem(name="Trail Map", category="documents", quantity=1),
        PackingItem(name="GPS Device", category="electronics", quantity=1),
        PackingItem(name="Moisture-wicking Shirts", category="clothing", quantity=2),
        PackingItem(name="Hiking Pants", category="clothing", quantity=1, essential=True),
        PackingItem(name="Hiking Socks", category="clothing", quantity=2, essential=True),
        PackingItem(name="Bandana", category="accessories", quantity=1),
        PackingItem(name="Energy Bars", category="food", quantity=3),
        PackingItem(name="First Aid Kit", category="health", quantity=1, essential=True),
    ],
    "skiing": [
        PackingItem(name="Ski Jacket", category="clothing", quantity=1, essential=True),
        PackingItem(name="Ski Pants", category="clothing", quantity=1, essential=True),
        PackingItem(name="Thermal Underwear", category="clothing", quantity=2, essential=True),
        PackingItem(name="Ski Gloves", category="accessories", quantity=1, essential=True),
        PackingItem(name="Ski Goggles", category="accessories", quantity=1, essential=True),
        PackingItem(name="Ski Socks", category="clothing", quantity=3, essential=True),
        PackingItem(name="Base Layers", category="clothing", quantity=2, essential=True),
        PackingItem(name="Fleece Mid-layer", category="clothing", quantity=1),
        PackingItem(name="Neck Gaiter", category="accessories", quantity=1),
        PackingItem(name="Lip Balm with SPF", category="toiletries", quantity=1),
        PackingItem(name="Sunscreen", category="toiletries", quantity=1, essential=True, notes="Snow reflects UV"),
    ],
    "photography": [
        PackingItem(name="Camera", category="electronics", quantity=1, essential=True),
        PackingItem(name="Extra Batteries", category="electronics", quantity=2, essential=True),
        PackingItem(name="Memory Cards", category="electronics", quantity=2, essential=True),
        PackingItem(name="Camera Cleaning Kit", category="accessories", quantity=1),
        PackingItem(name="Tripod", category="equipment", quantity=1),
        PackingItem(name="Camera Bag", category="accessories", quantity=1, essential=True),
        PackingItem(name="Lens Filters", category="electronics", quantity=1),
        PackingItem(name="Backup Storage Device", category="electronics", quantity=1),
    ],
    "snorkeling": [
        PackingItem(name="Snorkel Mask", category="equipment", quantity=1, essential=True, notes="Or rent at destination"),
        PackingItem(name="Snorkel", category="equipment", quantity=1, essential=True, notes="Or rent at destination"),
        PackingItem(name="Fins", category="equipment", quantity=1, notes="Or rent at destination"),
        PackingItem(name="Rashguard", category="clothing", quantity=1, notes="Sun protection"),
        PackingItem(name="Waterproof Sunscreen", category="toiletries", quantity=1, essential=True),
        PackingItem(name="Waterproof Bag", category="accessories", quantity=1),
        PackingItem(name="Water Shoes", category="footwear", quantity=1),
    ],
    "cycling": [
        PackingItem(name="Cycling Shorts", category="clothing", quantity=2, essential=True),
        PackingItem(name="Cycling Jersey", category="clothing", quantity=2),
        PackingItem(name="Cycling Shoes", category="footwear", quantity=1, essential=True),
        PackingItem(name="Helmet", category="equipment", quantity=1, essential=True),
        PackingItem(name="Cycling Gloves", category="accessories", quantity=1),
        PackingItem(name="Sunglasses", category="accessories", quantity=1),
        PackingItem(name="Repair Kit", category="tools", quantity=1),
        PackingItem(name="Water Bottle", category="accessories", quantity=1, essential=True),
        PackingItem(name="Energy Bars/Gels", category="food", quantity=3),
    ],
    "running": [
        PackingItem(name="Running Shoes", category="footwear", quantity=1, essential=True),
        PackingItem(name="Running Shorts", category="clothing", quantity=2),
        PackingItem(name="Moisture-wicking Shirts", category="clothing", quantity=2),
        PackingItem(name="Running Socks", category="clothing", quantity=2),
        PackingItem(name="Sports Watch/GPS", category="electronics", quantity=1),
        PackingItem(name="Armband for Phone", category="accessories", quantity=1),
        PackingItem(name="Hydration Belt", category="accessories", quantity=1),
        PackingItem(name="Sunglasses", category="accessories", quantity=1),
        PackingItem(name="Cap", category="accessories", quantity=1),
    ],
}

# Gender-specific items
GENDER_ITEMS = {
    "female": [
        PackingItem(name="Feminine Hygiene Products", category="toiletries", quantity=1, essential=True),
        PackingItem(name="Makeup", category="toiletries", quantity=1),
        PackingItem(name="Hair Styling Tools", category="toiletries", quantity=1),
        PackingItem(name="Hair Accessories", category="accessories", quantity=1),
        PackingItem(name="Birth Control", category="medication", quantity=1, essential=True, notes="If applicable"),
        PackingItem(name="Jewelry", category="accessories", quantity=1),
    ],
    "male": [
        PackingItem(name="Razor/Shaving Cream", category="toiletries", quantity=1),
        PackingItem(name="Beard Trimmer", category="toiletries", quantity=1),
        PackingItem(name="Aftershave", category="toiletries", quantity=1),
    ],
}

# Age group specific items
AGE_ITEMS = {
    "infant": [
        PackingItem(name="Diapers", category="baby", quantity=20, essential=True),
        PackingItem(name="Baby Wipes", category="baby", quantity=1, essential=True),
        PackingItem(name="Baby Food/Formula", category="baby", quantity=1, essential=True),
        PackingItem(name="Bottles", category="baby", quantity=2, essential=True),
        PackingItem(name="Baby Clothes", category="clothing", quantity=5, essential=True),
        PackingItem(name="Baby Blanket", category="baby", quantity=1),
        PackingItem(name="Pacifier", category="baby", quantity=2),
        PackingItem(name="Baby Carrier", category="baby", quantity=1, essential=True),
        PackingItem(name="Diaper Rash Cream", category="baby", quantity=1),
        PackingItem(name="Baby Toys", category="entertainment", quantity=3),
    ],
    "child": [
        PackingItem(name="Kids' Clothes", category="clothing", quantity=5, essential=True),
        PackingItem(name="Kids' Shoes", category="footwear", quantity=2, essential=True),
        PackingItem(name="Favorite Toy/Stuffed Animal", category="entertainment", quantity=1),
        PackingItem(name="Coloring Book/Crayons", category="entertainment", quantity=1),
        PackingItem(name="Tablet with Games", category="electronics", quantity=1),
        PackingItem(name="Kid-safe Sunscreen", category="toiletries", quantity=1, essential=True),
        PackingItem(name="Child Medication", category="medication", quantity=1, essential=True, notes="If needed"),
        PackingItem(name="Snacks", category="food", quantity=1, essential=True),
    ],
    "senior": [
        PackingItem(name="Prescription Medications", category="medication", quantity=1, essential=True, notes="Extra supply"),
        PackingItem(name="Pill Organizer", category="health", quantity=1),
        PackingItem(name="Reading Glasses", category="accessories", quantity=1, essential=True),
        PackingItem(name="Medical Alert Bracelet", category="accessories", quantity=1, notes="If applicable"),
        PackingItem(name="Medical Insurance Cards", category="documents", quantity=1, essential=True),
        PackingItem(name="List of Medications", category="documents", quantity=1, essential=True),
        PackingItem(name="Mobility Aids", category="health", quantity=1, essential=True, notes="If needed"),
        PackingItem(name="Extra Prescription Copies", category="documents", quantity=1, essential=True),
    ],
}

# Duration-specific adjustments
DURATION_MULTIPLIERS = {
    "clothing": {
        "short": 1,      # 1-3 days
        "medium": 1.5,   # 4-7 days
        "long": 2,       # 8-14 days
        "extended": 2.5  # 15+ days
    },
    "toiletries": {
        "short": 1,
        "medium": 1,
        "long": 2,
        "extended": 3
    }
}

def generate_packing_list(request: PackingListRequest) -> List[PackingItem]:
    """Generate a packing list based on the request parameters using rule-based approach."""
    items = BASE_ITEMS.copy()
    
    # Add season-specific items
    if request.season.lower() in SEASON_ITEMS:
        items.extend(SEASON_ITEMS[request.season.lower()])
    
    # Add trip type-specific items
    if request.trip_type.lower() in TRIP_TYPE_ITEMS:
        items.extend(TRIP_TYPE_ITEMS[request.trip_type.lower()])
    
    # Add destination-specific items
    destination_found = False
    for destination, dest_items in DESTINATION_ITEMS.items():
        if destination in request.destination.lower():
            items.extend(dest_items)
            destination_found = True
            break
    
    # If no specific destination was found, add universal travel items
    if not destination_found:
        items.append(PackingItem(name="Universal Power Adapter", category="electronics", quantity=1, essential=True))
        items.append(PackingItem(name="Travel Phrase Book/App", category="documents", quantity=1))
    
    # Add activity-specific items
    for activity in request.activities:
        if activity.lower() in ACTIVITY_ITEMS:
            items.extend(ACTIVITY_ITEMS[activity.lower()])
    
    # Add gender-specific items
    if request.gender and request.gender.lower() in GENDER_ITEMS:
        items.extend(GENDER_ITEMS[request.gender.lower()])
    
    # Add age-specific items
    if request.age_group and request.age_group.lower() in AGE_ITEMS:
        items.extend(AGE_ITEMS[request.age_group.lower()])
    
    # Determine duration category
    duration_category = "short"
    if request.duration <= 3:
        duration_category = "short"
    elif request.duration <= 7:
        duration_category = "medium"
    elif request.duration <= 14:
        duration_category = "long"
    else:
        duration_category = "extended"
    
    # Adjust quantities based on trip duration
    for item in items:
        # Scale clothing items by duration
        if item.category in DURATION_MULTIPLIERS and not item.essential:
            multiplier = DURATION_MULTIPLIERS[item.category][duration_category]
            item.quantity = min(round(item.quantity * multiplier), 10)  # Cap at 10
        
        # For really long trips, add laundry supplies
        if duration_category == "extended" and item == items[0]:  # Add only once
            items.append(PackingItem(name="Travel Laundry Soap", category="toiletries", quantity=1))
    
    # Add weather-specific items if needed
    if "rainy" in request.season.lower() or "monsoon" in request.season.lower():
        items.extend(SEASON_ITEMS["rainy"])
    
    if "tropical" in request.season.lower() or any(d in request.destination.lower() for d in ["caribbean", "bali", "hawaii", "thailand"]):
        items.extend(SEASON_ITEMS["tropical"])
    
    # Special case for business trips with presentations
    if request.trip_type.lower() == "business" and any("presentation" in a.lower() for a in request.activities):
        items.append(PackingItem(name="Presentation Remote", category="electronics", quantity=1))
        items.append(PackingItem(name="Backup of Presentation", category="documents", quantity=1, essential=True))
    
    # Remove duplicate items (keeping the ones with higher quantities)
    unique_items = {}
    for item in items:
        if item.name in unique_items:
            if item.quantity > unique_items[item.name].quantity or item.essential and not unique_items[item.name].essential:
                unique_items[item.name] = item
        else:
            unique_items[item.name] = item
    
    return list(unique_items.values())

@app.get("/")
async def root():
    return {
        "service": "Packing List Service",
        "version": "1.0.0",
        "model": "Rule-based",
        "endpoints": [
            "/generate"
        ]
    }

@app.post("/generate", response_model=PackingListResponse)
async def generate_packing_list_endpoint(request: PackingListRequest):
    items = generate_packing_list(request)
    
    return PackingListResponse(
        items=items,
        destination=request.destination,
        duration=request.duration,
        season=request.season,
        trip_type=request.trip_type
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)




# Test the packing list service

# if __name__ == "__main__":
#     # Example request
#     example_request = PackingListRequest(
#         destination="Paris",
#         duration=7,
#         season="summer",
#         trip_type="leisure",
#         activities=["sightseeing", "dining"],
#         gender="any",
#         age_group="adult"
#     )
    
#     # Make request to the API
#     import requests
#     import json
    
#     response = requests.post(
#         "http://localhost:8003/generate",
#         json=example_request.dict()
#     )
    
#     # Print response
#     if response.status_code == 200:
#         packing_list = response.json()
#         print("\nGenerated Packing List:")
#         print(f"Destination: {packing_list['destination']}")
#         print(f"Duration: {packing_list['duration']} days")
#         print(f"Season: {packing_list['season']}")
#         print("\nItems:")
#         for item in packing_list['items']:
#             print(f"- {item['quantity']}x {item['name']} ({item['category']})")
#     else:
#         print(f"Error: {response.status_code}")
#         print(response.json())

