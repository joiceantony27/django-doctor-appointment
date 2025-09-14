# Azure Deployment Guide for Django Doctor Appointment System

This guide will help you deploy your Django Doctor Appointment System to Azure using the GitHub Actions CI/CD pipeline.

## Prerequisites

### 1. Azure Account
- Active Azure subscription
- Azure CLI installed locally
- Appropriate permissions to create resources

### 2. GitHub Repository
- Repository with your Django project
- GitHub Actions enabled
- Admin access to repository settings

## Step 1: Create Azure Resources

### 1.1 Create Resource Group
```bash
az group create --name myResourceGroup --location eastus
```

### 1.2 Create Azure Container Registry
```bash
az acr create \
  --resource-group myResourceGroup \
  --name myregistry \
  --sku Basic \
  --admin-enabled true
```

### 1.3 Create Azure Web App
```bash
az webapp create \
  --resource-group myResourceGroup \
  --plan myAppServicePlan \
  --name mydoctorapp \
  --deployment-local-git
```

### 1.4 Configure Web App for Containers
```bash
az webapp config container set \
  --name mydoctorapp \
  --resource-group myResourceGroup \
  --docker-custom-image-name myregistry.azurecr.io/doctorapp:latest
```

## Step 2: Create Service Principal

### 2.1 Create Service Principal
```bash
az ad sp create-for-rbac \
  --name "github-actions-sp" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/myResourceGroup \
  --sdk-auth
```

### 2.2 Get ACR Credentials
```bash
az acr credential show --name myregistry
```

## Step 3: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

### Required Secrets:

#### AZURE_CREDENTIALS
```json
{
  "clientId": "your-client-id",
  "clientSecret": "your-client-secret",
  "subscriptionId": "your-subscription-id",
  "tenantId": "your-tenant-id",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

#### ACR_USERNAME
```
myregistry
```

#### ACR_PASSWORD
```
your-acr-password
```

## Step 4: Configure Environment Variables

Update the environment variables in `.github/workflows/ci-cd.yml`:

```yaml
env:
  ACR_NAME: myregistry
  AZURE_WEBAPP_NAME: mydoctorapp
  AZURE_RESOURCE_GROUP: myResourceGroup
  IMAGE_NAME: doctorapp
```

## Step 5: Configure Azure Web App Settings

### 5.1 Set Environment Variables
```bash
az webapp config appsettings set \
  --resource-group myResourceGroup \
  --name mydoctorapp \
  --settings \
    SECRET_KEY="your-django-secret-key" \
    DEBUG=False \
    ALLOWED_HOSTS="mydoctorapp.azurewebsites.net" \
    DB_NAME="your-db-name" \
    DB_USER="your-db-user" \
    DB_PASSWORD="your-db-password" \
    DB_HOST="your-db-host" \
    DB_PORT="5432" \
    EMAIL_HOST_USER="your-email" \
    EMAIL_HOST_PASSWORD="your-email-password" \
    STRIPE_PUBLISHABLE_KEY="your-stripe-key" \
    STRIPE_SECRET_KEY="your-stripe-secret" \
    RAZORPAY_KEY_ID="your-razorpay-key" \
    RAZORPAY_KEY_SECRET="your-razorpay-secret"
```

### 5.2 Configure Custom Domain (Optional)
```bash
az webapp config hostname add \
  --webapp-name mydoctorapp \
  --resource-group myResourceGroup \
  --hostname yourdomain.com
```

## Step 6: Database Setup

### 6.1 Create Azure Database for PostgreSQL
```bash
az postgres server create \
  --resource-group myResourceGroup \
  --name mydoctorapp-db \
  --location eastus \
  --admin-user dbadmin \
  --admin-password YourPassword123! \
  --sku-name GP_Gen5_2
```

### 6.2 Configure Firewall
```bash
az postgres server firewall-rule create \
  --resource-group myResourceGroup \
  --server mydoctorapp-db \
  --name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

## Step 7: SSL Certificate

### 7.1 Enable HTTPS
```bash
az webapp update \
  --resource-group myResourceGroup \
  --name mydoctorapp \
  --https-only true
```

## Step 8: Monitoring and Logging

### 8.1 Enable Application Insights
```bash
az monitor app-insights component create \
  --app mydoctorapp-insights \
  --location eastus \
  --resource-group myResourceGroup
```

### 8.2 Configure Logging
```bash
az webapp log config \
  --resource-group myResourceGroup \
  --name mydoctorapp \
  --application-logging true \
  --level information
```

## Step 9: Deploy

### 9.1 Push to Main Branch
```bash
git add .
git commit -m "Add CI/CD pipeline"
git push origin main
```

### 9.2 Monitor Deployment
- Go to GitHub Actions tab
- Watch the workflow execution
- Check Azure Web App logs

## Step 10: Post-Deployment

### 10.1 Run Initial Setup
```bash
# Connect to your Web App
az webapp ssh --resource-group myResourceGroup --name mydoctorapp

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 10.2 Test Application
- Visit: `https://mydoctorapp.azurewebsites.net`
- Test all functionality
- Check health endpoint: `https://mydoctorapp.azurewebsites.net/health/`

## Troubleshooting

### Common Issues:

1. **Authentication Failed**
   - Verify service principal permissions
   - Check AZURE_CREDENTIALS secret format

2. **ACR Push Failed**
   - Verify ACR credentials
   - Check ACR admin user is enabled

3. **Web App Deployment Failed**
   - Check Web App configuration
   - Verify container settings

4. **Database Connection Failed**
   - Check firewall rules
   - Verify connection string

5. **Static Files Not Loading**
   - Check STATIC_ROOT setting
   - Verify collectstatic ran successfully

### Useful Commands:

```bash
# Check Web App status
az webapp show --name mydoctorapp --resource-group myResourceGroup

# View Web App logs
az webapp log tail --name mydoctorapp --resource-group myResourceGroup

# Restart Web App
az webapp restart --name mydoctorapp --resource-group myResourceGroup

# Check ACR images
az acr repository list --name myregistry
```

## Security Best Practices

1. **Use Azure Key Vault** for sensitive configuration
2. **Enable Azure Security Center**
3. **Configure Network Security Groups**
4. **Use Managed Identity** when possible
5. **Regular security updates**
6. **Monitor with Azure Security Center**

## Cost Optimization

1. **Use Azure Dev/Test pricing** for development
2. **Configure auto-scaling**
3. **Monitor resource usage**
4. **Use Azure Cost Management**
5. **Right-size your resources**

## Support

- Azure Documentation: https://docs.microsoft.com/azure/
- GitHub Actions: https://docs.github.com/actions
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/
