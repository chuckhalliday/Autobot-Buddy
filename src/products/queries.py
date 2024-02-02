import requests
import json

def fetch_data(vin):
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}*BA?format=json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        
        data = response.json()
        
        vehicle_object = data.get("Results", [])
        
        if vehicle_object:
            year = vehicle_object[10].get("Value", "")
            make = vehicle_object[7].get("Value", "")
            trim = vehicle_object[13].get("Value", "")
            model = vehicle_object[9].get("Value", "")
            
            return {
                "vehicle_model": f"{year} {make} {model} {trim}",
                "year": year,
                "make": make,
                "model": model,
                "show_text": True
            }
        
    except requests.exceptions.RequestException as e:
        print(f"Something went wrong: {e}")
    
    return None