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

# resource "google_bigquery_table" "edit_per_count" {
#   deletion_protection = false
#   table_id   = "wikimedia_edit_per_count"
#   dataset_id = google_bigquery_dataset.data_transformed.dataset_id
#   schema =  <<EOF
#   [{
#     "name" : "window",
#     "type" : "RECORD",
#     "fields":[
#     {
#     "name":"start",
#     "type": "TIMESTAMP"
#     },
#         {
#     "name":"end",
#     "type": "TIMESTAMP"
#     }
#     ]
#     },
#     {
#       "name" : "edit_count",
#       "type" : "INT64"
#     }
#   ]
#   EOF

# }


resource "google_bigquery_table" "edit_per_count" {
  deletion_protection = false
  table_id   = "wikimedia_edit_per_count"
  dataset_id = google_bigquery_dataset.data_transformed.dataset_id
  schema =  <<EOF
  [{
    "name" : "window",
    "type" : "STRING"
    },
    {
      "name" : "edit_count",
      "type" : "STRING"
    }
  ]
  EOF

}

resource "google_bigquery_table" "rolling_avg" {
  deletion_protection = false
  table_id   = "wikimedia_rolling_avg"
  dataset_id = google_bigquery_dataset.data_transformed.dataset_id
  schema = <<EOF
   [{
    "name" :"window",
    "type" :"RECORD",
    "fields":[
    {
    "name":"start",
    "type": "TIMESTAMP"
    },
        {
    "name":"end",
    "type": "TIMESTAMP"
    }
    ]
    },
    {
      "name" :"rolling_avg_edit_count",
      "type" :"INT64"
    }
  ]
  EOF
}

resource "google_bigquery_table" "editor_type" {
  deletion_protection = false
  table_id   = "wikimedia_editor_type"
  dataset_id = google_bigquery_dataset.data_transformed.dataset_id
    schema = <<EOF
    [{
    "name" :"type_of_editor",
    "type":"STRING"
    },
    {
      "name":"count_per_editor",
      "type": "INT64"
    }
  ] 
  EOF
}