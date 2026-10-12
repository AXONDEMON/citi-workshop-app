output "api_url" {
  value = aws_apigatewayv2_api.api.api_endpoint
}

output "cloudfront_url" {
  value = "https://${aws_cloudfront_distribution.frontend.domain_name}"
}

output "distribution_id" {
  value = aws_cloudfront_distribution.frontend.id
}