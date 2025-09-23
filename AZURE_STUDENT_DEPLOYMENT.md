# Azure Student Deployment Guide - Django Doctor Appointment System

This guide will help you deploy the Django Doctor Appointment System to Azure using your student free credits with CI/CD pipeline.

## Prerequisites

- Azure Student Account with free credits
- GitHub account
- Azure CLI installed locally (optional)

## Step 1: Create Azure Resources

### 1.1 Login to Azure Portal
1. Go to [Azure Portal](https://portal.azure.com)
2. Sign in with your student account

### 1.2 Create Resource Group
```bash
# Using Azure CLI (if installed)
az group create --name doctor-app-rg --location "East US"
```

Or via Azure Portal:
1. Search for "Resource groups"
2. Click "Create"
3. Name: `doctor-app-rg`
4. Region: `East US` (or your preferred region)

### 1.3 Create Azure Container Registry (ACR)
```bash
# Using Azure CLI
az acr create --resource-group doctor-app-rg --name doctorappregistry --sku Basic
```

Or via Azure Portal:
1. Search for "Container registries"
2. Click "Create"
3. Resource group: `doctor-app-rg`
4. Registry name: `doctorappregistry`
5. Location: `East US`
6. SKU: `Basic` (free tier friendly)

### 1.4 Create Azure Database for PostgreSQL
```bash
# Using Azure CLI
az postgres flexible-server create \
  --resource-group doctor-app-rg \
  --name doctor-app-db \
  --admin-user dbadmin \
  --admin-password YourSecurePassword123! \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --public-access 0.0.0.0 \
  --storage-size 32
```

Or via Azure Portal:
1. Search for "Azure Database for PostgreSQL"
2. Select "Flexible server"
3. Resource group: `doctor-app-rg`
4. Server name: `doctor-app-db`
5. Compute + storage: `Burstable, B1ms` (cost-effective)
6. Admin username: `dbadmin`
7. Password: Create a secure password

### 1.5 Create Azure Web App
```bash
# Using Azure CLI
az webapp create \
  --resource-group doctor-app-rg \
  --plan doctor-app-plan \
  --name django-doctor-appointment \
  --deployment-container-image-name doctorappregistry.azurecr.io/doctor-appointment-app:latest
```

Or via Azure Portal:
1. Search for "App Services"
2. Click "Create"
3. Resource group: `doctor-app-rg`
4. Name: `django-doctor-appointment`
5. Publish: `Docker Container`
6. Operating System: `Linux`
7. Region: `East US`
8. Pricing plan: `Free F1` or `Basic B1`

## Step 2: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add the following secrets:

### 2.1 Azure Credentials
Create a service principal:
```bash
az ad sp create-for-rbac --name "django-doctor-app-sp" --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/doctor-app-rg \
  --sdk-auth
```

Copy the JSON output and add as secret: `AZURE_CREDENTIALS`

### 2.2 Container Registry Credentials
```bash
# Get ACR credentials
az acr credential show --name doctorappregistry
```

Add these secrets:
- `ACR_USERNAME`: Username from ACR credentials
- `ACR_PASSWORD`: Password from ACR credentials

### 2.3 Application Secrets
Add these secrets for your Django app:

- `DJANGO_SECRET_KEY`: Generate a new Django secret key
- `DATABASE_URL`: `postgresql://dbadmin:YourPassword@doctor-app-db.postgres.database.azure.com:5432/postgres`
- `STRIPE_PUBLISHABLE_KEY`: Your Stripe publishable key (optional)
- `STRIPE_SECRET_KEY`: Your Stripe secret key (optional)
- `RAZORPAY_KEY_ID`: Your Razorpay key ID (optional)
- `RAZORPAY_KEY_SECRET`: Your Razorpay secret (optional)

## Step 3: Generate Django Secret Key

Run this locally to generate a secret key:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Step 4: Configure Database Connection

### 4.1 Allow Azure Services
In your PostgreSQL server:
1. Go to "Networking"
2. Enable "Allow public access from any Azure service within Azure"
3. Add your IP address if needed for local access

### 4.2 Create Database
```bash
# Connect to your PostgreSQL server and create database
az postgres flexible-server execute \
  --name doctor-app-db \
  --admin-user dbadmin \
  --admin-password YourSecurePassword123! \
  --database-name postgres \
  --querytext "CREATE DATABASE doctor_appointment;"
```

## Step 5: Deploy

### 5.1 Push to GitHub
```bash
git add .
git commit -m "Configure Azure deployment"
git push origin main
```

### 5.2 Monitor Deployment
1. Go to your GitHub repository
2. Click on "Actions" tab
3. Watch the CI/CD pipeline run

## Step 6: Post-Deployment Configuration

### 6.1 Run Database Migrations
After successful deployment, run migrations:
```bash
# Using Azure CLI
az webapp ssh --resource-group doctor-app-rg --name django-doctor-appointment

# Inside the container
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 6.2 Configure Custom Domain (Optional)
If you have a custom domain, configure it in the Web App settings.

## Step 7: Access Your Application

Your application will be available at:
`https://django-doctor-appointment.azurewebsites.net`

## Cost Optimization Tips for Students

1. **Use Free Tiers**: 
   - App Service: Free F1 tier
   - PostgreSQL: Burstable B1ms tier
   - Container Registry: Basic tier

2. **Monitor Usage**:
   - Set up billing alerts
   - Use Azure Cost Management

3. **Auto-shutdown**: Configure auto-shutdown for development environments

## Troubleshooting

### Common Issues:

1. **Container fails to start**:
   - Check logs: `az webapp log tail --name django-doctor-appointment --resource-group doctor-app-rg`
   - Verify environment variables

2. **Database connection issues**:
   - Check firewall rules
   - Verify connection string

3. **Static files not loading**:
   - Ensure `collectstatic` runs successfully
   - Check Azure Storage configuration

### Useful Commands:

```bash
# View app logs
az webapp log tail --name django-doctor-appointment --resource-group doctor-app-rg

# Restart app
az webapp restart --name django-doctor-appointment --resource-group doctor-app-rg

# Check app status
az webapp show --name django-doctor-appointment --resource-group doctor-app-rg --query state

# Scale app (if needed)
az webapp up --sku B1 --name django-doctor-appointment --resource-group doctor-app-rg
```

## Security Considerations

1. **Environment Variables**: Never commit secrets to Git
2. **Database Security**: Use strong passwords and limit access
3. **HTTPS**: Always use HTTPS in production
4. **Regular Updates**: Keep dependencies updated

## Next Steps

1. Set up monitoring and alerts
2. Configure backup strategies
3. Implement proper logging
4. Set up staging environment
5. Configure CDN for static files (optional)

---

**Note**: This deployment uses Azure's free and low-cost tiers suitable for student accounts. Monitor your usage to stay within free credit limits.
