import requests
import json
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
    API_TOKEN = os.getenv("API_TOKEN")
except ImportError:
    # Fallback to hardcoded token if dotenv is not installed
    API_TOKEN = "1eaef4025e12865eecf2a34875493365a38745eddbe863e3fd3f1333eac37415"


API_URL = "https://api.brightdata.com/datasets/v3/snapshot/s_m4r993dq1cv5kh0mvg"


headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# Parameters
params = {
    "format": "json"
}

def collect_data() -> bool:
    """Collect data from the API and save to file"""
    try:
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, indent=4, ensure_ascii=False)
        
        print("Data successfully collected and saved to data.json")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    collect_data()
