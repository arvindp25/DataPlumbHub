terraform {

  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.20.0"
    }
  }
  backend "gcs" {
    bucket     = "to_be_overridden_by_init_command"
  }
}

provider "google" {
  project     = var.gcp_project_id
  region      = "asia-south1" 
}

resource "google_storage_bucket" "static" {
 name          = "test_bucket_1124"
 location = "asia-south1"
 storage_class = "STANDARD"

#  uniform_bucket_level_access = true
}