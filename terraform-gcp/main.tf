# Terraform configuration for Filosofía App on GCP
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.84"
    }
  }
  
  # Optional: Use GCS backend for state
  # backend "gcs" {
  #   bucket = "filosofia-app-terraform-state"
  #   prefix = "terraform/state"
  # }
}

# Configure the Google Cloud Provider
provider "google" {
  project = var.project_id
  region  = var.region
}

# Variables
variable "project_id" {
  description = "The GCP project ID"
  type        = string
  default     = "piratephilosopher"
}

variable "region" {
  description = "The GCP region"
  type        = string
  default     = "europe-southwest1"
}

variable "function_name" {
  description = "Name of the Cloud Function"
  type        = string
  default     = "filosofia-api"
}

# Enable required APIs
resource "google_project_service" "apis" {
  for_each = toset([
    "cloudfunctions.googleapis.com",
    "firestore.googleapis.com",
    "storage.googleapis.com",
    "cloudbuild.googleapis.com",
    "run.googleapis.com"
  ])
  
  project = var.project_id
  service = each.value
  
  disable_on_destroy = false
}

# Create Firestore database
resource "google_firestore_database" "database" {
  project     = var.project_id
  name        = "(default)"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"
  
  depends_on = [google_project_service.apis]
}

# Storage bucket for Cloud Functions source code
resource "google_storage_bucket" "functions_bucket" {
  name     = "${var.project_id}-functions-source"
  location = var.region
  
  # Enable versioning for source code
  versioning {
    enabled = true
  }
  
  # Lifecycle management
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
  
  depends_on = [google_project_service.apis]
}

# Optional: Storage bucket for static assets (images, etc.)
resource "google_storage_bucket" "assets_bucket" {
  name     = "${var.project_id}-assets"
  location = var.region
  
  # Make bucket publicly readable for static assets
  uniform_bucket_level_access = true
  
  depends_on = [google_project_service.apis]
}

# Make assets bucket public
resource "google_storage_bucket_iam_binding" "assets_public" {
  bucket = google_storage_bucket.assets_bucket.name
  role   = "roles/storage.objectViewer"
  
  members = [
    "allUsers",
  ]
}

# Outputs
output "project_id" {
  description = "The GCP project ID"
  value       = var.project_id
}

output "region" {
  description = "The GCP region"
  value       = var.region
}

output "firestore_database" {
  description = "Firestore database name"
  value       = google_firestore_database.database.name
}

output "functions_bucket" {
  description = "Functions source bucket name"
  value       = google_storage_bucket.functions_bucket.name
}

output "assets_bucket" {
  description = "Assets bucket name"  
  value       = google_storage_bucket.assets_bucket.name
}

output "assets_bucket_url" {
  description = "Assets bucket public URL"
  value       = "https://storage.googleapis.com/${google_storage_bucket.assets_bucket.name}"
}