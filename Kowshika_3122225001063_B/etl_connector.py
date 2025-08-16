import os
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
TALOS_API_KEY = os.getenv("TALOS_API_KEY")

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client["etl_database"]
collection = db["talos_raw"]

def extract(query):
    """
    Extract data from Cisco Talos.
    If API key is missing, fetch the public HTML page.
    """
    url = f"https://talosintelligence.com/reputation_center/lookup?search={query}"
    
    headers = {}
    if TALOS_API_KEY:  # Only add Authorization header if key exists
        headers["Authorization"] = f"Bearer {TALOS_API_KEY}"
    else:
        print("⚠️ No TALOS_API_KEY found. Fetching public HTML page...")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text   # Talos gives HTML, not JSON
    except Exception as e:
        print("❌ Error during Talos fetch:", e)
        return None

def transform(html_data, query):
    """
    Wrap HTML response with metadata for MongoDB storage.
    """
    if not html_data:
        return None
    return {
        "query": query,
        "html_response": html_data,
        "_ingested_at": datetime.utcnow()
    }

def load(record):
    """
    Insert transformed record into MongoDB.
    """
    if record:
        collection.insert_one(record)
        print(f"✅ Record for {record['query']} inserted into MongoDB.")

if __name__ == "__main__":
    # Example query
    search_item = "8.8.8.8"  # Replace with IP or domain
    raw_data = extract(search_item)
    transformed = transform(raw_data, search_item)
    load(transformed)
