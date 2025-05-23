resource "google_dataproc_cluster" "pyspark_dataproc_cluster" {
  name       = "my-dataproc-cluster"
  region     = "asia-south1"

  cluster_config {
    staging_bucket = google_storage_bucket.pyspark_staging_bucket.name
    endpoint_config {
               enable_http_port_access = "true"
        }
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



# resource "google_dataproc_job" "pyspark" {
#   region       = google_dataproc_cluster.pyspark_dataproc_cluster.region
#   depends_on = [ google_dataproc_cluster.pyspark_dataproc_cluster ]
#   force_delete = true
#   placement {
#     cluster_name = google_dataproc_cluster.pyspark_dataproc_cluster.name
#   }

#   pyspark_config {
#     main_python_file_uri = "gs://${google_storage_bucket.pyspark_files.name}/${var.commit_hash}/iot_sensor_transform.py"
#     args = ["arvind-develop.data_transformed.iot_sensor_data", "${ google_bigquery_dataset.data_transformed.dataset_id }", google_storage_bucket.pyspark_staging_bucket.name ]
#     properties = {
#       "spark.logConf" = "true"
#     }
#   }
# }


# resource "google_dataproc_job" "citibike_trips" {
#   region       = google_dataproc_cluster.pyspark_dataproc_cluster.region
#   depends_on = [ google_dataproc_cluster.pyspark_dataproc_cluster ]
#   force_delete = true
#   placement {
#     cluster_name = google_dataproc_cluster.pyspark_dataproc_cluster.name
#   }

#   pyspark_config {
#     main_python_file_uri = "gs://${google_storage_bucket.pyspark_files.name}/sql-ds/${var.commit_hash}/citibike_trips.py"
#     args = ["bigquery-public-data.new_york_citibike.citibike_trips", "${ google_bigquery_dataset.data_transformed.dataset_id }", google_storage_bucket.pyspark_staging_bucket.name ]
#     properties = {
#       "spark.logConf" = "true"
#     }
#   }
# }

# resource "google_dataproc_job" "austin_taxi" {
#   region       = google_dataproc_cluster.pyspark_dataproc_cluster.region
#   depends_on = [ google_dataproc_cluster.pyspark_dataproc_cluster ]
#   force_delete = true
#   placement {
#     cluster_name = google_dataproc_cluster.pyspark_dataproc_cluster.name
#   }

#   pyspark_config {
#     main_python_file_uri = "gs://${google_storage_bucket.pyspark_files.name}/sql-ds/${var.commit_hash}/austin_taxi.py"
#     args = ["bigquery-public-data.austin_bikeshare.bikeshare_trips,bigquery-public-data.austin_bikeshare.bikeshare_stations", "${ google_bigquery_dataset.data_transformed.dataset_id }", google_storage_bucket.pyspark_staging_bucket.name ]
#     properties = {
#       "spark.logConf" = "true"
#     }
#   }
# }

resource "google_dataproc_job" "spark_streaming" {
  region       = google_dataproc_cluster.pyspark_dataproc_cluster.region
  depends_on = [ google_dataproc_cluster.pyspark_dataproc_cluster,google_bigquery_table.rolling_avg,google_bigquery_table.edit_per_count, google_bigquery_table.editor_type ]
  force_delete = true
  placement {
    cluster_name = google_dataproc_cluster.pyspark_dataproc_cluster.name
  }

  pyspark_config {
    main_python_file_uri = "gs://${google_storage_bucket.pyspark_files.name}/wikimedia_streaming/${var.commit_hash}/spark-streaming.py"
    args = ["--streaming_bucket", "gs://${google_storage_bucket.wikimeida_streaming_bucket.name}",
            "--staging_bucket", "${google_storage_bucket.pyspark_staging_bucket.name}",
            "--table_name", jsonencode({"editing_count"="${google_bigquery_table.edit_per_count.project}.${google_bigquery_table.edit_per_count.dataset_id}.${google_bigquery_table.edit_per_count.table_id}"
            "rolling_avg" = "${google_bigquery_table.rolling_avg.project}.${google_bigquery_table.rolling_avg.dataset_id}.${google_bigquery_table.rolling_avg.table_id}"
            "editor_type" ="${google_bigquery_table.editor_type.project}.${google_bigquery_table.editor_type.dataset_id}.${google_bigquery_table.editor_type.table_id}"
            })
    ]
    properties = {
      "spark.logConf" = "true"
    }
  }
}
