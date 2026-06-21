# 🚀 Deployment Guide - Klinik Management System

## 📋 Quick Deployment (Automated)

### Option 1: Automated Deployment Script

```bash
# Download and run deployment script
cd /tmp
wget https://raw.githubusercontent.com/username/klinik-management/main/deploy.sh
chmod +x deploy.sh
sudo bash deploy.sh
```

### Option 2: Manual Deployment

Follow the steps below for manual deployment.

---

## 📋 Manual Deployment Steps

### Prerequisites

- Ubuntu 22.04+ server
- Domain name pointed to server IP
- Root access to server

### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-venv postgresql nginx curl git certbot python3-certbot-nginx
```

### Step 2: Database Setup

```bash
# Login to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE klinik_db;
CREATE USER klinik_user WITH PASSWORD 'your-strong-password';
GRANT ALL PRIVILEGES ON DATABASE klinik_db TO klinik_user;
ALTER ROLE klinik_user SET client_encoding TO 'utf8';
ALTER ROLE klinik_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE klinik_user SET timezone TO 'Asia/Jakarta';
\q
```

### Step 3: Application Setup

```bash
# Create application directory
sudo mkdir -p /var/www/klinik
cd /var/www/klinik

# Clone repository (replace with your repo)
sudo git clone https://github.com/username/klinik-management.git .
sudo chown -R $USER:$USER .

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Setup environment
cp .env.example .env
nano .env  # Edit with your settings
```

### Step 4: Database Migration

```bash
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### Step 5: Gunicorn Service

```bash
# Create service file
sudo nano /etc/systemd/system/klinik.service
```

Add the following content:

```ini
[Unit]
Description=Klinik Management System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/klinik
Environment="PATH=/var/www/klinik/venv/bin"
ExecStart=/var/www/klinik/venv/bin/gunicorn --workers 3 --bind unix:/var/www/klinik/klinik_project.sock klinik_project.wsgi:application
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable klinik
sudo systemctl start klinik
sudo systemctl status klinik
```

### Step 6: Nginx Configuration

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/klinik
```

Add the following content:

```nginx
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
```

Enable the site and test configuration:

```bash
sudo ln -s /etc/nginx/sites-available/klinik /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 7: SSL Certificate

```bash
# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

### Step 8: Firewall Configuration

```bash
# Configure firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

---

## 🔧 Post-Deployment Tasks

### 1. Verify Deployment

```bash
# Check services
sudo systemctl status klinik
sudo systemctl status nginx
sudo systemctl status postgresql

# Test application
curl -I https://your-domain.com

# Run health check
bash health_check.sh
```

### 2. Setup Monitoring

```bash
# Setup log monitoring
sudo tail -f /var/log/klinik/error.log

# Setup backup
sudo crontab -e
# Add: 0 2 * * * /var/www/klinik/backup.sh
```

### 3. Performance Optimization

```bash
# Optimize PostgreSQL
sudo nano /etc/postgresql/14/main/postgresql.conf
# Adjust: shared_buffers, effective_cache_size, work_mem

# Restart PostgreSQL
sudo systemctl restart postgresql
```

---

## 🆘 Troubleshooting

### Common Issues

#### 1. Gunicorn Not Starting

```bash
# Check logs
sudo journalctl -u klinik -n 50

# Check permissions
ls -la /var/www/klinik/
sudo chown -R www-data:www-data /var/www/klinik
```

#### 2. Nginx 502 Bad Gateway

```bash
# Check Gunicorn socket
ls -la /var/www/klinik/klinik_project.sock

# Restart Gunicorn
sudo systemctl restart klinik
```

#### 3. Database Connection Error

```bash
# Check PostgreSQL
sudo systemctl status postgresql

# Test connection
sudo -u postgres psql -d klinik_db -c "SELECT 1"
```

#### 4. Static Files Not Loading

```bash
# Collect static files
cd /var/www/klinik
source venv/bin/activate
python manage.py collectstatic --noinput

# Check permissions
sudo chown -R www-data:www-data /var/www/klinik/staticfiles
```

---

## 📊 Monitoring

### System Monitoring

```bash
# Check system resources
htop
df -h
free -h

# Check application logs
sudo journalctl -u klinik -f
sudo tail -f /var/log/nginx/error.log
```

### Application Monitoring

```bash
# Run health check
bash health_check.sh

# Check database size
sudo -u postgres psql -d klinik_db -c "SELECT pg_size_pretty(pg_database_size('klinik_db'));"

# Check user activity
sudo -u postgres psql -d klinik_db -c "SELECT count(*) FROM accounts_customuser;"
```

---

## 🔄 Maintenance

### Regular Tasks

```bash
# Daily: Check logs
sudo journalctl -u klinik --since "24 hours ago" | grep ERROR

# Weekly: Backup database
bash backup.sh

# Monthly: Update system
sudo apt update && sudo apt upgrade -y
sudo systemctl restart klinik
```

### Backup Strategy

```bash
# Automated backup (add to crontab)
0 2 * * * /var/www/klinik/backup.sh

# Backup retention (keep last 30 days)
find /var/backups/klinik -name "*.sql" -mtime +30 -delete
find /var/backups/klinik -name "*.tar.gz" -mtime +30 -delete
```

---

## 📞 Support

For deployment issues:
- Check logs: `sudo journalctl -u klinik -f`
- Run health check: `bash health_check.sh`
- Contact: admin@klinik.com
