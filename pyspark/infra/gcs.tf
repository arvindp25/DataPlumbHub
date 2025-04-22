resource "google_storage_bucket" "pyspark_files" {
 name          = "dataproc_python_file"
 location = "asia-south1"
 storage_class = "STANDARD"
 force_destroy = true

#  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "pyspark_staging_bucket" {
 name          = "pyspark_staging_bucket"
 location = "asia-south1"
 storage_class = "STANDARD"
 force_destroy = true

#  uniform_bucket_level_access = true
}

resource "google_storage_bucket_object" "copy_files_to_gcs" {
  for_each = fileset("../cymbal_investment_dataset", "*")  # Change path and pattern as needed
  
  bucket =google_storage_bucket.pyspark_files.name
  name   = "${var.commit_hash}/${each.value}"  # Destination path in the bucket
  source = "../cymbal_investment_dataset/${each.value}"  # Local file path
}

resource "google_storage_bucket_object" "copy_sql_ds_file_to_gcs" {
  for_each = fileset("../sql-ds", "*")  # Change path and pattern as needed
  
  bucket =google_storage_bucket.pyspark_files.name
  name   = "sql-ds/${var.commit_hash}/${each.value}"  # Destination path in the bucket
  source = "../sql-ds/${each.value}"  # Local file path
}