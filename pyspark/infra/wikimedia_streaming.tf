

## first we will deploy image to gcp artificat registory

resource "google_artifact_registry_repository" "docker_images" {
  location      = var.location
  repository_id = "wikimedia-streaming"
  description   = "to store wikimedia"
  format        = "DOCKER"
}

# using null resource to convert code to docker image in github

resource "null_resource" "copy_image_to_artifcat_registory_wiki" {
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

resource "google_cloud_run_v2_job" "wikimedia-streaming-app" {
  name     = "wikimedia-streaming-job"
  location = var.location
  deletion_protection = false
  depends_on = [null_resource.copy_image_to_artifcat_registory_wiki]

  template {
    template {
      


    containers {
      image = "${google_artifact_registry_repository.docker_images.location}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.docker_images.repository_id}/wikimedia-streaming:${var.commit_hash}"

        env {
        name = "GCP_PROJECT_ID"
        value = var.gcp_project_id
      }
        env {
        name = "PUB_SUB_TOPIC"
        value = google_pubsub_topic.wikimedia_streaming.name
      }
     
    }
       max_retries = 1
      timeout     = "3000s"
    }
    
    }
  }

  


resource "google_pubsub_topic" "wikimedia_streaming" {

  name = "wikimedia-sse-topic"


}
resource "google_pubsub_topic" "dlq_topic_wiki" {
  name = "wikimedia-sse-topic_dlq"
}

resource "google_pubsub_subscription" "wikimedia-subscription" {
  name  = "wikimedia-sse-subscription"
  topic = google_pubsub_topic.wikimedia_streaming.id


  # 20 minutes
  message_retention_duration = "10m"
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

resource "google_pubsub_subscription" "gcs_subscription" {
  name  = "wikimedia_streaming_data"
  topic = google_pubsub_topic.wikimedia_streaming.id
  cloud_storage_config {
    bucket = google_storage_bucket.wikimeida_streaming_bucket.name
  }
    dead_letter_policy {
    dead_letter_topic = google_pubsub_topic.dlq_topic_wiki.id
    max_delivery_attempts = 10
  }
  ack_deadline_seconds = 30


  # depends_on = [google_project_iam_member.viewer, google_project_iam_member.editor]
}

# resource "google_project_iam_member" "run_job_pubsub_publisher" {
#   project = var.gcp_project_id
#   role    = "roles/pubsub.publisher"
#   member  = "serviceAccount:${google_cloud_run_v2_job.wiki_stream_job.template.0.template.0.service_account}"
# }