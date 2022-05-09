
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }
}

provider "aws" {
  region = "${var.aws_region}"
}

provider "archive" {}

resource "null_resource" "pip" {
  triggers = {
    main         = "${base64sha256(file("src/main.py"))}"
    requirements = "${base64sha256(file("src/requirements.txt"))}"
  }

  provisioner "local-exec" {
    command = "./src/pip.sh"
    interpreter = ["/bin/sh"]
  }
}


data "archive_file" "zip" {
  type        = "zip"
  output_file_mode = "0666"
  source_dir = "./src"
  output_path = "process_files.zip"
  depends_on = [
    null_resource.pip
  ]
}
resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow"
    },
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "cloudwatch.amazonaws.com"
      },
      "Effect": "Allow"
    },
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "s3.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.process-csv.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.csv-files-bucket.arn
}

resource "aws_lambda_function" "process-csv" {
  filename         = "${data.archive_file.zip.output_path}"
  source_code_hash = "${data.archive_file.zip.output_base64sha256}"

  function_name = "process-csv"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "main.lambda_handler"
  runtime       = "python3.6"
}

resource "aws_s3_bucket" "csv-files-bucket" {
  bucket = "csv-files-bucket-stori"
}


resource "aws_s3_bucket_policy" "allow_public_access" {
  bucket = aws_s3_bucket.csv-files-bucket.id
  policy = data.aws_iam_policy_document.allow_public_access.json
}

data "aws_iam_policy_document" "allow_public_access" {
  statement {
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }

    actions = [
      "s3:GetObject",
      "s3:ListBucket",
    ]

    resources = [
      aws_s3_bucket.csv-files-bucket.arn,
      "${aws_s3_bucket.csv-files-bucket.arn}/*",
    ]
  }
}

resource "aws_s3_bucket_notification" "bucket_notification_csv" {
  bucket = aws_s3_bucket.csv-files-bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.process-csv.arn
    events              = ["s3:ObjectCreated:*"]
    filter_suffix = ".csv"
  }

  depends_on = [aws_lambda_permission.allow_bucket]
}