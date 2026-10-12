#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Usage: ./scripts/deploy.sh <unique-suffix> [api-url]
SUFFIX="${1:?Usage: deploy.sh <unique-suffix> [api-url]}"
API_URL="${2:-}"

echo "==> 1/4 Package backend"
"$ROOT/scripts/package_backend.sh"

echo "==> 2/4 Terraform apply"
cd "$ROOT/infra"
terraform init -input=false
terraform apply -auto-approve -var="suffix=$SUFFIX"
BUCKET="$(terraform output -raw bucket_name)"

echo "==> 3/4 Build frontend"
cd "$ROOT/frontend"
npm ci
VITE_API_URL="$API_URL" npm run build

echo "==> 4/4 Upload to S3: $BUCKET"
aws s3 sync dist/ "s3://$BUCKET" --delete

echo "==> Deploy complete"