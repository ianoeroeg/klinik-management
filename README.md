# 🏥 Klinik Management System

Sistem manajemen klinik berbasis web ngagunakeun **Python** jeung **Django**.

## 📋 Status Proyek

### ✅ Tahap 1 — Setup Lingkungan
- Python 3.13.12, Django 6.0.6, DRF 3.17.1
- PostgreSQL driver, Pillow, xlsxwriter, weasyprint
- Crispy Forms, Gunicorn, Whitenoise, python-decouple

### ✅ Tahap 2 — Desain Database (Models)
- 7 apps: accounts, patients, doctors, appointments, prescriptions, billing, reports
- 13+ models jeung relasi anu lengkap
- Migrations geus dijieun jeung di-migrate
- Superuser: `admin` / `admin123`

### ✅ Tahap 3 — Views, URLs, Templates
- **Views**: 20+ view functions & class-based views
- **URLs**: 25+ URL patterns
- **Admin**: Custom admin pikeun sakabéh models
- **Templates**: 15+ templates jeung Bootstrap 5

### ✅ Tahap 4 — REST API (Django Rest Framework) (RENGSÉ!)
- **Serializers**: 8 serializers pikeun sakabéh models
- **ViewSets**: 8 viewsets jeung custom actions
- **Permissions**: Session & Basic Authentication
- **API Endpoints**: 8 resources + custom endpoints

## 🚀 Cara Ngajalankeun

```bash
cd klinik_project

# Jieun superuser (lamun can):
python3 manage.py createsuperuser

# Jalankeun server:
python3 manage.py runserver

# Buka browser:
# http://127.0.0.1:8000/        → Home
# http://127.0.0.1:8000/login/  → Login
# http://127.0.0.1:8000/admin/  → Admin panel
```

## 📡 API Documentation

Base URL: `http://127.0.0.1:8000/api/`

### Authentication
- Session Authentication (web)
- Basic Authentication (API)
- Contoh: `admin` / `admin123`

### API Endpoints

| Resource | URL | Methods |
|----------|-----|---------|
| Users | `/api/users/` | GET, POST, PUT, PATCH, DELETE |
| Patients | `/api/patients/` | GET, POST, PUT, PATCH, DELETE |
| Doctors | `/api/doctors/` | GET, POST, PUT, PATCH, DELETE |
| Appointments | `/api/appointments/` | GET, POST, PUT, PATCH, DELETE |
| Medicines | `/api/medicines/` | GET, POST, PUT, PATCH, DELETE |
| Prescriptions | `/api/prescriptions/` | GET, POST, PUT, PATCH, DELETE |
| Invoices | `/api/invoices/` | GET, POST, PUT, PATCH, DELETE |
| Payments | `/api/payments/` | GET, POST, PUT, PATCH, DELETE |

### Custom Actions

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/appointments/today/` | GET | Today's appointments |
| `/api/appointments/<pk>/update_status/` | POST | Update appointment status |
| `/api/medicines/low_stock/` | GET | Low stock medicines (≤10) |
| `/api/invoices/revenue/` | GET | Revenue statistics |

### Filter & Search

- **Search**: `?search=<keyword>` (depends on model)
- **Filter**: `?status=completed&priority=urgent`
- **Pagination**: Default 20 items per page

### Contoh API Call (curl)

```bash
# Get all patients
curl -u admin:admin123 http://127.0.0.1:8000/api/patients/

# Get today's appointments
curl -u admin:admin123 http://127.0.0.1:8000/api/appointments/today/

# Get low stock medicines
curl -u admin:admin123 http://127.0.0.1:8000/api/medicines/low_stock/

# Get revenue
curl -u admin:admin123 http://127.0.0.1:8000/api/invoices/revenue/

# Create new patient
curl -X POST -u admin:admin123 \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "nik": "1234567890", "gender": "L"}' \
  http://127.0.0.1:8000/api/patients/
```

## 📁 Struktur Templates

```
templates/
├── base.html              # Template utama (sidebar + layout)
├── base_auth.html         # Template pikeun login/home
├── accounts/
│   ├── home.html          # Halaman utama
│   ├── login.html         # Form login
│   └── dashboard.html     # Dashboard
├── patients/
│   ├── patient_list.html
│   ├── patient_detail.html
│   └── patient_form.html
├── doctors/
│   ├── doctor_list.html
│   └── doctor_detail.html
├── appointments/
│   ├── appointment_list.html
│   ├── appointment_detail.html
│   └── appointment_form.html
├── prescriptions/
│   ├── prescription_list.html
│   ├── prescription_detail.html
│   └── medicine_list.html
├── billing/
│   ├── invoice_list.html
│   ├── invoice_detail.html
│   └── payment_list.html
└── reports/
    └── dashboard.html
```

## ✅ Status Tahap 4
- [x] Serializers: 8 serializers (User, Patient, Doctor, Appointment, Medicine, Prescription, Invoice, Payment)
- [x] ViewSets: 8 viewsets jeung CRUD operations
- [x] Custom Actions: today, update_status, low_stock, revenue
- [x] Permissions: IsAuthenticated + IsAdminOrReadOnly
- [x] Authentication: Session + Basic Auth
- [x] Filtering & Search: filterset_fields + search_fields
- [x] Pagination: 20 items per page
- [x] All API endpoints tested: 200 OK
# klinik-management
