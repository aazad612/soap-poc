CREATE TABLE IF NOT EXISTS `bronze.first_countries` (
  iso_code STRING OPTIONS(description="2-letter ISO country code"),
  name STRING OPTIONS(description="Country name"),
  capital_city STRING OPTIONS(description="Capital city"),
  phone_code STRING OPTIONS(description="International dialing code"),
  continent_code STRING OPTIONS(description="2-letter continent code"),
  currency_iso_code STRING OPTIONS(description="Currency code e.g. USD"),
  flag_url STRING OPTIONS(description="URL to country flag image"),
  languages ARRAY<STRUCT<
    iso_code STRING,
    name STRING
  >> OPTIONS(description="Official/spoken languages"),
  raw_payload STRING OPTIONS(description="Raw SOAP XML / JSON payload"),
  ingested_at TIMESTAMP OPTIONS(description="Ingestion timestamp")
);
