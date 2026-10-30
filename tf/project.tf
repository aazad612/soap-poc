resource "random_id" "project_suffix" {
  byte_length = 3
}

resource "google_project" "soappoc" {
  name            = var.project_name
  project_id      = "${var.project_name}-${random_id.project_suffix.hex}"
  org_id          = var.org_id
  billing_account = var.billing_account_id
}
