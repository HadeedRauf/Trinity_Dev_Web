# CI/CD Pipeline Setup Guide - Trinity Store on AWS EC2

## 📋 Overview

This guide will help you set up a complete CI/CD pipeline that:
- Automatically builds Docker images on every push to `main` branch
- Deploys to your AWS EC2 instance
- Runs database migrations
- Sends notifications on success/failure

## 🔧 Information You Have

- **EC2 Instance IP**: `13.53.101.211`
- **EC2 Hostname**: `ec2-13-53-101-211.eu-north-1.compute.amazonaws.com`
- **EC2 User**: `ec2-user`
- **EC2 Region**: `eu-north-1`
- **PEM File**: `/home/hadeed/Downloads/trinity_dev.pem`
- **GitHub Repo**: `https://github.com/HadeedRauf/Trinity_Dev_Web`

## 🚀 Step 1: Set Up EC2 Instance

### Option A: Manual Setup (Recommended for first time)

SSH into your EC2 instance:
```bash
ssh -i /home/hadeed/Downloads/trinity_dev.pem ec2-user@13.53.101.211
```

Then run the setup script:
```bash
# Install required tools
sudo yum update -y
sudo yum install -y docker git
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone and setup project
mkdir -p /home/ec2-user/Trinity_Dev_Web
cd /home/ec2-user/Trinity_Dev_Web
git clone https://github.com/HadeedRauf/Trinity_Dev_Web.git .

# Start the application
docker-compose up -d
```

Or run the automated script:
```bash
bash /home/hadeed/Trinity_Dev_Web/scripts/setup-ec2.sh
```

## 🔑 Step 2: Configure GitHub Secrets

You need to add the following secrets to your GitHub repository:

### How to Add Secrets:

1. Go to: `https://github.com/HadeedRauf/Trinity_Dev_Web/settings/secrets/actions`
2. Click "New repository secret"
3. Add each secret below:

### Required Secrets:

#### 1. `EC2_PRIVATE_KEY` (Your PEM file content)
```
- Click "New repository secret"
- Name: EC2_PRIVATE_KEY
- Value: [Copy the entire content of trinity_dev.pem]
```

To get the PEM file content:
```bash
cat /home/hadeed/Downloads/trinity_dev.pem
```

Then copy the entire content including `-----BEGIN RSA PRIVATE KEY-----` and `-----END RSA PRIVATE KEY-----`

#### 2. `EC2_HOST` 
```
- Name: EC2_HOST
- Value: 13.53.101.211
```

#### 3. `EC2_USER`
```
- Name: EC2_USER
- Value: ec2-user
```

### Optional Secrets (for notifications):

#### 4. `SLACK_WEBHOOK` (Optional - for Slack notifications)
```
- Name: SLACK_WEBHOOK
- Value: [Your Slack webhook URL]
```

To create a Slack webhook:
1. Go to your Slack workspace settings
2. Create an Incoming Webhook
3. Copy the webhook URL and add it as a secret

## 📝 Step 3: Deploy Your Code

Once secrets are configured, the CI/CD pipeline will:

### Automatic Deployment (on git push):
```bash
cd /home/hadeed/Trinity_Dev_Web
git add .
git commit -m "Deploy to EC2"
git push origin main
```

The workflow will:
1. Build Docker images
2. Push to GitHub Container Registry
3. SSH into EC2
4. Pull latest code
5. Stop old containers
6. Start new containers
7. Run migrations
8. Send notification

### Manual Deployment (if needed):
You can also SSH and deploy manually:
```bash
ssh -i /home/hadeed/Downloads/trinity_dev.pem ec2-user@13.53.101.211 << 'EOF'
cd /home/ec2-user/Trinity_Dev_Web
git pull origin main
docker-compose down
docker-compose up -d
docker-compose exec -T backend python manage.py migrate
EOF
```

## 🌍 Access Your Application

Once deployed, access it at:
- **Frontend**: http://13.53.101.211:3000
- **Backend API**: http://13.53.101.211:8000/api/
- **Django Admin**: http://13.53.101.211:8000/admin/

### Test Accounts:
- **Admin**: username: `admin` / password: `admin`
- **Customer**: username: `customer` / password: `customer123`

## 📊 Monitor Deployment

### View GitHub Actions:
- Go to: `https://github.com/HadeedRauf/Trinity_Dev_Web/actions`
- Watch the build and deployment progress

### View EC2 Logs:
```bash
ssh -i /home/hadeed/Downloads/trinity_dev.pem ec2-user@13.53.101.211
cd /home/ec2-user/Trinity_Dev_Web
docker-compose logs -f
```

### Check Container Status:
```bash
ssh -i /home/hadeed/Downloads/trinity_dev.pem ec2-user@13.53.101.211
docker-compose ps
```

## 🛠️ Troubleshooting

### If deployment fails:

1. **Check GitHub Actions logs**:
   - Go to Actions tab → Latest workflow run → See error details

2. **SSH into EC2 and check logs**:
```bash
ssh -i /home/hadeed/Downloads/trinity_dev.pem ec2-user@13.53.101.211
cd /home/ec2-user/Trinity_Dev_Web
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

3. **Restart containers**:
```bash
ssh -i /home/hadeed/Downloads/trinity_dev.pem ec2-user@13.53.101.211
docker-compose restart
```

4. **Pull latest code manually**:
```bash
ssh -i /home/hadeed/Downloads/trinity_dev.pem ec2-user@13.53.101.211
cd /home/ec2-user/Trinity_Dev_Web
git pull origin main
docker-compose down
docker-compose up -d
```

## 🔒 Security Recommendations

1. **Change database passwords** in production
2. **Use HTTPS/SSL** - Set up with Let's Encrypt
3. **Keep PEM file secure** - Never commit it to git
4. **Use AWS Security Groups** to restrict port access
5. **Enable backups** for your EC2 instance
6. **Monitor logs regularly** for security issues

## 📈 Next Steps

1. Set up GitHub Secrets (see Step 2 above)
2. SSH into EC2 and run setup script
3. Push a small change to test the pipeline:
```bash
git add .
git commit -m "Test CI/CD pipeline"
git push origin main
```

4. Monitor the deployment in GitHub Actions
5. Access your application and test it

## 📞 Support

If you encounter any issues:
1. Check GitHub Actions workflow logs
2. SSH into EC2 and review Docker logs
3. Verify all secrets are correctly configured
4. Ensure EC2 security groups allow ports 3000 and 8000

---

**Workflow Files Location**: `.github/workflows/deploy.yml`
**Setup Script Location**: `scripts/setup-ec2.sh`

Happy deploying! 🚀
