resource "google_dataproc_cluster" "pyspark_dataproc_cluster" {
  name       = "my-dataproc-cluster"
  region     = "asia-south1"

  cluster_config {
    staging_bucket = google_storage_bucket.pyspark_staging_bucket.name
    master_config {
      num_instances = 1
      machine_type  = "n1-standard-2"
      disk_config {
        boot_disk_size_gb = 30  # Set smaller disk size (default is 500GB)
      }
    }

    worker_config {
      num_instances = 2
      machine_type  = "n1-standard-2"
      disk_config {
        boot_disk_size_gb = 30  # Set smaller disk size (default is 500GB)
      }
    }

    software_config {
      image_version = "2.1.84-debian11"
    }
  }
}



resource "google_dataproc_job" "pyspark" {
  region       = google_dataproc_cluster.pyspark_dataproc_cluster.region
  depends_on = [ google_dataproc_cluster.pyspark_dataproc_cluster ]
  force_delete = true
  placement {
    cluster_name = google_dataproc_cluster.pyspark_dataproc_cluster.name
  }

  pyspark_config {
    main_python_file_uri = "gs://${google_storage_bucket.pyspark_files.name}/${var.commit_hash}/iot_sensor_transform.py"
    args = ["arvind-develop.data_transformed.iot_sensor_data", "${ google_bigquery_dataset.data_transformed.dataset_id }", google_storage_bucket.pyspark_staging_bucket.name ]
    properties = {
      "spark.logConf" = "true"
    }
  }
}

