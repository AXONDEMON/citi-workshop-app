variable "region" {
  type    = string
  default = "ap-south-1"
}

variable "project_name" {
  type    = string
  default = "citi-notes"
}

variable "suffix" {
  type        = string
  description = "Makes the S3 bucket name globally unique, e.g. your username"
}

variable "mongo_uri" {
  type      = string
  sensitive = true
  default   = ""
}