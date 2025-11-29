#!/bin/bash
set -e

# CONFIG
BUCKET="landlor-frontend"
FRONTEND_DIR="frontend"
DIST_DIR="$FRONTEND_DIR/dist"

echo "🚀 Starting frontend deployment..."

# 1. Ensure frontend exists
if [ ! -d "$FRONTEND_DIR" ]; then
  echo "❌ ERROR: '$FRONTEND_DIR' directory not found. Run this from the repository root."
  exit 1
fi

# 2. Build React app
echo "📦 Building frontend..."
cd "$FRONTEND_DIR"
npm install
npm run build
cd ..

# 3. Remove old files in GCS bucket
echo "🧹 Cleaning bucket gs://$BUCKET ..."
gsutil -m rm -r gs://$BUCKET/** || true

# 4. Upload new build
echo "⬆️ Uploading new build..."
gsutil -m rsync -d -r "$DIST_DIR" gs://$BUCKET

# 5. Set website hosting config
echo "🌐 Configuring static website hosting..."
gsutil web set -m index.html -e index.html gs://$BUCKET

# 6. Make bucket objects public
echo "🔓 Making website public..."
gsutil iam ch allUsers:objectViewer gs://$BUCKET

# 7. Print final URL
echo ""
echo "🎉 Deployment complete!"
echo "----------------------------------"
echo "🌍 Website URL (HTTP):"
echo "  http://storage.googleapis.com/$BUCKET/"
echo ""
echo "🔒 Direct HTTPS URL to index.html:"
echo "  https://storage.googleapis.com/download/storage/v1/b/$BUCKET/o/index.html?alt=media"
echo "----------------------------------"
