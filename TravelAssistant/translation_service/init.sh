#!/bin/bash

# Wait for MongoDB service to be ready
echo "Waiting for MongoDB to be ready..."
sleep 2

# Run the seed script to populate the database
echo "Seeding the database with initial common phrases..."
python seed_data.py

# Start the Translation Service
echo "Starting the Translation Service..."
uvicorn main:app --host 0.0.0.0 --port 8001 