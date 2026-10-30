resource "google_bigquery_dataset" "medallion" {
  for_each   = toset(["bronze", "silver", "gold"])
  project    = google_project.soappoc.project_id
  dataset_id = each.key
  location   = var.region
  depends_on = [google_project_service.enabled_apis]
}
