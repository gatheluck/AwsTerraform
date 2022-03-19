module "vpc" {
  // https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 3.13.0"

  name            = var.vpc_name
  cidr            = var.vpc_cidr
  azs             = var.vpc_azs
  private_subnets = var.vpc_private_subnets
  public_subnets  = var.vpc_public_subnets

  // single NAT gateway
  enable_nat_gateway = true
  single_nat_gateway = true

  enable_dns_hostnames = true
}