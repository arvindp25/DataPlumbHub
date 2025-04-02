variable "gcp_project_id" {
type = string
}

variable "tfstate_bucket" {
type = string
}

variable "commit_hash" {
    type = string
  
}

variable "location" {
    default = "asia-south1"
    type = string
  
}