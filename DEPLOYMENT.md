# 🚀 Deployment Guide - GCP Serverless

## Stack Overview

- **Frontend**: Vercel (Next.js)
- **Backend**: Google Cloud Functions
- **Database**: Firestore (europe-southwest1)
- **Infrastructure**: Terraform
- **CI/CD**: GitHub Actions

## Prerequisites

### 1. GCP Setup
1. Create GCP project: `filosofia-app-serverless`
2. Enable billing account
3. Install Google Cloud CLI: `gcloud init`
4. Login: `gcloud auth login`

### 2. Service Account Setup
```bash
# Create service account for Terraform/CI
gcloud iam service-accounts create terraform-sa \
  --display-name="Terraform Service Account"

# Grant necessary permissions
gcloud projects add-iam-policy-binding filosofia-app-serverless \
  --member="serviceAccount:terraform-sa@filosofia-app-serverless.iam.gserviceaccount.com" \
  --role="roles/editor"

gcloud projects add-iam-policy-binding filosofia-app-serverless \
  --member="serviceAccount:terraform-sa@filosofia-app-serverless.iam.gserviceaccount.com" \
  --role="roles/cloudfunctions.admin"

# Create and download key
gcloud iam service-accounts keys create key.json \
  --iam-account=terraform-sa@filosofia-app-serverless.iam.gserviceaccount.com
```

### 3. GitHub Secrets Setup
Add to GitHub repository secrets:
- `GCP_SERVICE_ACCOUNT_KEY`: Contents of `key.json`

## Local Development

### 1. Backend Setup
```bash
cd backend/

# Install dependencies
pip install -r requirements-gcp.txt

# Set up local Firestore emulator (optional)
firebase emulators:start --only firestore

# Run with functions-framework
functions-framework --target=app --source=app/main_gcp.py --debug
```

### 2. Frontend Setup
```bash
cd frontend/

# Install dependencies
npm install

# Update API URL in .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8080" > .env.local

# Run development server
npm run dev
```

## Production Deployment

### 1. Infrastructure Deployment
```bash
cd terraform-gcp/

# Initialize Terraform
terraform init

# Plan deployment
terraform plan -var="project_id=filosofia-app-serverless"

# Deploy infrastructure
terraform apply -var="project_id=filosofia-app-serverless"
```

### 2. Data Migration (One-time)
```bash
cd backend/

# Export from existing PostgreSQL
export DATABASE_URL="postgresql://user:password@host:port/database"

# Set up GCP credentials
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"

# Run migration
python migrate_to_firestore.py
```

### 3. Backend Deployment
```bash
cd backend/

# Deploy function manually (or use GitHub Actions)
gcloud functions deploy filosofia-api \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated \
  --region europe-southwest1 \
  --source . \
  --entry-point app \
  --requirements-file requirements-gcp.txt \
  --memory 512MB \
  --timeout 60s \
  --env-vars-file .env.gcp
```

### 4. Frontend Deployment
1. Connect Vercel to GitHub repository
2. Set build command: `npm run build`
3. Set environment variable:
   - `NEXT_PUBLIC_API_URL`: Your Cloud Function URL

## CI/CD Pipeline

### Automatic Deployment
1. Push to `main` branch triggers deployment
2. GitHub Actions workflow:
   - Tests backend code
   - Deploys infrastructure with Terraform
   - Deploys Cloud Function
   - Tests deployment

### Manual Deployment
```bash
# Trigger manual deployment
gh workflow run deploy-gcp.yml
```

## Monitoring & Logs

### Cloud Function Logs
```bash
# View logs
gcloud functions logs read filosofia-api --region europe-southwest1

# Follow logs in real-time
gcloud functions logs tail filosofia-api --region europe-southwest1
```

### Firestore Monitoring
- GCP Console → Firestore → Usage tab
- Monitor read/write operations
- Set up billing alerts

## Cost Management

### Always Free Resources
- **Cloud Functions**: 2M invocations/month
- **Firestore**: 1GB storage + 50K reads/day + 20K writes/day
- **Cloud Storage**: 5GB storage

### Expected Costs (Spain/EU)
- **Monthly**: €0-3/month
- **Per 1M requests**: ~€0.40
- **Firestore overage**: €0.18/100K operations

### Cost Optimization
```bash
# Set budget alerts
gcloud billing budgets create \
  --billing-account=BILLING_ACCOUNT_ID \
  --display-name="Filosofia App Budget" \
  --budget-amount=5EUR \
  --threshold-rule=percent=0.8,basis=CURRENT_SPEND
```

## Security

### API Security
- CORS configured for Vercel domains only
- No API keys required (public API)
- Rate limiting via Cloud Functions quotas

### Firestore Security Rules
```javascript
// Firestore rules (read-only for public)
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow read access to all collections
    match /{document=**} {
      allow read: if true;
      allow write: if false; // Only backend can write
    }
  }
}
```

## Troubleshooting

### Common Issues

1. **Cold Start Latency**
   - Solution: Use Cloud Run if consistently slow
   - Monitor via GCP Console

2. **CORS Errors**
   - Check `CORS_ORIGINS` in `.env.gcp`
   - Verify Vercel domain is included

3. **Firestore Permissions**
   - Verify service account has Firestore permissions
   - Check security rules

### Health Check
```bash
# Test API endpoint
curl https://your-function-url.cloudfunctions.net/health

# Expected response
{"status":"ok","platform":"gcp-cloud-functions","database":"firestore"}
```

## Rollback Plan

### Emergency Rollback
```bash
# Revert to previous function version
gcloud functions deploy filosofia-api \
  --source gs://gcf-sources-bucket/previous-version.zip
  
# Or disable traffic
gcloud functions deploy filosofia-api --no-allow-unauthenticated
```

---

## 📞 Support

- **Documentation**: This file
- **Logs**: `gcloud functions logs read filosofia-api`
- **Monitoring**: GCP Console → Cloud Functions