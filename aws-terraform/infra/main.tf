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

data "aws_vpc" "default_vpc" {
    default = true
  
}

resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssg"
  description = "Allow ssh"
  vpc_id = data.aws_vpc.default_vpc.id
  ingress {
    cidr_blocks = ["0.0.0.0/0"]
    from_port = 22
    to_port = 22
    protocol = "tcp"
  }
  egress {
   from_port = 0
   to_port = 0
   protocol = "-1"
   cidr_blocks = ["0.0.0.0/0"]
 }

}


resource "aws_instance" "ec2_instance" {
    ami = "ami-0f1dcc636b69a6438"
    instance_type = "t2.micro"
    security_groups = [aws_security_group.allow_ssh.id]
    tags = {
      Name = "ec2_instance"
    }
  
}