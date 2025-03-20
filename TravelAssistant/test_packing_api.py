import requests
import json
import sys

def test_packing_list_api(port=None):
    # Try specific port if provided, or try different ports
    ports = [port] if port else [8003, 8004, 8005, 8006, 8007]
    base_url = None
    
    # First find which port the server is running on
    for port in ports:
        try:
            url = f"http://localhost:{port}"
            print(f"Checking server on {url}...")
            response = requests.get(
                url,
                timeout=2  # 2 second timeout
            )
            if response.status_code == 200:
                info = response.json()
                print(f"Found server on port {port}")
                print(f"Service: {info.get('service')}")
                print(f"Version: {info.get('version')}")
                print(f"Model: {info.get('model', 'Unknown')}")
                base_url = url
                break
        except requests.exceptions.RequestException as e:
            print(f"No server on port {port}")
    
    if not base_url:
        print("Could not find a running packing list service")
        return
    
    # Example request
    request_data = {
        "destination": "Paris",
        "duration": 7,
        "season": "summer",
        "trip_type": "leisure",
        "activities": ["sightseeing", "dining"],
        "gender": "any",
        "age_group": "adult"
    }
    
    print(f"\nSending request to {base_url}/generate...")
    response = requests.post(
        f"{base_url}/generate",
        json=request_data
    )
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return
    
    # Print response
    packing_list = response.json()
    print("\nGenerated Packing List:")
    print(f"Destination: {packing_list['destination']}")
    print(f"Duration: {packing_list['duration']} days")
    print(f"Season: {packing_list['season']}")
    print(f"Trip Type: {packing_list['trip_type']}")
    print("\nItems:")
    
    # Group items by category
    items_by_category = {}
    for item in packing_list['items']:
        category = item['category']
        if category not in items_by_category:
            items_by_category[category] = []
        items_by_category[category].append(item)
    
    # Print items by category
    for category, items in sorted(items_by_category.items()):
        print(f"\n{category.upper()}:")
        for item in items:
            essential_mark = " *" if item['essential'] else ""
            notes = f" - {item['notes']}" if item['notes'] else ""
            print(f"- {item['quantity']}x {item['name']}{essential_mark}{notes}")
    
    print("\n* Essential items")
    
    # Return the response for further processing if needed
    return packing_list

if __name__ == "__main__":
    # Check if a port is specified as a command-line argument
    port = int(sys.argv[1]) if len(sys.argv) > 1 else None
    test_packing_list_api(port) 