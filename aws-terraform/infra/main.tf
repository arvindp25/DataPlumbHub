terraform {
  backend "s3" {
    key    = "envs/terraform.tfstate"
    region = "ap-south-1"
}

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1"
}

resource "aws_s3_bucket" "test" {
    bucket = "test4577h85"
  
}


resource "aws_instance" "ec2_instance" {
    ami = "ami-0f1dcc636b69a6438"
    instance_type = "t2.micro"

  
}