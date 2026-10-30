resource "google_service_account" "soap_svc" {
  project      = google_project.soappoc.project_id
  account_id   = "soap-svc-account"
  display_name = "SOAP Pipeline Service Account"
  depends_on   = [google_project_service.enabled_apis]
}

resource "google_project_iam_member" "sa_roles" {
  for_each = toset([
    "roles/bigquery.dataEditor",
    "roles/bigquery.jobUser",
    "roles/storage.objectAdmin",
    "roles/dataflow.worker",
    "roles/dataflow.admin",
    "roles/cloudfunctions.developer",
    "roles/dataform.editor"
  ])
  project = google_project.soappoc.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.soap_svc.email}"
}
