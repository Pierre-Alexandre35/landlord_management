# 🏡 landlor_management

A production-ready **FastAPI** project with:

- ⚡ FastAPI + Pydantic
- 🐘 PostgreSQL (NeonDB)
- 🔄 Liquibase for database migrations
- 🐳 Docker (local + production)
- ☁️ Google Cloud Run deployment
- 📦 Artifact Registry for container storage
- 🔐 Google Secret Manager for environment secrets

This repository provides a clean architecture for developing, running, and deploying a FastAPI backend with secure secret handling and automated container deployment.

## 📁 Project Structure

```
.
├── Dockerfile
├── LICENSE
├── app
│   ├── __init__.py
│   ├── auth
│   │   ├── hash.py
│   │   ├── jwt_service.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── service.py
│   ├── db.py
│   └── main.py
├── deploy.sh
├── liquibase.properties
├── local.sh
├── migrations
│   ├── changelog-master.xml
│   └── changesets
│       └── 001-create-users.sql
├── readme
│   └── md
└── requirements.txt
```

## 🔐 Environment Variables

This project loads secrets from **Google Secret Manager** in production, and from a local `.env` file during development.

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Fill it with your local secrets.

## `.env.example`

```env
# PostgreSQL connection string
DATABASE_URL="postgresql://USER:PASSWORD@HOST:PORT/DBNAME?sslmode=require"
```

## 🛠️ Running Locally (Docker)

Start your API locally:

```bash
docker build -t fastapi-hello .
docker run -p 8080:8080 --env-file .env fastapi-hello
```

API runs at:
```
http://localhost:8080
```

## 📚 Database Migrations (Liquibase)

Liquibase is configured using `liquibase.properties`:

```
url=jdbc:postgresql://<neon-host>/<db>?sslmode=require
username=neondb_owner
password=********
changeLogFile=migrations/changelog-master.xml
```

Run migrations:

```bash
liquibase update
```

## ☁️ Deployment (Cloud Run)

Deployment uses:

- Artifact Registry
- Secret Manager
- Cloud Run
- deploy.sh

### deploy.sh

```bash
#!/bin/bash
set -e

SERVICE="fastapi-helloworld"
REGION="europe-west1"
PROJECT="landlor_management"

IMAGE="europe-west1-docker.pkg.dev/landlor_management/fastapi/fastapi-helloworld"

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
```

## 📄 License

MIT
