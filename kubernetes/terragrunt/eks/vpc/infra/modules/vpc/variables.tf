variable "region" {
    type = string
    description = "VPC region"
}
variable "name" {
    type = string
    description = "VPC name"
}
variable "base_cidr" {
    type = string
    description = "base CIDR for VPC"
}
variable "environment" {
    type = string
    description = "environment name"
}