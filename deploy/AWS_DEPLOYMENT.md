# AWS EC2 Deployment Guide for DetoxifyAI

## Prerequisites
- AWS Account
- Your Azure Storage connection string

## Step 1: Launch EC2 Instance

1. Go to AWS EC2 Console
2. Click "Launch Instance"
3. Choose configuration:
   - **Name**: DetoxifyAI-Server
   - **AMI**: Ubuntu Server 22.04 LTS (Free tier eligible)
   - **Instance Type**: t2.medium or t3.medium (recommended for ML workloads)
   - **Key pair**: Create new or use existing (save the .pem file)
   - **Network settings**:
     - Allow SSH (port 22) from your IP
     - Allow HTTP (port 80) from anywhere
     - Allow HTTPS (port 443) from anywhere
     - Allow Custom TCP (port 8000) from anywhere (for testing)
   - **Storage**: 20 GB gp3 (minimum)
4. Launch instance

## Step 2: Connect to Your EC2 Instance

```bash
# Make your key pair file read-only
chmod 400 your-key.pem

# SSH into your instance
ssh -i your-key.pem ubuntu@<your-ec2-public-ip>
```

## Step 3: Set Up the Server

Once connected to your EC2 instance, run these commands:

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python and required system packages
sudo apt install -y python3-pip python3-venv nginx git

# Clone your repository
git clone https://github.com/al-Jurjani/DetoxifyAI.git
cd DetoxifyAI

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download NLTK data (required for preprocessing)
python3 -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## Step 4: Configure Environment Variables

```bash
# Create .env file with your Azure connection string
nano .env
```

Add this content (replace with your actual connection string):
```
AZURE_STORAGE_CONNECTION_STRING="your-connection-string-here"
```

Press `Ctrl+X`, then `Y`, then `Enter` to save.

## Step 5: Test FastAPI Manually

```bash
# From the DetoxifyAI directory
source venv/bin/activate
cd app
uvicorn main:app --host 0.0.0.0 --port 8000

# In another terminal, test it:
curl http://<your-ec2-public-ip>:8000/health
```

If this works, press `Ctrl+C` to stop the server.

## Step 6: Set Up Systemd Service (Production)

```bash
# Copy the service file
sudo cp deploy/detoxifyai.service /etc/systemd/system/

# Edit the service file to update paths
sudo nano /etc/systemd/system/detoxifyai.service
# Update User, WorkingDirectory, and Environment paths to match your setup

# Reload systemd and start service
sudo systemctl daemon-reload
sudo systemctl enable detoxifyai
sudo systemctl start detoxifyai

# Check status
sudo systemctl status detoxifyai

# View logs
sudo journalctl -u detoxifyai -f
```

## Step 7: Set Up Nginx (Reverse Proxy)

```bash
# Copy nginx config
sudo cp deploy/nginx-detoxifyai.conf /etc/nginx/sites-available/detoxifyai

# Create symbolic link
sudo ln -s /etc/nginx/sites-available/detoxifyai /etc/nginx/sites-enabled/

# Remove default nginx site
sudo rm /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

## Step 8: Deploy Frontend

```bash
# Copy frontend files to nginx web root
sudo mkdir -p /var/www/detoxifyai
sudo cp -r frontend/* /var/www/detoxifyai/

# Update API URL in frontend
sudo nano /var/www/detoxifyai/app.js
# Change API_URL to: const API_URL = 'http://<your-ec2-public-ip>';
# Or use '/api' if using nginx proxy

# Set proper permissions
sudo chown -R www-data:www-data /var/www/detoxifyai
```

## Step 9: Access Your Application

- **Frontend**: http://<your-ec2-public-ip>
- **API Health**: http://<your-ec2-public-ip>/api/health
- **API Docs**: http://<your-ec2-public-ip>/api/docs

## Optional: Set Up Domain Name

1. Purchase a domain or use existing one
2. Create an A record pointing to your EC2 public IP
3. Update nginx configuration with your domain name
4. Set up SSL/TLS with Let's Encrypt:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## Troubleshooting

### Check FastAPI Service
```bash
sudo systemctl status detoxifyai
sudo journalctl -u detoxifyai -n 50
```

### Check Nginx
```bash
sudo systemctl status nginx
sudo tail -f /var/log/nginx/error.log
```

### Check if port 8000 is listening
```bash
sudo netstat -tulpn | grep 8000
```

### Restart services
```bash
sudo systemctl restart detoxifyai
sudo systemctl restart nginx
```

## Security Recommendations

1. **Use Security Groups**: Restrict SSH (port 22) to your IP only
2. **Set up firewall**:
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```
3. **Use SSL/TLS**: Set up HTTPS with Let's Encrypt
4. **Keep Azure credentials secure**: Never commit .env to git
5. **Regular updates**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

## Updating Your Application

```bash
cd ~/DetoxifyAI
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart detoxifyai
```
