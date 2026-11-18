import csv
from pathlib import Path
import requests

QUERY_URL = (
    "https://services6.arcgis.com/nyYfO9SxHU2ChQd9/arcgis/rest/services/Service_Requests_2023_until_20_May_2026/FeatureServer/0/query"
)
OUTPUT_CSV = Path("data/test/sample_no_power_1000.csv")

#"where": "C3_Complaint_Type = 'No Power'",
params = {
    "where": "1 = 1",
    "outFields": "*",
    "returnGeometry": "false",
    "f": "json",
    "resultRecordCount": 1000,
    "orderByFields": "OBJECTID ASC",
}

response = requests.get(QUERY_URL, params=params, timeout=30)
response.raise_for_status()
data = response.json()

if "error" in data:
    raise RuntimeError(f"ArcGIS API error: {data['error']}")

records = [feature["attributes"] for feature in data.get("features", [])]

if records:
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    print(f"Saved {len(records)} rows to {OUTPUT_CSV}")
else:
    print("No matching records found.")
