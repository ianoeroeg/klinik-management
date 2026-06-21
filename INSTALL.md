# Panduan Instalasi Klinik Management System

## 📋 Requirements

- Python 3.12+
- PostgreSQL 14+ (production) atawa SQLite (development)
- pip
- Git

## 🚀 Langkah Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/username/klinik-management.git
cd klinik-management
```

### 2. Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

```bash
cp .env.example .env
```

Edit file `.env`:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Development - SQLite)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Database (Production - PostgreSQL)
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=klinik_db
# DB_USER=klinik_user
# DB_PASSWORD=your-password
# DB_HOST=localhost
# DB_PORT=5432

# Security
SECURE_SSL_REDIRECT=False
```

### 5. Database Setup

```bash
# Buat migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Buat superuser
python manage.py createsuperuser
```

### 6. Collect Static Files

```bash
python manage.py collectstatic
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Aksés: http://localhost:8000

## ✅ Verifikasi Instalasi

1. Buka browser jeung aksés http://localhost:8000
2. Login kalayan akun superuser anu geus dijieun
3. Cek dashboard - kudu muncul statistik klinik
4. Coba tambah data pasien, dokter, jeung appointment

## 🔧 Troubleshooting

### Masalah Database

```bash
# Hapus database jeung reset
rm db.sqlite3
python manage.py migrate
```

### Masalah Static Files

```bash
# Clear cache jeung collect ulang
python manage.py collectstatic --clear
python manage.py collectstatic
```

### Masalah Dependencies

```bash
# Install deui dependencies
pip install -r requirements.txt --force-reinstall
```

## 📚 Dokumentasi Tambahan

- [Deployment Guide](DEPLOY.md)
- [API Documentation](API.md)
- [Architecture Overview](ARCHITECTURE.md)
