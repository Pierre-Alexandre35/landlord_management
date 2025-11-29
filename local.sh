#!/bin/bash
set -e

IMAGE="fastapi-hello"
CONTAINER="my-fastapi"

# Database URL
DATABASE_URL="postgresql://neondb_owner:npg_mIAjwEu2xX8t@ep-odd-wildflower-ab7yw4ua-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

echo "🧹 Removing previous container (if exists)..."
docker rm -f $CONTAINER 2>/dev/null || true

echo "🐳 Building Docker image..."
docker build -t $IMAGE .

echo "🚀 Running container..."
docker run -p 8080:8080 \
  --name $CONTAINER \
  -e DATABASE_URL="$DATABASE_URL" \
  $IMAGE
