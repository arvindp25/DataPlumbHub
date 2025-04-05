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