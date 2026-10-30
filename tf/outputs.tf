output "project_id" {
  description = "The created GCP project ID"
  value       = google_project.soappoc.project_id
}

output "service_account_email" {
  description = "Service account email"
  value       = google_service_account.soap_svc.email
}

output "medallion_datasets" {
  description = "Medallion BQ datasets"
  value       = [for d in google_bigquery_dataset.medallion : d.dataset_id]
}

output "gcs_bucket_name" {
  description = "GCS bucket name"
  value       = google_storage_bucket.soap_storage.name
}
