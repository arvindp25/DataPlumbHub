terraform {
  required_providers {
    aws = {
        source = "heashicorp/aws"
        version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1"
}

resource "aws_s3_bucket" "test" {
    bucket = "test4577785"
  
}