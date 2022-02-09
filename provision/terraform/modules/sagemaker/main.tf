resource "aws_sagemaker_notebook_instance" "notebook" {
  name          = "${var.root_name}-${var.project_name}"
  role_arn      = var.role_arn
  instance_type = var.notebook_instance_type
  volume_size   = var.notebook_volume_size
  root_access   = "Enabled"
}