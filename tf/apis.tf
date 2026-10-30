resource "google_project_service" "enabled_apis" {
  for_each = toset([
    "bigquery.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "iam.googleapis.com",
    "storage.googleapis.com",
    "dataflow.googleapis.com",
    "cloudfunctions.googleapis.com",
    "cloudbuild.googleapis.com",
    "artifactregistry.googleapis.com",
    "run.googleapis.com",
    "dataform.googleapis.com"
  ])
  project            = google_project.soappoc.project_id
  service            = each.key
  disable_on_destroy = false
}
