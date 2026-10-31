# Function 1: A - J
data "archive_file" "first_countries_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../functions/load_countries"
  output_path = "${path.module}/load_first_countries.zip"
}

resource "google_storage_bucket_object" "first_countries_code" {
  name   = "functions/first_countries-${data.archive_file.first_countries_zip.output_md5}.zip"
  bucket = google_storage_bucket.soap_storage.name
  source = data.archive_file.first_countries_zip.output_path
}

resource "google_cloudfunctions2_function" "load_first_countries" {
  project     = google_project.soappoc.project_id
  name        = "load-first-countries"
  location    = var.region
  description = "Ingest A-J countries into bronze.first_countries"

  build_config {
    runtime     = "python311"
    entry_point = "load_countries_a_to_j"
    source {
      storage_source {
        bucket = google_storage_bucket.soap_storage.name
        object = google_storage_bucket_object.first_countries_code.name
      }
    }
  }

  service_config {
    max_instance_count    = 1
    available_memory      = "256M"
    timeout_seconds       = 120
    service_account_email = google_service_account.soap_svc.email
    environment_variables = {
      GCP_PROJECT = google_project.soappoc.project_id
      TABLE_NAME  = "first_countries"
    }
  }

  depends_on = [
    google_project_service.enabled_apis,
    google_project_iam_member.sa_roles
  ]
}

# Function 2: K - R
data "archive_file" "second_countries_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../functions/load_second_countries"
  output_path = "${path.module}/load_second_countries.zip"
}

resource "google_storage_bucket_object" "second_countries_code" {
  name   = "functions/second_countries-${data.archive_file.second_countries_zip.output_md5}.zip"
  bucket = google_storage_bucket.soap_storage.name
  source = data.archive_file.second_countries_zip.output_path
}

resource "google_cloudfunctions2_function" "load_second_countries" {
  project     = google_project.soappoc.project_id
  name        = "load-second-countries"
  location    = var.region
  description = "Ingest K-R countries into bronze.second_countries"

  build_config {
    runtime     = "python311"
    entry_point = "load_countries_k_to_r"
    source {
      storage_source {
        bucket = google_storage_bucket.soap_storage.name
        object = google_storage_bucket_object.second_countries_code.name
      }
    }
  }

  service_config {
    max_instance_count    = 1
    available_memory      = "256M"
    timeout_seconds       = 120
    service_account_email = google_service_account.soap_svc.email
    environment_variables = {
      GCP_PROJECT = google_project.soappoc.project_id
      TABLE_NAME  = "second_countries"
    }
  }

  depends_on = [
    google_project_service.enabled_apis,
    google_project_iam_member.sa_roles
  ]
}

# Function 3: S - Z
data "archive_file" "third_countries_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../functions/load_third_countries"
  output_path = "${path.module}/load_third_countries.zip"
}

resource "google_storage_bucket_object" "third_countries_code" {
  name   = "functions/third_countries-${data.archive_file.third_countries_zip.output_md5}.zip"
  bucket = google_storage_bucket.soap_storage.name
  source = data.archive_file.third_countries_zip.output_path
}

resource "google_cloudfunctions2_function" "load_third_countries" {
  project     = google_project.soappoc.project_id
  name        = "load-third-countries"
  location    = var.region
  description = "Ingest S-Z countries into bronze.third_countries"

  build_config {
    runtime     = "python311"
    entry_point = "load_countries_s_to_z"
    source {
      storage_source {
        bucket = google_storage_bucket.soap_storage.name
        object = google_storage_bucket_object.third_countries_code.name
      }
    }
  }

  service_config {
    max_instance_count    = 1
    available_memory      = "256M"
    timeout_seconds       = 120
    service_account_email = google_service_account.soap_svc.email
    environment_variables = {
      GCP_PROJECT = google_project.soappoc.project_id
      TABLE_NAME  = "third_countries"
    }
  }

  depends_on = [
    google_project_service.enabled_apis,
    google_project_iam_member.sa_roles
  ]
}

# Invoker permissions for all 3 functions
resource "google_cloud_run_service_iam_member" "invoker" {
  for_each = {
    first  = google_cloudfunctions2_function.load_first_countries.name
    second = google_cloudfunctions2_function.load_second_countries.name
    third  = google_cloudfunctions2_function.load_third_countries.name
  }
  project  = google_project.soappoc.project_id
  location = var.region
  service  = each.value
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.soap_svc.email}"
}
