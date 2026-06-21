# Panduan Deployment Klinik Management System

## 🎯 Prerequisites

- Server Ubuntu 22.04 atawa leuwih anyar
- Python 3.12+
- PostgreSQL 14+
- Nginx
- Git
- SSL Certificate (Let's Encrypt recommended)

## 📋 Langkah Deployment

### 1. Setup Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3-pip python3-venv postgresql nginx curl -y

# Install Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y
```

### 2. Setup Database

```bash
# Login ka PostgreSQL
sudo -u postgres psql

# Buat database jeung user
CREATE DATABASE klinik_db;
CREATE USER klinik_user WITH PASSWORD 'your-strong-password';
ALTER ROLE klinik_user SET client_encoding TO 'utf8';
ALTER ROLE klinik_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE klinik_user SET timezone TO 'Asia/Jakarta';
GRANT ALL PRIVILEGES ON DATABASE klinik_db TO klinik_user;
\q
```

### 3. Clone Repository

```bash
cd /var/www
sudo git clone https://github.com/username/klinik-management.git
sudo chown -R $USER:$USER klinik-management
cd klinik-management
```

### 4. Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Environment Configuration

```bash
cp .env.example .env
nano .env
```

Edit `.env` pikeun production:

```env
SECRET_KEY=your-very-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

DB_ENGINE=django.db.backends.postgresql
DB_NAME=klinik_db
DB_USER=klinik_user
DB_PASSWORD=your-strong-password
DB_HOST=localhost
DB_PORT=5432

SECURE_SSL_REDIRECT=True
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
```

### 6. Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
```

### 7. Test Application

```bash
python manage.py test
python manage.py check --deploy
```

### 8. Setup Gunicorn

```bash
sudo pip install gunicorn
```

Test Gunicorn:

```bash
gunicorn --bind 0.0.0.0:8000 klinik_project.wsgi:application
```

### 9. Setup Systemd Service

Buat file `/etc/systemd/system/klinik.service`:

```ini
[Unit]
Description=Klinik Management System
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/klinik-management
Environment="PATH=/var/www/klinik-management/venv/bin"
ExecStart=/var/www/klinik-management/venv/bin/gunicorn --workers 3 --bind unix:/var/www/klinik-management/klinik_project.sock klinik_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable jeung start service:

```bash
sudo systemctl daemon-reload
sudo systemctl start klinik
sudo systemctl enable klinik
```

### 10. Setup Nginx

Buat file `/etc/nginx/sites-available/klinik`:

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
        alias /var/www/klinik-management/staticfiles/;
    }

    # Media Files
    location /media/ {
        alias /var/www/klinik-management/media/;
    }

    # Gunicorn
    location / {
        proxy_pass http://unix:/var/www/klinik-management/klinik_project.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/klinik /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 11. Setup SSL Certificate

```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### 12. Firewall Configuration

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

## 🔍 Monitoring

### Check Service Status

```bash
sudo systemctl status klinik
sudo journalctl -u klinik -f
```

### Check Nginx

```bash
sudo systemctl status nginx
sudo tail -f /var/log/nginx/error.log
```

### Check Database

```bash
sudo -u postgres psql -c "\l"
sudo -u postgres psql -d klinik_db -c "\dt"
```

## 🔄 Update Application

```bash
cd /var/www/klinik-management
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart klinik
sudo systemctl restart nginx
```

## 🆘 Troubleshooting

### Permission Issues

```bash
sudo chown -R www-data:www-data /var/www/klinik-management
sudo chmod -R 755 /var/www/klinik-management
```

### Database Connection Issues

```bash
sudo systemctl status postgresql
sudo -u postgres psql -c "SELECT 1"
```

### Gunicorn Issues

```bash
sudo systemctl status klinik
sudo journalctl -u klinik -n 50
```

### Nginx Issues

```bash
sudo nginx -t
sudo tail -f /var/log/nginx/error.log
```

## 📚 Dokumentasi Tambahan

- [Installation Guide](INSTALL.md)
- [API Documentation](API.md)
- [Architecture Overview](ARCHITECTURE.md)
