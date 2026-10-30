variable "project_name" {
  type        = string
  description = "Base name for the new GCP project"
  default     = "soappoc"
}

variable "org_id" {
  type        = string
  description = "GCP Organization ID"
}

variable "billing_account_id" {
  type        = string
  description = "GCP Billing Account ID"
}

variable "region" {
  type        = string
  description = "Default GCP Region"
  default     = "us-central1"
}
