#!/bin/bash

# Azure Setup Script for Django Doctor Appointment System
# Run this script to create all Azure resources for your student deployment

set -e

# Configuration
RESOURCE_GROUP="doctor-app-rg"
LOCATION="eastus"
ACR_NAME="doctorappregistry"
DB_SERVER_NAME="doctor-app-db"
DB_ADMIN_USER="dbadmin"
DB_ADMIN_PASSWORD="DoctorApp2024!"
WEBAPP_NAME="django-doctor-appointment"
APP_SERVICE_PLAN="doctor-app-plan"

echo "🚀 Starting Azure resource creation for Django Doctor Appointment System..."

# Login to Azure (uncomment if not already logged in)
# az login

# Create Resource Group
echo "📦 Creating resource group: $RESOURCE_GROUP"
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Azure Container Registry
echo "🐳 Creating Azure Container Registry: $ACR_NAME"
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled true

# Get ACR credentials
echo "🔑 Getting ACR credentials..."
ACR_CREDENTIALS=$(az acr credential show --name $ACR_NAME)
echo "ACR Username: $(echo $ACR_CREDENTIALS | jq -r '.username')"
echo "ACR Password: $(echo $ACR_CREDENTIALS | jq -r '.passwords[0].value')"

# Create PostgreSQL Flexible Server
echo "🗄️ Creating PostgreSQL server: $DB_SERVER_NAME"
az postgres flexible-server create \
  --resource-group $RESOURCE_GROUP \
  --name $DB_SERVER_NAME \
  --admin-user $DB_ADMIN_USER \
  --admin-password $DB_ADMIN_PASSWORD \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --public-access 0.0.0.0 \
  --storage-size 32 \
  --location $LOCATION

# Create database
echo "📊 Creating application database..."
az postgres flexible-server db create \
  --resource-group $RESOURCE_GROUP \
  --server-name $DB_SERVER_NAME \
  --database-name doctor_appointment

# Create App Service Plan
echo "📋 Creating App Service Plan: $APP_SERVICE_PLAN"
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --sku B1 \
  --is-linux

# Create Web App
echo "🌐 Creating Web App: $WEBAPP_NAME"
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --name $WEBAPP_NAME \
  --deployment-container-image-name nginx

# Configure Web App for containers
echo "⚙️ Configuring Web App settings..."
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $WEBAPP_NAME \
  --settings \
    WEBSITES_PORT=8000 \
    DOCKER_REGISTRY_SERVER_URL=https://$ACR_NAME.azurecr.io \
    WEBSITES_ENABLE_APP_SERVICE_STORAGE=false

# Create Service Principal for GitHub Actions
echo "🔐 Creating Service Principal for GitHub Actions..."
SUBSCRIPTION_ID=$(az account show --query id --output tsv)
SP_JSON=$(az ad sp create-for-rbac \
  --name "django-doctor-app-sp" \
  --role contributor \
  --scopes /subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP \
  --sdk-auth)

echo "✅ Azure resources created successfully!"
echo ""
echo "📋 IMPORTANT: Add these secrets to your GitHub repository:"
echo "=================================================="
echo ""
echo "🔑 GitHub Secrets to add:"
echo "AZURE_CREDENTIALS:"
echo "$SP_JSON"
echo ""
echo "ACR_USERNAME: $(echo $ACR_CREDENTIALS | jq -r '.username')"
echo "ACR_PASSWORD: $(echo $ACR_CREDENTIALS | jq -r '.passwords[0].value')"
echo ""
echo "DATABASE_URL: postgresql://$DB_ADMIN_USER:$DB_ADMIN_PASSWORD@$DB_SERVER_NAME.postgres.database.azure.com:5432/doctor_appointment"
echo ""
echo "DJANGO_SECRET_KEY: [Generate a new Django secret key]"
echo ""
echo "🌐 Your application will be available at:"
echo "https://$WEBAPP_NAME.azurewebsites.net"
echo ""
echo "📚 Next steps:"
echo "1. Add the above secrets to your GitHub repository"
echo "2. Generate a Django secret key and add it as DJANGO_SECRET_KEY"
echo "3. Push your code to trigger the CI/CD pipeline"
echo "4. Monitor the deployment in GitHub Actions"
echo ""
echo "💡 To generate a Django secret key, run:"
echo "python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'"
