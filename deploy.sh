#!/bin/bash
set -e

SERVICE="fastapi-helloworld"
REGION="europe-west1"
PROJECT="landlor-management"

IMAGE="europe-west1-docker.pkg.dev/landlor-management/fastapi/fastapi-helloworld"

echo "🔧 Building image..."
docker build --platform linux/amd64 -t $IMAGE .

echo "📤 Pushing image..."
docker push $IMAGE

echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE \
  --image $IMAGE \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --set-secrets DATABASE_URL=DATABASE_URL:latest
