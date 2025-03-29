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

resource "google_service_account" "dataproc_service_account" {
  account_id   = "dataprocserverless"
  display_name = "Service Account"
}

resource "google_service_account_iam_member" "dataproc-service-account-iam" {
  service_account_id = google_service_account.dataproc_service_account.id
  role               = "roles/dataproc.editorroles/dataproc.editor"
  member             = "serviceAccount:${google_service_account.dataproc_service_account.email}"
}

resource "google_bigquery_dataset" "data_transformed" {
  dataset_id                  = "data_transformed"
  location                    = "asia-south1"

}



resource "google_dataproc_batch" "example_batch_pyspark" {
  depends_on = [ google_bigquery_dataset.data_transformed, google_service_account.dataproc_service_account ]
    batch_id      = "tf-test-batch"
    location      = "asia-south1"
    runtime_config {
      properties    = { "spark.dynamicAllocation.enabled": "false", "spark.executor.instances": "2" }
    }

    environment_config {
      execution_config {
        subnetwork_uri = "default"
        service_account = google_service_account.dataproc_service_account.email
      }
    }

    pyspark_batch {
      main_python_file_uri = "gs://dataproc_python_file/main.py"
      args                 = ["bigquery-public-data.cymbal_investments.trade_capture_report", "${ google_bigquery_dataset.data_transformed.dataset_id }"]
      # jar_file_uris        = ["file:///usr/lib/spark/examples/jars/spark-examples.jar"]
      # python_file_uris     = ["gs://dataproc-examples/pyspark/hello-world/hello-world.py"]
      # # archive_uris         = [
      #   "https://storage.googleapis.com/terraform-batches/animals.txt.tar.gz#unpacked",
      #   "https://storage.googleapis.com/terraform-batches/animals.txt.jar",
      #   "https://storage.googleapis.com/terraform-batches/animals.txt"
      # ]
      # file_uris            = ["https://storage.googleapis.com/terraform-batches/people.txt"]
    }
}