#!/bin/bash
# 🚀 GCP Setup Script with Security Best Practices
# This script helps you set up GCP safely without exposing sensitive data

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Load environment variables
if [ -f ".env.gcp-setup" ]; then
    echo -e "${GREEN}📁 Loading environment variables...${NC}"
    source .env.gcp-setup
else
    echo -e "${RED}❌ .env.gcp-setup file not found!${NC}"
    echo "Please create .env.gcp-setup file with your configuration."
    exit 1
fi

echo -e "${BLUE}🚀 Starting GCP Setup for Filosofía App${NC}"
echo -e "${BLUE}Project ID: ${GCP_PROJECT_ID}${NC}"
echo -e "${BLUE}Region: ${GCP_REGION}${NC}"

# Step 1: Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ Google Cloud CLI not found!${NC}"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo -e "${GREEN}✅ Google Cloud CLI found${NC}"

# Step 2: Login to GCP (if not already logged in)
echo -e "${YELLOW}🔐 Checking GCP authentication...${NC}"
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
    echo -e "${YELLOW}Please login to your Google account:${NC}"
    gcloud auth login
else
    echo -e "${GREEN}✅ Already authenticated${NC}"
fi

# Step 3: Create project (if it doesn't exist)
echo -e "${YELLOW}📋 Creating/checking GCP project...${NC}"
if ! gcloud projects describe $GCP_PROJECT_ID &>/dev/null; then
    echo -e "${YELLOW}Creating new project: $GCP_PROJECT_ID${NC}"
    gcloud projects create $GCP_PROJECT_ID --name="Filosofía App Serverless"
    echo -e "${GREEN}✅ Project created successfully${NC}"
else
    echo -e "${GREEN}✅ Project already exists${NC}"
fi

# Step 4: Set default project
echo -e "${YELLOW}⚙️ Setting default project...${NC}"
gcloud config set project $GCP_PROJECT_ID

# Step 5: Get billing account (interactive)
echo -e "${YELLOW}💳 Checking billing account...${NC}"
if [ -z "$GCP_BILLING_ACCOUNT_ID" ] || [ "$GCP_BILLING_ACCOUNT_ID" = "your-billing-account-id-here" ]; then
    echo -e "${BLUE}Available billing accounts:${NC}"
    gcloud billing accounts list
    echo ""
    echo -e "${YELLOW}Please copy your billing account ID and update .env.gcp-setup${NC}"
    echo -e "${YELLOW}Then run this script again.${NC}"
    exit 0
fi

# Step 6: Link billing account
echo -e "${YELLOW}💳 Linking billing account...${NC}"
gcloud billing projects link $GCP_PROJECT_ID --billing-account=$GCP_BILLING_ACCOUNT_ID
echo -e "${GREEN}✅ Billing account linked${NC}"

# Step 7: Enable required APIs
echo -e "${YELLOW}🔧 Enabling required APIs...${NC}"
apis=(
    "cloudfunctions.googleapis.com"
    "firestore.googleapis.com" 
    "storage.googleapis.com"
    "cloudbuild.googleapis.com"
    "run.googleapis.com"
    "iam.googleapis.com"
    "cloudresourcemanager.googleapis.com"
)

for api in "${apis[@]}"; do
    echo -e "  Enabling $api..."
    gcloud services enable $api
done
echo -e "${GREEN}✅ All APIs enabled${NC}"

# Step 8: Create service account
echo -e "${YELLOW}👤 Creating service account...${NC}"
if ! gcloud iam service-accounts describe $GCP_SERVICE_ACCOUNT_EMAIL &>/dev/null; then
    gcloud iam service-accounts create $GCP_SERVICE_ACCOUNT_NAME \
        --display-name="Terraform Service Account for Filosofía App" \
        --description="Service account for managing infrastructure via Terraform and CI/CD"
    echo -e "${GREEN}✅ Service account created${NC}"
else
    echo -e "${GREEN}✅ Service account already exists${NC}"
fi

# Step 9: Grant IAM roles
echo -e "${YELLOW}🔑 Granting IAM roles...${NC}"
roles=(
    "roles/editor"
    "roles/cloudfunctions.admin"
    "roles/storage.admin"
    "roles/firestore.serviceAgent"
    "roles/iam.serviceAccountUser"
)

for role in "${roles[@]}"; do
    echo -e "  Granting $role..."
    gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
        --member="serviceAccount:$GCP_SERVICE_ACCOUNT_EMAIL" \
        --role="$role" \
        --quiet
done
echo -e "${GREEN}✅ IAM roles granted${NC}"

# Step 10: Create and download service account key
echo -e "${YELLOW}🔐 Creating service account key...${NC}"
mkdir -p $(dirname $GCP_CREDENTIALS_PATH)
gcloud iam service-accounts keys create $GCP_CREDENTIALS_PATH \
    --iam-account=$GCP_SERVICE_ACCOUNT_EMAIL

echo -e "${GREEN}✅ Service account key saved to: $GCP_CREDENTIALS_PATH${NC}"

# Step 11: Set local environment
echo -e "${YELLOW}⚙️ Setting up local environment...${NC}"
export GOOGLE_APPLICATION_CREDENTIALS=$GCP_CREDENTIALS_PATH
gcloud auth activate-service-account --key-file=$GCP_CREDENTIALS_PATH

# Step 12: Create Terraform state bucket
echo -e "${YELLOW}🪣 Creating Terraform state bucket...${NC}"
if ! gsutil ls gs://$GCP_TERRAFORM_STATE_BUCKET &>/dev/null; then
    gsutil mb -l $GCP_REGION gs://$GCP_TERRAFORM_STATE_BUCKET
    gsutil versioning set on gs://$GCP_TERRAFORM_STATE_BUCKET
    echo -e "${GREEN}✅ Terraform state bucket created${NC}"
else
    echo -e "${GREEN}✅ Terraform state bucket already exists${NC}"
fi

# Step 13: Show summary
echo ""
echo -e "${GREEN}🎉 GCP Setup Complete!${NC}"
echo ""
echo -e "${BLUE}📋 Summary:${NC}"
echo -e "  Project ID: $GCP_PROJECT_ID"
echo -e "  Region: $GCP_REGION"
echo -e "  Service Account: $GCP_SERVICE_ACCOUNT_EMAIL"
echo -e "  Credentials: $GCP_CREDENTIALS_PATH"
echo -e "  Terraform State Bucket: gs://$GCP_TERRAFORM_STATE_BUCKET"
echo ""
echo -e "${YELLOW}🔐 Security Notes:${NC}"
echo -e "  • Credentials saved locally: $GCP_CREDENTIALS_PATH"
echo -e "  • This file is git-ignored for security"
echo -e "  • For CI/CD, you'll need to add the key content to GitHub Secrets"
echo ""
echo -e "${BLUE}📝 Next Steps:${NC}"
echo -e "  1. Copy the credentials content for GitHub Secrets"
echo -e "  2. Run: terraform init in terraform-gcp/"
echo -e "  3. Run: terraform plan"
echo ""

# Step 14: Prepare GitHub Secrets content
echo -e "${YELLOW}📋 Preparing GitHub Secrets content...${NC}"
echo ""
echo -e "${BLUE}Copy this content to GitHub Secrets as 'GCP_SERVICE_ACCOUNT_KEY':${NC}"
echo -e "${GREEN}====== START COPYING FROM HERE ======${NC}"
cat $GCP_CREDENTIALS_PATH
echo ""
echo -e "${GREEN}====== END COPYING HERE ======${NC}"
echo ""
echo -e "${YELLOW}⚠️  Keep this key secure and never commit it to git!${NC}"