# EC2 Deployment Guide - Amazon Linux ARM

Complete step-by-step guide to deploy the Memory-Enabled Strands Agent on EC2.

## Prerequisites
- Fresh EC2 instance (Amazon Linux ARM)
- Security group allowing ports: 22 (SSH), 8000 (API), 8501 (Streamlit)
- AWS credentials configured or IAM role attached

## Step 1: Connect to EC2 Instance

```bash
ssh -i your-key.pem ec2-user@your-ec2-ip
```

## Step 2: System Update & Install Dependencies

```bash
# Update system
sudo yum update -y

# Install Python 3.11
sudo yum install python3.11 python3.11-pip -y

# Install Git
sudo yum install git -y

# Install Graphviz (required for diagrams)
sudo yum install graphviz graphviz-devel -y

# Install development tools
sudo yum groupinstall "Development Tools" -y
```

## Step 3: Install AWS CLI v2

```bash
# Download AWS CLI for ARM
curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"

# Install unzip if not present
sudo yum install unzip -y

# Unzip and install
unzip awscliv2.zip
sudo ./aws/install

# Verify installation
aws --version

# Configure AWS CLI (if not using IAM role)
aws configure
```

## Step 4: Clone Repository

```bash
# Navigate to home directory
cd ~

# Clone your repository
git clone https://github.com/YOUR_USERNAME/AWS_strands_agents_aws_mcp.git

# Navigate to project
cd AWS_strands_agents_aws_mcp/strands-agents
```

## Step 5: Setup Python Environment

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install uv (for MCP server)
pip install uv
```

## Step 6: Install Python Dependencies

```bash
# Install all requirements
pip install -r requirements.txt

# Install diagrams package explicitly
pip install diagrams

# Verify installations
pip list | grep -E "fastapi|streamlit|mem0|strands|diagrams"
```

## Step 7: Configure Environment Variables

```bash
# Create .env file
cat > .env << 'EOF'
# AWS Configuration
AWS_REGION=us-east-1
AWS_PROFILE=default

# API Configuration
API_BASE_URL=http://localhost:8000

# Cognito (Optional - leave empty for demo mode)
COGNITO_DOMAIN=
COGNITO_CLIENT_ID=
COGNITO_CLIENT_SECRET=
REDIRECT_URI=http://your-ec2-ip:8501

# Bedrock Configuration
AWS_DEFAULT_REGION=us-east-1
EOF

# Make sure AWS credentials are available
aws sts get-caller-identity
```

## Step 8: Test Components

```bash
# Test memory configuration
python memory_config.py

# Test agent
python memory_agent.py

# Test diagram generation
python test.py
```

## Step 9: Start Backend API

```bash
# Option 1: Run in foreground (for testing)
python api.py

# Option 2: Run in background with nohup
nohup python api.py > api.log 2>&1 &

# Option 3: Run with screen (recommended)
screen -S api
python api.py
# Press Ctrl+A then D to detach
```

## Step 10: Start Streamlit Frontend

```bash
# Open new terminal or screen session
screen -S streamlit

# Activate virtual environment
cd ~/AWS_strands_agents_aws_mcp/strands-agents
source venv/bin/activate

# Start Streamlit
streamlit run streamlit_auth.py --server.port 8501 --server.address 0.0.0.0

# Press Ctrl+A then D to detach
```

## Step 11: Configure Security Group

In AWS Console:
1. Go to EC2 → Security Groups
2. Select your instance's security group
3. Add Inbound Rules:
   - Type: Custom TCP, Port: 8000, Source: Your IP or 0.0.0.0/0
   - Type: Custom TCP, Port: 8501, Source: Your IP or 0.0.0.0/0

## Step 12: Access Application

```bash
# API Documentation
http://your-ec2-ip:8000/docs

# Streamlit UI
http://your-ec2-ip:8501

# Health Check
curl http://your-ec2-ip:8000/health
```

## Step 13: Setup Systemd Services (Production)

### Create API Service

```bash
sudo tee /etc/systemd/system/strands-api.service > /dev/null << 'EOF'
[Unit]
Description=Strands Agent API
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/AWS_strands_agents_aws_mcp/strands-agents
Environment="PATH=/home/ec2-user/AWS_strands_agents_aws_mcp/strands-agents/venv/bin"
ExecStart=/home/ec2-user/AWS_strands_agents_aws_mcp/strands-agents/venv/bin/python api.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```

### Create Streamlit Service

```bash
sudo tee /etc/systemd/system/strands-streamlit.service > /dev/null << 'EOF'
[Unit]
Description=Strands Streamlit UI
After=network.target strands-api.service

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/home/ec2-user/AWS_strands_agents_aws_mcp/strands-agents
Environment="PATH=/home/ec2-user/AWS_strands_agents_aws_mcp/strands-agents/venv/bin"
ExecStart=/home/ec2-user/AWS_strands_agents_aws_mcp/strands-agents/venv/bin/streamlit run streamlit_auth.py --server.port 8501 --server.address 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```

### Enable and Start Services

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable services to start on boot
sudo systemctl enable strands-api
sudo systemctl enable strands-streamlit

# Start services
sudo systemctl start strands-api
sudo systemctl start strands-streamlit

# Check status
sudo systemctl status strands-api
sudo systemctl status strands-streamlit

# View logs
sudo journalctl -u strands-api -f
sudo journalctl -u strands-streamlit -f
```

## Troubleshooting

### Check if ports are listening
```bash
sudo netstat -tlnp | grep -E '8000|8501'
```

### Check application logs
```bash
# API logs
tail -f api.log

# Streamlit logs
tail -f ~/.streamlit/logs/*.log
```

### Test API endpoint
```bash
curl http://localhost:8000/health
```

### Check AWS credentials
```bash
aws sts get-caller-identity
```

### Verify Graphviz installation
```bash
dot -V
```

### Check Python packages
```bash
pip list | grep -E "diagrams|graphviz"
```

## Useful Commands

### Manage Screen Sessions
```bash
# List sessions
screen -ls

# Reattach to session
screen -r api
screen -r streamlit

# Kill session
screen -X -S api quit
```

### Manage Systemd Services
```bash
# Stop services
sudo systemctl stop strands-api
sudo systemctl stop strands-streamlit

# Restart services
sudo systemctl restart strands-api
sudo systemctl restart strands-streamlit

# Disable services
sudo systemctl disable strands-api
sudo systemctl disable strands-streamlit
```

### Monitor Resources
```bash
# CPU and Memory
htop

# Disk usage
df -h

# Check running processes
ps aux | grep python
```

## Security Best Practices

1. **Use IAM Roles**: Attach IAM role to EC2 instead of storing credentials
2. **Restrict Security Groups**: Limit access to specific IPs
3. **Enable HTTPS**: Use nginx/Apache with SSL certificate
4. **Update Regularly**: Keep system and packages updated
5. **Monitor Logs**: Set up CloudWatch for log monitoring

## Optional: Setup Nginx Reverse Proxy

```bash
# Install nginx
sudo yum install nginx -y

# Configure nginx
sudo tee /etc/nginx/conf.d/strands.conf > /dev/null << 'EOF'
server {
    listen 80;
    server_name your-domain.com;

    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
EOF

# Start nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

## Backup and Restore

### Backup Memory Data
```bash
# Backup Qdrant data
tar -czf qdrant_backup_$(date +%Y%m%d).tar.gz ~/.qdrant
```

### Restore Memory Data
```bash
# Restore from backup
tar -xzf qdrant_backup_YYYYMMDD.tar.gz -C ~/
```

## Performance Tuning

### For ARM instances (t4g, m6g, etc.)
```bash
# Check ARM architecture
uname -m  # Should show aarch64

# Ensure using ARM-optimized packages
pip install --upgrade --force-reinstall numpy pandas
```

## Next Steps

1. Configure domain name and SSL certificate
2. Set up CloudWatch monitoring
3. Configure automated backups
4. Set up CI/CD pipeline
5. Implement rate limiting and authentication

## Support

For issues:
- Check logs: `sudo journalctl -u strands-api -f`
- Verify AWS credentials: `aws sts get-caller-identity`
- Test connectivity: `curl http://localhost:8000/health`
