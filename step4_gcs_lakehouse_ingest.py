"""
Step 4: GCS Lakehouse Landing (Bronze Pattern)
SOAP API -> Raw .jsonl to GCS (gs://soappoc-fb85c7-data/raw/) -> BQ Load Job to bronze.countries
"""

import os
import json
import tempfile
from datetime import datetime, timezone
from google.cloud import storage, bigquery
from zeep import Client
from zeep.helpers import serialize_object

# Configuration
WSDL_URL = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL"
PROJECT_ID = os.environ.get("GCP_PROJECT", "soappoc-fb85c7")
BUCKET_NAME = "soappoc-fb85c7-data"
TABLE_ID = f"{PROJECT_ID}.bronze.countries"

print(f"1. Fetching all countries from SOAP service at:\n   {WSDL_URL}")
client = Client(wsdl=WSDL_URL)
all_countries = client.service.ListOfCountryNamesByName()
print(f"   Fetched {len(all_countries)} countries from SOAP endpoint.")

# 2. Serialize to newline-delimited JSON (.jsonl)
now_utc = datetime.now(timezone.utc)
timestamp_str = now_utc.strftime("%Y%m%d_%H%M%S")
gcs_blob_name = f"raw/countries_{timestamp_str}.jsonl"

with tempfile.NamedTemporaryFile("w+", suffix=".jsonl", delete=False) as tmp_file:
    tmp_path = tmp_file.name
    for c in all_countries:
        row = {
            "iso_code": c.sISOCode,
            "name": c.sName,
            "capital_city": None,
            "phone_code": None,
            "continent_code": None,
            "currency_iso_code": None,
            "flag_url": None,
            "languages": [],
            "raw_payload": json.dumps(serialize_object(c)),
            "ingested_at": now_utc.isoformat()
        }
        tmp_file.write(json.dumps(row) + "\n")

# 3. Upload to GCS raw landing zone
print(f"\n2. Uploading raw .jsonl to GCS Lakehouse: gs://{BUCKET_NAME}/{gcs_blob_name}")
storage_client = storage.Client(project=PROJECT_ID)
bucket = storage_client.bucket(BUCKET_NAME)
blob = bucket.blob(gcs_blob_name)
blob.upload_from_filename(tmp_path)
os.remove(tmp_path)
print("   Uploaded successfully to GCS raw zone.")

# 4. Trigger BigQuery Load Job from GCS URI
gcs_uri = f"gs://{BUCKET_NAME}/{gcs_blob_name}"
print(f"\n3. Triggering BigQuery Load Job into: {TABLE_ID}")
bq_client = bigquery.Client(project=PROJECT_ID)

schema = [
    bigquery.SchemaField("iso_code", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("name", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("capital_city", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("phone_code", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("continent_code", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("currency_iso_code", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("flag_url", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("languages", "RECORD", mode="REPEATED", fields=[
        bigquery.SchemaField("iso_code", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("name", "STRING", mode="NULLABLE")
    ]),
    bigquery.SchemaField("raw_payload", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("ingested_at", "TIMESTAMP", mode="NULLABLE")
]

job_config = bigquery.LoadJobConfig(
    schema=schema,
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    create_disposition=bigquery.CreateDisposition.CREATE_IF_NEEDED
)

load_job = bq_client.load_table_from_uri(gcs_uri, TABLE_ID, job_config=job_config)
print(f"   Load job started (ID: {load_job.job_id}). Waiting for completion...")
load_job.result()  # Wait for job to finish

table = bq_client.get_table(TABLE_ID)
print(f"\n4. Success! Table {TABLE_ID} now has {table.num_rows} total rows.")
