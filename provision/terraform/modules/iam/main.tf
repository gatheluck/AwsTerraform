data "aws_iam_policy_document" "assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = [var.identifier]
    }
  }
}

resource "aws_iam_role" "sagemaker_user" {
  name               = "role_sagemaker_user"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

data "aws_iam_policy_document" "sagemaker_user" {
  statement {
    effect = "Allow"
    actions = [
      "s3:GetBucketLocation",
      "s3:ListBucket",
      "s3:ListAllMyBuckets",
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
      "s3:GetBucketCors",
      "s3:PutBucketCors"
    ]
    resources = [
      "arn:aws:s3:::*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "sagemaker:CreateTrainingJob",
      "sagemaker:DescribeTrainingJob"
    ]
    resources = [
      "arn:aws:sagemaker:${var.aws_region}:${data.aws_caller_identity.current.account_id}:*"
    ]
  }
}

resource "aws_iam_policy" "sagemaker_user" {
  name        = "policy_sagemaker_user"
  path        = "/"
  description = "Policy for the SageMaker Notebook Instance to manage training jobs, models and endpoints"
  policy      = data.aws_iam_policy_document.sagemaker_user.json
}

resource "aws_iam_role_policy_attachment" "sagemaker_user" {
  role       = aws_iam_role.sagemaker_user.name
  policy_arn = aws_iam_policy.sagemaker_user.arn
}