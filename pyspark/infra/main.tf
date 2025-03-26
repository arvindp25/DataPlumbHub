terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.20.0"
    }
  }
}

provider "google" {
  project     = var.gcp-project-id
  region      = "us-central1" 
}

