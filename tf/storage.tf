resource "google_storage_bucket" "soap_storage" {
  project       = google_project.soappoc.project_id
  name          = "${google_project.soappoc.project_id}-data"
  location      = var.region
  force_destroy = true
  depends_on    = [google_project_service.enabled_apis]
}
