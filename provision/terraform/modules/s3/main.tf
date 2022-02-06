resource "aws_s3_bucket" "file_storage" {
    bucket = "${var.root_name}-${var.project_name}"
    acl    = "private"

    server_side_encryption_configuration {
        rule {
            apply_server_side_encryption_by_default {
                sse_algorithm = "AES256"
            }
        }
    }

    force_destroy = var.s3_force_destroy
}

resource "aws_s3_bucket_public_access_block" "file_storage" {
    bucket                  = aws_s3_bucket.file_storage.id
    block_public_acls       = true
    block_public_policy     = true
    ignore_public_acls      = true
    restrict_public_buckets = true
}