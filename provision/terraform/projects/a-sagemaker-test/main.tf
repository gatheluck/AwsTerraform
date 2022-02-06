locals {
  project_name = "a-sagemaker-test"
}

module "a_sagemaker_test_s3" {
  source = "../../modules/s3"

  root_name        = var.root_name
  project_name     = local.project_name
  s3_force_destroy = true
}