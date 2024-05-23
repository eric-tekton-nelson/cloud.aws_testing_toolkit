include "region" {
  path = find_in_parent_folders()
  merge_strategy = "deep"
}

include "common" {
  path = find_in_parent_folders("common/common.hcl")
  merge_strategy = "deep"
}

include "provider" {
  path = find_in_parent_folders("common/provider.hcl")
  merge_strategy = "deep"
}

inputs = {
   name = "dev-main-ue2"
   base_cidr = "10.3.0.0/16"
}

terraform {
  source = "../../../../modules/vpc"
}