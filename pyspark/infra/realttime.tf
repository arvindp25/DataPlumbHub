

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
    docker build ./realtime-data-generator -t realtime-gen:{var.commit_hash} 
    docker tag realtime-gen:${var.commit_hash} ${google_artifact_registry_repository.docker_images.location}-docker.pkg.dev/${var.gcp_project_id}/${google_artifact_registry_repository.docker_images.repository_id}/realtime-gen:${var.commit_hash}
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
        value = "abc123" # for testing
      }
    }
  }

  depends_on = [null_resource.copy_image_to_artifcat_registory]
}