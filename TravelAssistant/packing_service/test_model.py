import requests
import json
from typing import Dict, Any

def test_packing_service(data: Dict[str, Any]) -> None:
    """Test the packing service with the provided data."""
    print(f"Testing packing list generation for {data['destination']}...")
    try:
        response = requests.post(
            "http://localhost:8003/generate",
            json=data
        )
        
        if response.status_code == 200:
            packing_list = response.json()
            print("\nGenerated Packing List:")
            print(f"Destination: {packing_list['destination']}")
            print(f"Duration: {packing_list['duration']} days")
            print(f"Season: {packing_list['season']}")
            print(f"Trip type: {packing_list['trip_type']}")
            
            print("\nItems:")
            for item in packing_list['items']:
                essential_mark = "[ESSENTIAL]" if item['essential'] else ""
                notes = f" - Note: {item['notes']}" if item['notes'] else ""
                print(f"- {item['quantity']}x {item['name']} ({item['category']}) {essential_mark}{notes}")
            
            return len(packing_list['items'])
        else:
            print(f"Error: {response.status_code}")
            print(response.json())
            return 0
    except Exception as e:
        print(f"Error testing packing service: {e}")
        return 0

def check_service_status() -> bool:
    """Check if the packing service is running."""
    try:
        response = requests.get("http://localhost:8003/")
        if response.status_code == 200:
            info = response.json()
            print(f"Service: {info['service']}")
            print(f"Version: {info['version']}")
            print(f"Model: {info['model']}")
            return True
        return False
    except:
        print("Error: Cannot connect to the packing service")
        return False

if __name__ == "__main__":
    # Check if service is running
    print("Checking packing service status...")
    if not check_service_status():
        print("\nError: Packing service is not running. Please start it with 'docker-compose up -d packing_service'")
        exit(1)
    
    # Example requests
    test_cases = [
        {
            "destination": "Paris",
            "duration": 7,
            "season": "summer",
            "trip_type": "leisure",
            "activities": ["sightseeing", "dining"],
            "gender": "any",
            "age_group": "adult"
        },
        {
            "destination": "Tokyo",
            "duration": 5,
            "season": "spring",
            "trip_type": "business",
            "activities": ["meetings", "dining"],
            "gender": "male",
            "age_group": "adult"
        },
        {
            "destination": "New York",
            "duration": 3,
            "season": "winter",
            "trip_type": "business",
            "activities": ["meetings", "theater"],
            "gender": "female",
            "age_group": "adult"
        }
    ]
    
    # Run tests
    total_items = 0
    for i, test_case in enumerate(test_cases):
        print(f"\n--- Test Case {i+1} ---")
        items_count = test_packing_service(test_case)
        total_items += items_count
    
    print(f"\nTests completed. Generated {total_items} items across {len(test_cases)} test cases.") 