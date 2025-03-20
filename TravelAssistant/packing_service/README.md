# Packing List Service

This service generates detailed packing lists for travel based on destination, duration, season, and activities.

## Features

- **Rule-based packing list generation**: Provides reliable, consistent recommendations for travel items.
- **Trip customization**: Considers destination, season, trip type (business/leisure), and planned activities.
- **Personal preferences**: Optional gender and age group parameters for more tailored suggestions.
- **Smart quantity adjustments**: Automatically adjusts clothing quantities for longer trips.

## Getting Started

### Running the Service

The service runs inside a Docker container as part of the Travel Assistant application:

```bash
# Build and start the service
docker-compose build packing_service
docker-compose up -d packing_service
```

### Local Development

To run the service directly on your local machine:

```bash
cd packing_service
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8003
```

## Testing

A test script is included to verify the service functionality:

```bash
# Start the service first, then run the test script
python test_model.py
```

## API Endpoints

### Generate Packing List

```
POST /generate
```

Request body:
```json
{
  "destination": "Paris",
  "duration": 7,
  "season": "summer",
  "trip_type": "leisure",
  "activities": ["sightseeing", "dining"],
  "gender": "any",
  "age_group": "adult"
}
```

Response:
```json
{
  "items": [
    {
      "name": "Passport",
      "category": "documents",
      "quantity": 1,
      "essential": true,
      "notes": null
    },
    ...
  ],
  "destination": "Paris",
  "duration": 7,
  "season": "summer",
  "trip_type": "leisure"
}
```

## How It Works

The packing list service uses a sophisticated rule-based system to generate recommendations:

1. **Base items** - Essential items that everyone needs regardless of trip details
2. **Season-specific items** - Items selected based on the season (summer, winter, spring, fall)
3. **Trip type items** - Items appropriate for business, leisure, beach, or adventure trips
4. **Destination-specific items** - Special items needed for particular destinations
5. **Activity-based items** - Items needed for activities like swimming, hiking, skiing, etc.

The service combines these categories and removes duplicates to create a comprehensive, 
personalized packing list for each user's unique travel needs. 