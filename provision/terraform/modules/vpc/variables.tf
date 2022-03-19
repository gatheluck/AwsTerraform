variable "aws_profile" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "vpc_azs" {
  description = "A list of availability zones names or ids in the region"
  type        = list(string)
}

variable "vpc_cidr" {
  description = "The CIDR block for the VPC. Default value is a valid CIDR, but not acceptable by AWS and should be overridden"
  type        = string
}

variable "vpc_name" {
  description = "Name to be used on all the resources as identifier"
  type        = string
}

variable "vpc_private_subnets" {
  description = "A list of private subnets inside the VPC"
  type        = list(string)
}

variable "vpc_public_subnets" {
  description = "A list of public subnets inside the VPC"
  type        = list(string)
}