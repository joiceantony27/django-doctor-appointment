# CI/CD Pipeline for Django Doctor Appointment System

This GitHub Actions workflow automates the build, test, and deployment of the Django Doctor Appointment System to Azure.

## Workflow Overview

The pipeline consists of 4 main jobs:

1. **build-and-deploy**: Builds Docker image and deploys to Azure Web App
2. **test**: Runs Django tests and security checks
3. **security-scan**: Scans Docker image for vulnerabilities
4. **notify**: Sends deployment status notifications

## Prerequisites

### Azure Resources
- Azure Container Registry (ACR)
- Azure Web App for Containers
- Azure Resource Group

### GitHub Secrets
Configure the following secrets in your GitHub repository:

#### Required Secrets:
- `AZURE_CREDENTIALS`: Azure service principal credentials (JSON format)
- `ACR_USERNAME`: Azure Container Registry username
- `ACR_PASSWORD`: Azure Container Registry password

#### Optional Secrets:
- `SLACK_WEBHOOK_URL`: For Slack notifications
- `TEAMS_WEBHOOK_URL`: For Microsoft Teams notifications

## Environment Variables

The workflow uses these environment variables (configurable in the workflow file):

- `ACR_NAME`: Azure Container Registry name (default: myregistry)
- `AZURE_WEBAPP_NAME`: Azure Web App name (default: mydoctorapp)
- `AZURE_RESOURCE_GROUP`: Azure Resource Group name (default: myResourceGroup)
- `IMAGE_NAME`: Docker image name (default: doctorapp)

## Workflow Triggers

- **Push to main branch**: Full CI/CD pipeline
- **Pull Request to main**: Build and test only (no deployment)

## Pipeline Steps

### 1. Build and Deploy Job
- Checkout repository
- Set up Docker Buildx
- Login to Azure Container Registry
- Extract metadata for tagging
- Build and push Docker image
- Deploy to Azure Web App
- Configure app settings
- Restart Web App

### 2. Test Job
- Set up Python environment
- Install dependencies
- Run Django tests
- Run security checks (Bandit, Safety)
- Upload test results

### 3. Security Scan Job
- Run Trivy vulnerability scanner
- Upload results to GitHub Security tab

### 4. Notify Job
- Send deployment status notifications

## Docker Images

The workflow builds two types of images:

- **Development**: `Dockerfile` (for local development)
- **Production**: `Dockerfile.production` (for Azure deployment)

## Deployment URL

After successful deployment, your application will be available at:
`https://{AZURE_WEBAPP_NAME}.azurewebsites.net`

## Monitoring

- View workflow runs in GitHub Actions tab
- Check deployment logs in Azure Portal
- Monitor application health in Azure Web App

## Troubleshooting

### Common Issues:

1. **Authentication Failed**
   - Verify `AZURE_CREDENTIALS` secret is correctly formatted
   - Check service principal permissions

2. **ACR Login Failed**
   - Verify `ACR_USERNAME` and `ACR_PASSWORD` secrets
   - Check ACR admin user is enabled

3. **Deployment Failed**
   - Check Azure Web App configuration
   - Verify resource group and app name

4. **Tests Failed**
   - Review test output in GitHub Actions
   - Check Django settings configuration

## Customization

### Adding Environment Variables
Add environment variables to the Azure Web App:

```yaml
- name: Configure App Settings
  uses: azure/CLI@v1
  with:
    inlineScript: |
      az webapp config appsettings set \
        --resource-group ${{ env.AZURE_RESOURCE_GROUP }} \
        --name ${{ env.AZURE_WEBAPP_NAME }} \
        --settings \
          SECRET_KEY=your-secret-key \
          DEBUG=False \
          DB_HOST=your-db-host
```

### Adding Notifications
Add Slack or Teams notifications:

```yaml
- name: Slack Notification
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
```

## Security Best Practices

1. Use Azure Key Vault for sensitive configuration
2. Enable Azure Security Center
3. Regular security scans with Trivy
4. Keep dependencies updated
5. Use least privilege principle for service principals

## Cost Optimization

1. Use Azure Container Registry Basic tier for development
2. Configure auto-scaling for Web App
3. Use Azure Dev/Test pricing for non-production
4. Monitor resource usage in Azure Cost Management
