
#check if the required package is installed, else exit and guide for install  
try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError as exc:
    raise SystemExit(
        "Missing required package, please see readme 'Setup and Installation'. "
        "Please install dependencies with: pip install -r requirements.txt"
    ) from exc

# import all the packages of interest here
import argparse
import csv
import json
import logging
from pathlib import Path
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# We want to be able to log some information we configure that here 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Set the configuration files here to keep the assessment code in one place
api_url = (
    "https://services6.arcgis.com/nyYfO9SxHU2ChQd9/arcgis/rest/services/Service_Requests_2023_until_20_May_2026/FeatureServer/0/query"
)
where_clause = "C3_Complaint_Type = 'No Power'"
batch_size = 1000

raw_dir = Path("../data/raw")
processed_csv = Path("../data/no_power_service_requests.csv")
summary_csv = Path("../data/no_power_service_requests_sub_summary.csv")


def create_retrying_session(
    retries: int = 5, backoff_factor: float = 1.0
) -> requests.Session:
    """Create a requests Session configured with exponential backoff retries."""
    session = requests.Session()
    retry_strategy = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def fetch_and_save_raw(session: requests.Session) -> list[dict]:
    """Paginate through ArcGIS REST API, cache raw JSON pages, and return attributes."""
    raw_dir.mkdir(parents=True, exist_ok=True)

    # Clear stale cached pages before a fresh download so old pages don't linger
    for old_file in raw_dir.glob("no_power_page_*.json"):
        old_file.unlink()

    all_records: list[dict] = []
    offset = 0
    page = 1

    while True:
        params = {
            "where": where_clause,
            "outFields": "*",
            "returnGeometry": "false",
            "f": "json",
            "resultOffset": offset,
            "resultRecordCount": batch_size,
            "orderByFields": "OBJECTID ASC",
        }

        logger.info(
            "Requesting page %d (offset=%d, limit=%d)...",
            page,
            offset,
            batch_size,
        )

        try:
            response = session.get(api_url, params=params, timeout=(10, 60))
            response.raise_for_status()
            payload = response.json()
        except requests.exceptions.Timeout:
            logger.error("Request timed out at offset %d.", offset)
            raise
        except requests.exceptions.RequestException as exc:
            logger.error(
                "Network or HTTP error at offset %d: %s", offset, exc
            )
            raise
        except ValueError as exc:
            logger.error(
                "Invalid JSON received from server at offset %d: %s",
                offset,
                exc,
            )
            raise

        # ArcGIS APIs often return HTTP 200 even when a query error occurs inside the JSON
        if "error" in payload:
            error_info = payload["error"]
            logger.error("ArcGIS API returned an error payload: %s", error_info)
            raise RuntimeError(f"ArcGIS Query Error: {error_info}")

        features = payload.get("features")
        if features is None or not isinstance(features, list):
            logger.error(
                "Unexpected response structure (missing 'features' list): %s",
                list(payload.keys()),
            )
            raise ValueError("Unexpected API response format.")

        # Save raw API response page to data/raw/ for offline rebuilds
        raw_file = raw_dir / f"no_power_page_{page:04d}.json"
        with raw_file.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        logger.debug("Saved raw response to %s", raw_file)

        if not features:
            logger.info("No more records returned. Extraction complete.")
            break

        batch_records = [feat.get("attributes", {}) for feat in features]
        all_records.extend(batch_records)
        logger.info(
            "Fetched %d records on page %d (Running total: %d)",
            len(batch_records),
            page,
            len(all_records),
        )

        exceeded_limit = payload.get("exceededTransferLimit", False)
        if len(features) < batch_size and not exceeded_limit:
            logger.info("Reached final page of results.")
            break

        offset += len(features)
        page += 1
        time.sleep(0.25)

    return all_records


def load_from_cache(raw_dir: Path) -> list[dict]:
    """Read cached JSON page files from data/raw/ without making network calls."""
    cached_files = sorted(raw_dir.glob("no_power_page_*.json"))
    if not cached_files:
        raise FileNotFoundError(
            f"No cached JSON files found in '{raw_dir}'. Run without --from-cache first."
        )

    logger.info("Loading %d cached page(s) from %s...", len(cached_files), raw_dir)
    all_records: list[dict] = []

    for file_path in cached_files:
        try:
            with file_path.open("r", encoding="utf-8") as f:
                payload = json.load(f)
        except (OSError, ValueError) as exc:
            logger.error("Failed to read cached file %s: %s", file_path, exc)
            raise

        features = payload.get("features", [])
        batch_records = [feat.get("attributes", {}) for feat in features]
        all_records.extend(batch_records)
        logger.debug("Loaded %d records from %s", len(batch_records), file_path.name)

    logger.info("Loaded %d total records from local cache.", len(all_records))
    return all_records


def export_to_csv(records: list[dict], output_path: Path) -> None:
    """Write extracted attribute dictionaries to a CSV file."""
    if not records:
        logger.warning("No records found; skipping CSV creation.")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(records[0].keys())

    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    logger.info("Exported %d rows to %s", len(records), output_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract 'No Power' service requests from ArcGIS REST API or local cache."
    )
    parser.add_argument(
        "--from-cache",
        action="store_true",
        help="Rebuild the CSV from cached JSON files in data/raw/ without calling the API.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        if args.from_cache:
            logger.info("Running in offline rebuild mode (--from-cache).")
            records = load_from_cache(raw_dir)
        else:
            logger.info("Starting live API extraction with filter: %s", where_clause)
            session = create_retrying_session(retries=5, backoff_factor=1.0)
            try:
                records = fetch_and_save_raw(session)
            finally:
                session.close()

        export_to_csv(records, processed_csv)
        logger.info("Pipeline finished successfully.")
    except Exception as exc:
        logger.critical("Pipeline failed: %s", exc)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
