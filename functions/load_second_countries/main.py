import os
import json
from datetime import datetime, timezone
import functions_framework
from google.cloud import bigquery
from zeep import Client
from zeep.helpers import serialize_object

WSDL_URL = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL"
PROJECT_ID = os.environ.get("GCP_PROJECT", "soappoc-fb85c7")
TABLE_NAME = os.environ.get("TABLE_NAME", "second_countries")
TABLE_ID = f"{PROJECT_ID}.bronze.{TABLE_NAME}"

@functions_framework.http
def load_countries_k_to_r(request):
    """Fetches countries from SOAP and loads K-R countries into bronze table."""
    client = Client(wsdl=WSDL_URL)
    all_countries = client.service.ListOfCountryNamesByName()
    
    allowed_letters = set("KLMNOPQR")
    filtered = [
        c for c in all_countries 
        if c.sName and c.sName.strip() and c.sName.strip()[0].upper() in allowed_letters
    ]

    now_iso = datetime.now(timezone.utc).isoformat()
    rows = [
        {
            "iso_code": c.sISOCode,
            "name": c.sName,
            "capital_city": None,
            "phone_code": None,
            "continent_code": None,
            "currency_iso_code": None,
            "flag_url": None,
            "languages": [],
            "raw_payload": json.dumps(serialize_object(c)),
            "ingested_at": now_iso
        }
        for c in filtered
    ]

    bq_client = bigquery.Client(project=PROJECT_ID)
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        schema_update_options=[bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION]
    )
    job = bq_client.load_table_from_json(rows, TABLE_ID, job_config=job_config)
    job.result()

    return {
        "status": "success",
        "batch": "K-R",
        "loaded_count": len(rows),
        "target_table": TABLE_ID,
        "sample": [r["name"] for r in rows[:5]]
    }, 200
