#!/bin/bash
# ============================================
# Deployment Script - Klinik Management System
# ============================================
# This script automates the deployment process
# Run: sudo bash deploy.sh
# ============================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}Klinik Management System - Deployment Script${NC}"
echo -e "${GREEN}============================================${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root or with sudo${NC}"
    exit 1
fi

# ============================================
# 1. Update System
# ============================================
echo -e "\n${YELLOW}[1/10] Updating system...${NC}"
apt update && apt upgrade -y

# ============================================
# 2. Install Dependencies
# ============================================
echo -e "\n${YELLOW}[2/10] Installing dependencies...${NC}"
apt install -y python3-pip python3-venv postgresql nginx curl git certbot python3-certbot-nginx

# ============================================
# 3. Create Application User
# ============================================
echo -e "\n${YELLOW}[3/10] Creating application user...${NC}"
if ! id -u www-data >/dev/null 2>&1; then
    adduser --system --no-create-home www-data
fi

# ============================================
# 4. Setup PostgreSQL Database
# ============================================
echo -e "\n${YELLOW}[4/10] Setting up PostgreSQL database...${NC}"

# Set database credentials (change these!)
DB_NAME="klinik_db"
DB_USER="klinik_user"
DB_PASSWORD="KlinikSecure2024!@#"

sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME};" 2>/dev/null || echo "Database already exists"
sudo -u postgres psql -c "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';" 2>/dev/null || echo "User already exists"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};" 2>/dev/null || true
sudo -u postgres psql -c "ALTER ROLE ${DB_USER} SET client_encoding TO 'utf8';" 2>/dev/null || true
sudo -u postgres psql -c "ALTER ROLE ${DB_USER} SET default_transaction_isolation TO 'read committed';" 2>/dev/null || true
sudo -u postgres psql -c "ALTER ROLE ${DB_USER} SET timezone TO 'Asia/Jakarta';" 2>/dev/null || true

# ============================================
# 5. Clone/Setup Application
# ============================================
echo -e "\n${YELLOW}[5/10] Setting up application...${NC}"

APP_DIR="/var/www/klinik"
if [ ! -d "$APP_DIR" ]; then
    echo "Creating application directory..."
    mkdir -p $APP_DIR
    git clone https://github.com/username/klinik-management.git $APP_DIR 2>/dev/null || {
        echo -e "${RED}Failed to clone repository. Please set up manually.${NC}"
        exit 1
    }
else
    echo "Application directory already exists. Pulling latest changes..."
    cd $APP_DIR
    git pull
fi

# ============================================
# 6. Setup Python Virtual Environment
# ============================================
echo -e "\n${YELLOW}[6/10] Setting up Python environment...${NC}"

cd $APP_DIR
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# ============================================
# 7. Setup Environment Variables
# ============================================
echo -e "\n${YELLOW}[7/10] Configuring environment variables...${NC}"

if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file. Please edit it with your settings!"
    echo "Required changes:"
    echo "  - SECRET_KEY"
    echo "  - ALLOWED_HOSTS"
    echo "  - DB_PASSWORD"
    echo "  - SECURE settings"
fi

# ============================================
# 8. Database Migration
# ============================================
echo -e "\n${YELLOW}[8/10] Running database migrations...${NC}"

source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

# ============================================
# 9. Setup Gunicorn Service
# ============================================
echo -e "\n${YELLOW}[9/10] Setting up Gunicorn service...${NC}"

cat > /etc/systemd/system/klinik.service << EOF
[Unit]
Description=Klinik Management System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
ExecStart=$APP_DIR/venv/bin/gunicorn --workers 3 --bind unix:/var/www/klinik/klinik_project.sock klinik_project.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable klinik
systemctl start klinik

# ============================================
# 10. Setup Nginx
# ============================================
echo -e "\n${YELLOW}[10/10] Configuring Nginx...${NC}"

cat > /etc/nginx/sites-available/klinik << 'EOF'
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    # Static Files
    location /static/ {
        alias /var/www/klinik/staticfiles/;
    }

    # Media Files
    location /media/ {
        alias /var/www/klinik/media/;
    }

    # Gunicorn
    location / {
        proxy_pass http://unix:/var/www/klinik/klinik_project.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

ln -sf /etc/nginx/sites-available/klinik /etc/nginx/sites-enabled/
nginx -t && systemctl restart nginx

# ============================================
# Setup SSL Certificate
# ============================================
echo -e "\n${YELLOW}Setting up SSL certificate...${NC}"
echo "Please replace 'your-domain.com' with your actual domain!"
certbot --nginx -d your-domain.com -d www.your-domain.com

# ============================================
# Final Setup
# ============================================
echo -e "\n${GREEN}============================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}============================================${NC}"

# Create superuser
echo -e "\n${YELLOW}Creating superuser...${NC}"
echo "Run: cd /var/www/klinik && source venv/bin/activate && python manage.py createsuperuser"

# Set permissions
echo -e "\n${YELLOW}Setting permissions...${NC}"
chown -R www-data:www-data /var/www/klinik
chmod -R 755 /var/www/klinik

echo -e "\n${GREEN}Your Klinik Management System is ready!${NC}"
echo -e "${GREEN}Access: https://your-domain.com${NC}"
echo -e "${YELLOW}Don't forget to:${NC}"
echo -e "  1. Edit .env file with your settings"
echo -e "  2. Create superuser"
echo -e "  3. Set up SSL certificate"
echo -e "  4. Configure firewall"
