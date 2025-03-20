# Travel Assistant Application

A microservices-based application that provides translation, mapping, and packing list services for travelers.

## Architecture

The application consists of the following components:

- **API Gateway**: Unified entry point for all client requests (web/mobile)
- **Translation Service**: Provides text translation and TTS audio generation
- **Map Service**: Provides information about famous places and integrates with mapping APIs
- **Packing List Service**: Generates dynamic packing lists based on destination, duration, and season

## Development Setup

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- MongoDB (for Translation Service and Map Service data storage)
- Google Cloud Project with Text-to-Speech and Storage APIs enabled (for TTS functionality)

### Setup Instructions

1. Clone the repository:
   ```
   git clone [repository-url]
   cd TravelAssistant
   ```

2. Configure MongoDB:
   - Create a `.env` file in the root directory (copy from `.env.example`)
   - Set your MongoDB connection string in the `.env` file
   - This connection will be used by both the Translation Service and Map Service
   - Each service uses a different database within the same MongoDB instance

3. Configure Google Cloud (for TTS functionality):
   - Create a Google Cloud Project and enable the Text-to-Speech and Storage APIs
   - Create a service account with access to these APIs
   - Download the service account key (JSON format)
   - Set the path to your service account key in the `.env` file
   - Configure the GCP project ID and GCS bucket name in the `.env` file

4. Seed the databases:
   ```
   # Translation Service common phrases
   cd translation_service
   python seed_data.py
   
   # Map Service places
   cd ../map_service
   python seed_data.py
   ```

5. Install dependencies for each service:
   ```
   # In each service directory
   pip install -r requirements.txt
   ```

6. Run using Docker Compose:
   ```
   docker-compose up --build
   ```

7. Access the API Gateway at: http://localhost:8000

## API Documentation

Once the services are running, you can access the API documentation at:
- API Gateway: http://localhost:8000/docs
- Translation Service: http://localhost:8001/docs
- Map Service: http://localhost:8002/docs
- Packing List Service: http://localhost:8003/docs

## Authentication

The application uses JWT-based authentication through the API Gateway.

## Services

### Translation Service
- Text translation between multiple languages
- Text-to-speech audio generation using Google Cloud TTS
- High-quality voice synthesis with 9+ languages supported
- Audio files stored in Google Cloud Storage for efficient delivery
- Common phrases database with pre-translated content
- MongoDB storage for common phrases

### Map Service
- Information about famous places in different destinations
- Integration with third-party mapping APIs
- MongoDB storage for place information

### Packing List Service
- Dynamic generation of packing lists based on:
  - Destination
  - Duration of stay
  - Season/weather
  - Trip type (business, leisure, etc.) 