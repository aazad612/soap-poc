resource "google_cloud_scheduler_job" "country_ingest_job" {
  project     = google_project.soappoc.project_id
  name        = "daily-load-all-countries"
  description = "Trigger sequential Cloud Workflow to ingest all countries daily"
  schedule    = "0 6 * * *"
  time_zone   = "America/New_York"
  region      = var.region

  http_target {
    http_method = "POST"
    uri         = "https://workflowexecutions.googleapis.com/v1/${google_workflows_workflow.countries_pipeline.id}/executions"

    oauth_token {
      service_account_email = google_service_account.soap_svc.email
    }
  }

  depends_on = [
    google_project_service.enabled_apis,
    google_workflows_workflow.countries_pipeline
  ]
}
