data "archive_file" "init" {
  type        = "zip"
  source_file = "lambda.py"
  output_path = "lambda.zip"
}

resource "aws_lambda_function" "test_lambda" {
  filename      = "lambda.zip"
  function_name = "lambda.py"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda.lambda_handler"
  runtime = "python3.7"

}



resource "aws_s3_bucket" "bucket_anagram" {
  bucket = "anagram-fd-testing"
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.bucket_anagram.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.test_lambda.arn
    events = ["s3:ObjectCreated:*"]
    filter_suffix = "anagram.csv"
  }
}



resource "aws_lambda_permission" "allow_bucket" {
  function_name = aws_lambda_function.test_lambda.arn
  source_arn = aws_s3_bucket.bucket_anagram.arn
  statement_id = "AllowExecutionFromS3Bucket"
  action = "lambda:InvokeFunction"
  principal = "s3.amazonaws.com"
}