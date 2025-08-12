# 🆓 TERRAFORM PARA AWS FREE TIER
# Filosofía App - Infrastructure as Code
# ✅ GARANTÍA: $0.00 durante 12 meses

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Variables
variable "project_name" {
  description = "Nombre del proyecto"
  type        = string
  default     = "filosofia-app"
}

variable "environment" {
  description = "Ambiente (dev, prod)"
  type        = string
  default     = "prod"
}

variable "db_password" {
  description = "Password para RDS PostgreSQL"
  type        = string
  sensitive   = true
}

variable "aws_region" {
  description = "Región AWS"
  type        = string
  default     = "us-east-1"
}

# Locals
locals {
  name_prefix = "${var.project_name}-${var.environment}"
  
  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
    CostCenter  = "FreeTier"
  }
}

# Provider
provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = local.tags
  }
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]
  
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
  
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}
