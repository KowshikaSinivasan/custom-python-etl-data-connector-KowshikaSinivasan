# Cisco Talos ETL Connector

## Overview
This connector extracts threat intelligence data from Cisco Talos Reputation Center, 
transforms the raw HTML response into a MongoDB-storable format, and loads it into MongoDB.

## Files
- `etl_connector.py`: Main ETL script
- `ENV_TEMPLATE`: Placeholder for required environment variables (no secrets)
- `.env`: Local file with real environment variables (not committed)
- `requirements.txt`: Python dependencies
- `README.md`: Instructions

## Setup Instructions
1. Clone the repository and checkout your branch (`Kowshika_3122225001063_B`).
2. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create `.env` file in the same directory:
   ```ini
   MONGO_URI=mongodb://localhost:27017
   TALOS_API_KEY=your_real_talos_api_key_here
   ```
4. Run the ETL script:
   ```bash
   python etl_connector.py
   ```

## Notes
- Cisco Talos API currently returns HTML response. This script stores the HTML directly in MongoDB with an ingestion timestamp.
- Future improvements can include parsing the HTML into structured JSON for easier querying.

