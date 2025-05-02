

## first we will deploy image to gcp artificat registory

resource "google_artifact_registry_repository" "docker_images" {
  location      = var.location
  repository_id = "wikimedia-streaming"
  description   = "to store wikimedia"
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
    docker build ../wikimedia_streaming -t wikimedia-streaming:${var.commit_hash} 
    docker tag wikimedia-streaming:${var.commit_hash} ${google_artifact_registry_repository.docker_images.location}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.docker_images.repository_id}/wikimedia-streaming:${var.commit_hash}
    gcloud auth configure-docker ${google_artifact_registry_repository.docker_images.location}-docker.pkg.dev 
    docker push ${google_artifact_registry_repository.docker_images.location}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.docker_images.repository_id}/wikimedia-streaming:${var.commit_hash}
    EOT
  }

}

resource "google_cloud_run_v2_service" "wikimedia-streaming-app" {
  name     = "wikimedia_streaming"
  location = var.location
  deletion_protection = false
  ingress = "INGRESS_TRAFFIC_ALL"

  template {
    scaling {
      max_instance_count = 2
    }

    containers {
      image = "${google_artifact_registry_repository.docker_images.location}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.docker_images.repository_id}/wikimedia-streaming:${var.commit_hash}"

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


resource "google_cloud_run_v2_service_iam_policy" "noauth-wikimedia" {
    name =  google_cloud_run_v2_service.wikimedia-streaming-app.name
  location = google_cloud_run_v2_service.wikimedia-streaming-app.location
  project  = google_cloud_run_v2_service.wikimedia-streaming-app.project

  policy_data = jsonencode({
    bindings = [
      {
        role    = "roles/run.invoker"
        members = ["allUsers"]
      }
    ]
  })
}


resource "google_pubsub_topic" "wikimedia_streaming" {

  name = "wikimedia-sse-topic"


}
resource "google_pubsub_topic" "dlq_topic" {
  name = "wikimedia-sse-topic_dlq"
}

resource "google_pubsub_subscription" "wikimedia-subscription" {
  name  = "wikimedia-sse-subscription"
  topic = google_pubsub_topic.wikimedia_streaming.id


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

#   enable_message_ordering    = true
}

# resource "google_pubsub_subscription" "bigquery_subscription" {
#   name  = "bigquery_subscription"
#   topic = google_pubsub_topic.iot_sensor_data.name
#     dead_letter_policy {
#     dead_letter_topic = google_pubsub_topic.dlq_topic.id
#     max_delivery_attempts = 10
#   }
#   ack_deadline_seconds = 30

#   bigquery_config {
#     table = "${google_bigquery_table.iot_sensor_data.project}.${google_bigquery_table.iot_sensor_data.dataset_id}.${google_bigquery_table.iot_sensor_data.table_id}"
#     use_topic_schema = true
#   }

#   # depends_on = [google_project_iam_member.viewer, google_project_iam_member.editor]
# }