#!/bin/bash

# Trinity Store - EC2 Server Setup Script
# This script sets up all dependencies and the project on your EC2 instance

set -e

echo "🚀 Trinity Store - AWS EC2 Server Setup"
echo "========================================"

# Update system packages
echo "📦 Updating system packages..."
sudo yum update -y

# Install Docker
echo "🐳 Installing Docker..."
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user

# Install Docker Compose
echo "🐳 Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose

# Install Git
echo "📝 Installing Git..."
sudo yum install -y git

# Install Docker credentials helper
echo "🔐 Installing Docker credentials helper..."
sudo yum install -y pass

# Create project directory
echo "📁 Creating project directory..."
mkdir -p /home/ec2-user/Trinity_Dev_Web
cd /home/ec2-user/Trinity_Dev_Web

# Clone repository
echo "📥 Cloning repository..."
git clone https://github.com/HadeedRauf/Trinity_Dev_Web.git . || git pull origin main

# Create .env file for backend
echo "⚙️ Creating environment configuration..."
cat > backend/.env << 'ENVEOF'
DEBUG=False
SECRET_KEY=your-secret-key-change-this-in-production
ALLOWED_HOSTS=13.53.101.211,ec2-13-53-101-211.eu-north-1.compute.amazonaws.com,localhost,127.0.0.1
DATABASE_NAME=time_manager
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=db
DATABASE_PORT=5432
ENVEOF

# Create .env file for frontend
cat > frontend/.env << 'ENVEOF'
VITE_API_URL=http://13.53.101.211:8000/api
REACT_APP_API_URL=http://13.53.101.211:8000/api
ENVEOF

# Set correct permissions
sudo chown -R ec2-user:ec2-user /home/ec2-user/Trinity_Dev_Web
chmod -R 755 /home/ec2-user/Trinity_Dev_Web

echo "✅ Server setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Update the .env files with your settings"
echo "2. Run: docker-compose up -d"
echo "3. Access the application at: http://13.53.101.211:3000"
echo ""
echo "🔑 Default credentials:"
echo "   Admin - username: admin, password: admin"
echo "   Customer - username: customer, password: customer123"
