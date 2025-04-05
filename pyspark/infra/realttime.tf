

## first we will deploy image to gcp artificat registory

resource "google_artifact_registry_repository" "docker_images" {
  location      = var.location
  repository_id = "realtime-websocket-repo"
  description   = "example docker repository"
  format        = "DOCKER"
}

# using null resource to convert code to docker image in github

resource "null_resource" "copy_image_to_artifcat_registory" {
  triggers = {
    always = var.commit_hash
  }
  
  provisioner "local-exec" {
    command = <<EOT
    gcloud auth activate-service-account --key-file="gcp.json"
    docker build ../realtime-data-generator -t realtime-gen:${var.commit_hash} 
    docker tag realtime-gen:${var.commit_hash} ${google_artifact_registry_repository.docker_images.location}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.docker_images.repository_id}/realtime-gen:${var.commit_hash}
    gcloud auth configure-docker ${google_artifact_registry_repository.docker_images.location}-docker.pkg.dev 
    docker push ${google_artifact_registry_repository.docker_images.location}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.docker_images.repository_id}/realtime-gen:${var.commit_hash}
    EOT
  }

}

resource "google_cloud_run_v2_service" "mock-data-generator" {
  name     = "mock-data-generator"
  location = var.location
  deletion_protection = false
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    scaling {
      max_instance_count = 2
    }

    containers {
      image = "${google_artifact_registry_repository.docker_images.location}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.docker_images.repository_id}/realtime-gen:${var.commit_hash}"

      env {
        name = "API_KEY"
        value = var.API_KEY
      }
        env {
        name = "GCP_PROJECT_ID"
        value = var.gcp_project_id
      }
        env {
        name = "PUB_SUB_TOPIC"
        value = google_pubsub_topic.iot_sensor_data.name
      }

    }
  }

  depends_on = [null_resource.copy_image_to_artifcat_registory]
}


resource "google_cloud_run_v2_service_iam_policy" "noauth" {
    name =  google_cloud_run_v2_service.mock-data-generator.name
  location = google_cloud_run_v2_service.mock-data-generator.location
  project  = google_cloud_run_v2_service.mock-data-generator.project

  policy_data = jsonencode({
    bindings = [
      {
        role    = "roles/run.invoker"
        members = ["allUsers"]
      }
    ]
  })
}



# resource "google_pubsub_schema" "iot_sensor_data_schema" {
#   name = "iot_sensor_data_schema"
#   type = "AVRO"
#   definition = file("./iot_sensor_data_ps.avsc")

# }

resource "google_pubsub_topic" "iot_sensor_data" {

  name = "iot-sensor-topic"
  # schema_settings {
  #   schema     = google_pubsub_schema.iot_sensor_data_schema.id
  #   encoding   = "AVRO"
  # }

}

resource "google_pubsub_subscription" "iot-sensor-subscription" {
  name  = "iot-sensor-subscription"
  topic = google_pubsub_topic.iot_sensor_data.id


  # 20 minutes
  message_retention_duration = "1200s"
  retain_acked_messages      = false

  ack_deadline_seconds = 20

  expiration_policy {
    ttl = "300000.5s"
  }
  retry_policy {
    minimum_backoff = "10s"
  }

  enable_message_ordering    = true
}

resource "google_pubsub_subscription" "bigquery_subscription" {
  name  = "bigquery_subscription"
  topic = google_pubsub_topic.iot_sensor_data.name

  bigquery_config {
    table = "${google_bigquery_table.iot_sensor_data.project}.${google_bigquery_table.iot_sensor_data.dataset_id}.${google_bigquery_table.iot_sensor_data.table_id}"
  }

  # depends_on = [google_project_iam_member.viewer, google_project_iam_member.editor]
}

# these permission is provided with consloe
# resource "google_project_iam_member" "editor" {
#   project = var.gcp_project_id
#   role   = "roles/bigquery.dataEditor"
#   member = "serviceAccount:service-${data.google_project.project.number}@gcp-sa-pubsub.iam.gserviceaccount.com"
# }

# resource "google_project_iam_member" "viewer" {
#   project = data.google_project.project.project_id
#   role   = "roles/bigquery.metadataViewer"
#   member = "serviceAccount:service-${data.google_project.project.number}@gcp-sa-pubsub.iam.gserviceaccount.com"
# }