resource "google_bigquery_dataset" "data_transformed" {
  dataset_id                  = "data_transformed"
  location                    = "asia-south1"

}

resource "google_bigquery_table" "iot_sensor_data" {
  deletion_protection = false
  table_id   = "iot_sensor_data"
  dataset_id = google_bigquery_dataset.data_transformed.dataset_id

  schema = file("./iot_sensor_data_bq.json")
}

resource "google_bigquery_table" "edit_per_count" {
  deletion_protection = false
  table_id   = "wikimedia_edit_per_count"
  dataset_id = google_bigquery_dataset.data_transformed.dataset_id

}

resource "google_bigquery_table" "rolling_avg" {
  deletion_protection = false
  table_id   = "wikimedia_rolling_avg"
  dataset_id = google_bigquery_dataset.data_transformed.dataset_id

}

resource "google_bigquery_table" "editor_type" {
  deletion_protection = false
  table_id   = "wikimedia_editor_type"
  dataset_id = google_bigquery_dataset.data_transformed.dataset_id

}