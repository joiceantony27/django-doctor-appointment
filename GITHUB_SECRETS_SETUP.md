# 🔐 GitHub Secrets Setup Guide

## Step 1: Access GitHub Repository Settings

1. Go to your repository: https://github.com/joiceantony27/django-doctor-appointment
2. Click on **Settings** tab (top right of the repository)
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret** button

## Step 2: Add Required Secrets

Add these secrets one by one by clicking "New repository secret" for each:

### Secret 1: AZURE_CREDENTIALS
**Name:** `AZURE_CREDENTIALS`
**Value:** Use the Azure credentials JSON from your previous setup

### Secret 2: ACR_USERNAME
**Name:** `ACR_USERNAME`
**Value:** Your Azure Container Registry username

### Secret 3: ACR_PASSWORD
**Name:** `ACR_PASSWORD`
**Value:** Your Azure Container Registry password

### Secret 4: DATABASE_URL
**Name:** `DATABASE_URL`
**Value:** Your PostgreSQL database connection string

### Secret 5: DJANGO_SECRET_KEY
**Name:** `DJANGO_SECRET_KEY`
**Value:** Your Django secret key for production

## Step 3: Verify All Secrets Are Added

After adding all secrets, you should see these 5 secrets in your repository:
- ✅ AZURE_CREDENTIALS
- ✅ ACR_USERNAME  
- ✅ ACR_PASSWORD
- ✅ DATABASE_URL
- ✅ DJANGO_SECRET_KEY

## Step 4: Trigger Deployment

Once all secrets are added, the deployment will automatically trigger when you push code. You can also manually trigger it by:

1. Go to **Actions** tab in your GitHub repository
2. Click on **CI/CD Pipeline for Django Doctor Appointment System**
3. Click **Run workflow** → **Run workflow**

## Expected Deployment URL

After successful deployment, your application will be available at:
**https://django-doctor-appointment.azurewebsites.net**

## Troubleshooting

If deployment fails:
1. Check the **Actions** tab for error logs
2. Verify all secrets are correctly added
3. Ensure Azure resources are still active
4. Check the CI/CD pipeline logs for specific errors

---
**Note:** Keep these credentials secure and never share them publicly!
