terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.20.0"
    }
  }
}

provider "google" {
  project     = var.gcp_project_id
  region      = "us-central1" 
}

