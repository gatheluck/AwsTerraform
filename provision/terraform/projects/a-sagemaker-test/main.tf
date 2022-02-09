locals {
  project_name = "a-sagemaker-test"
}

module "file_storage" {
  source = "../../modules/s3"

  # vavriables
  project_name     = local.project_name
  root_name        = var.root_name
  s3_force_destroy = true
}

module "iam" {
  source = "../../modules/iam"

  # variables
  aws_region = var.aws_region
  identifier = "sagemaker.amazonaws.com"
}

module "notebook" {
  source = "../../modules/sagemaker"

  # vavriables
  notebook_instance_type = "ml.t2.medium"
  notebook_volume_size   = 25
  project_name           = local.project_name
  role_arn               = module.iam.iam_role_arn
  root_name              = var.root_name
}