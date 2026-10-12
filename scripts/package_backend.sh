#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/build/lambda"

echo "==> Packaging backend"
rm -rf "$OUT"
mkdir -p "$OUT"

# Lambda runs Linux, so download Linux wheels even though you're on a Mac
pip install -r "$ROOT/backend/requirements.txt" \
  --target "$OUT" \
  --platform manylinux2014_x86_64 \
  --python-version 3.12 \
  --only-binary=:all: \
  --implementation cp

cp "$ROOT/backend/lambda_function.py" "$ROOT/backend/store.py" "$OUT/"
echo "==> Done: $OUT"