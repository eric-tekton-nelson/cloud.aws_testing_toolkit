locals {
  region = read_terragrunt_config(find_in_parent_folders("terragrunt.hcl")).inputs.region
  environment = read_terragrunt_config(find_in_parent_folders("common/common.hcl")).inputs.environment
}

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite"
  contents  = <<-EOF
  provider "aws" {
    region = "${local.region}"
    default_tags {
      tags = {
        Environment = "${local.environment}"
        "bwell/owner" = "EricNelson"
        "bwell/terraform" = "true"
        "bwell/terraform-module" = "terragrunt"
      }
    }
  }
  EOF
}

generate "backend" {
  path = "backend.tf"
  if_exists = "overwrite"
  contents = <<-EOF
  terraform {
        backend "s3" {
        bucket         = "<tfstate_bucket_name>"
        key            = "<name>/<region>/terraform.tfstate"
        region         = "<region>"
        encrypt        = true
        dynamodb_table = "<table_name>"
        kms_key_id     = "<kms_key_arn>"
        # skip_credentials_validation = true
        # skip_metadata_api_check     = true
    }
  }
  EOF
}
