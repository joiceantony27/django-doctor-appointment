# 🚀 Azure Deployment Checklist for Django Doctor Appointment System

## ✅ Step 1: Azure Portal Setup (5-10 minutes)

### 1.1 Create Azure Account
- Go to [portal.azure.com](https://portal.azure.com)
- Sign up for free Azure account (if you don't have one)
- You get $200 free credit for 30 days!

### 1.2 Create Resource Group
1. In Azure Portal, click "Create a resource"
2. Search for "Resource Group"
3. Click "Create"
4. Name: `django-doctor-appointment-rg`
5. Region: Choose closest to you
6. Click "Review + Create" → "Create"

### 1.3 Create Container Registry
1. In Azure Portal, click "Create a resource"
2. Search for "Container Registry"
3. Click "Create"
4. Resource Group: `django-doctor-appointment-rg`
5. Registry Name: `djangoappointmentacr` (must be unique)
6. Location: Same as Resource Group
7. SKU: Basic
8. Click "Review + Create" → "Create"

### 1.4 Create App Service
1. In Azure Portal, click "Create a resource"
2. Search for "Web App"
3. Click "Create"
4. Resource Group: `django-doctor-appointment-rg`
5. Name: `django-doctor-appointment-app` (must be unique)
6. Runtime Stack: Python 3.12
7. Operating System: Linux
8. Region: Same as Resource Group
9. App Service Plan: Create new (Basic B1)
10. Click "Review + Create" → "Create"

## ✅ Step 2: GitHub Secrets Setup (2-3 minutes)

### 2.1 Get Azure Credentials
1. In Azure Portal, go to "Azure Active Directory"
2. Click "App registrations"
3. Click "New registration"
4. Name: `django-app-github-actions`
5. Click "Register"
6. Copy the "Application (client) ID"
7. Go to "Certificates & secrets"
8. Click "New client secret"
9. Copy the secret value
10. Go to "API permissions" → "Add a permission" → "Azure Service Management" → "user_impersonation" → "Grant admin consent"

### 2.2 Add GitHub Secrets
1. Go to your GitHub repository: https://github.com/joiceantony27/django-doctor-appointment
2. Click "Settings" tab
3. Click "Secrets and variables" → "Actions"
4. Click "New repository secret"
5. Add these secrets:

**Secret 1:**
- Name: `AZURE_CREDENTIALS`
- Value: 
```json
{
  "clientId": "YOUR_APPLICATION_ID",
  "clientSecret": "YOUR_CLIENT_SECRET",
  "subscriptionId": "YOUR_SUBSCRIPTION_ID",
  "tenantId": "YOUR_TENANT_ID"
}
```

**Secret 2:**
- Name: `AZURE_CONTAINER_REGISTRY`
- Value: `djangoappointmentacr.azurecr.io`

**Secret 3:**
- Name: `AZURE_APP_SERVICE_NAME`
- Value: `django-doctor-appointment-app`

**Secret 4:**
- Name: `AZURE_RESOURCE_GROUP`
- Value: `django-doctor-appointment-rg`

## ✅ Step 3: Deploy! (Automatic)

### 3.1 Trigger Deployment
1. Make any small change to your code (like adding a comment)
2. Commit and push:
```bash
git add .
git commit -m "Trigger deployment"
git push origin master
```

### 3.2 Monitor Deployment
1. Go to your GitHub repository
2. Click "Actions" tab
3. Watch the CI/CD pipeline run
4. It will take 5-10 minutes to complete

### 3.3 Access Your App
Once deployment is complete, your app will be available at:
`https://django-doctor-appointment-app.azurewebsites.net`

## 🔧 Troubleshooting

### If deployment fails:
1. Check GitHub Actions logs
2. Verify all secrets are correct
3. Make sure Azure resources are created
4. Check Azure App Service logs

### Common issues:
- **Registry name not unique**: Change `djangoappointmentacr` to something unique
- **App name not unique**: Change `django-doctor-appointment-app` to something unique
- **Missing permissions**: Make sure to grant admin consent for the app registration

## 📞 Need Help?
- Check the detailed guide: `AZURE_DEPLOYMENT_GUIDE.md`
- GitHub Actions logs will show exactly what went wrong
- Azure App Service logs are in the Azure Portal

## �� Success!
Once deployed, you'll have:
- ✅ Automated CI/CD pipeline
- ✅ Production-ready Django app
- ✅ Scalable Azure infrastructure
- ✅ Health monitoring
- ✅ SSL certificate (automatic)

Your Django Doctor Appointment System will be live on the internet! 🌐
