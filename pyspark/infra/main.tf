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

resource "google_storage_bucket" "pyspark_files" {
 name          = "dataproc_python_file"
 location = "asia-south1"
 storage_class = "STANDARD"

#  uniform_bucket_level_access = true
}

resource "null_resource" "copy_file_code" {
  triggers = { always_run = var.commit_hash }
  provisioner "local-exec" {
    command = <<-EOT
      gcloud auth activate-service-account --key-file="gcp.json"
      gsutil -m cp -r ../cymbal_investment_dataset/* gs://${google_storage_bucket.pyspark_files.name }
    EOT
  }

}
