output "bucket_name" {
  value = aws_s3_bucket.frontend.id
}

output "lambda_name" {
  value = aws_lambda_function.api.function_name
}