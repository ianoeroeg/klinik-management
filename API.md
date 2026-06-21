# API Documentation - Klinik Management System

## 📖 Overview

REST API pikeun Klinik Management System, dilindungi ku JWT authentication.

**Base URL**: `https://your-domain.com/api/v1/`

## 🔐 Authentication

Semua endpoint (kajaba `/auth/login/` jeung `/auth/register/`) butuh authentication token.

### Login

```http
POST /api/v1/auth/login/
Content-Type: application/json

{
    "username": "admin",
    "password": "admin123"
}
```

**Response**:

```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
        "id": 1,
        "username": "admin",
        "role": "admin",
        "email": "admin@klinik.com"
    }
}
```

### Refresh Token

```http
POST /api/v1/auth/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## 📋 Endpoints

### 👤 Users

#### Get All Users (Admin only)

```http
GET /api/v1/users/
Authorization: Bearer <token>
```

**Query Parameters**:
- `role` - Filter ku role (admin, dokter, staff, pasien)
- `search` - Search ku username, email, atawa nama
- `page` - Pagination (default: 1)
- `page_size` - Items per page (default: 20)

**Response**:

```json
{
    "count": 10,
    "next": "http://api/v1/users/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "username": "admin",
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@klinik.com",
            "role": "admin",
            "phone": "+6281234567890",
            "is_active": true,
            "created_at": "2026-01-01T00:00:00Z"
        }
    ]
}
```

#### Get User Detail

```http
GET /api/v1/users/{id}/
Authorization: Bearer <token>
```

#### Create User (Admin only)

```http
POST /api/v1/users/
Authorization: Bearer <token>
Content-Type: application/json

{
    "username": "dr_sinta",
    "password": "securepass123",
    "first_name": "Sinta",
    "last_name": "Medika",
    "email": "sinta@klinik.com",
    "role": "dokter",
    "phone": "+6281234567890"
}
```

#### Update User

```http
PUT /api/v1/users/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
    "first_name": "Sinta",
    "last_name": "Medika",
    "email": "sinta@klinik.com",
    "phone": "+6281234567890"
}
```

#### Delete User (Admin only)

```http
DELETE /api/v1/users/{id}/
Authorization: Bearer <token>
```

### 🏥 Patients

#### Get All Patients

```http
GET /api/v1/patients/
Authorization: Bearer <token>
```

**Query Parameters**:
- `search` - Search ku nama, NIK, atawa telepon
- `gender` - Filter ku gender (L/P)
- `page` - Pagination

#### Get Patient Detail

```http
GET /api/v1/patients/{id}/
Authorization: Bearer <token>
```

**Response**:

```json
{
    "id": 1,
    "user": {
        "username": "pasien1",
        "first_name": "Andi",
        "last_name": "Wijaya",
        "email": "andi@email.com"
    },
    "nik": "3201234567890001",
    "date_of_birth": "1990-05-15",
    "gender": "L",
    "address": "Jl. Merdeka No. 10, Bandung",
    "phone": "+6281234567890",
    "blood_type": "A",
    "age": 34,
    "created_at": "2026-01-01T00:00:00Z"
}
```

#### Create Patient

```http
POST /api/v1/patients/
Authorization: Bearer <token>
Content-Type: application/json

{
    "user": 1,
    "nik": "3201234567890001",
    "date_of_birth": "1990-05-15",
    "gender": "L",
    "address": "Jl. Merdeka No. 10, Bandung",
    "phone": "+6281234567890",
    "blood_type": "A"
}
```

### 👨‍⚕️ Doctors

#### Get All Doctors

```http
GET /api/v1/doctors/
Authorization: Bearer <token>
```

**Query Parameters**:
- `specialization` - Filter ku spesialisasi
- `is_available` - Filter ku ketersediaan (true/false)
- `search` - Search ku nama

#### Get Doctor Detail

```http
GET /api/v1/doctors/{id}/
Authorization: Bearer <token>
```

**Response**:

```json
{
    "id": 1,
    "user": {
        "username": "dr_sinta",
        "first_name": "Sinta",
        "last_name": "Medika",
        "email": "sinta@klinik.com"
    },
    "license_number": "STR-12345",
    "specialization": "umum",
    "education": "S1 Kedokteran",
    "experience_years": 5,
    "consultation_fee": 150000,
    "is_available": true,
    "created_at": "2026-01-01T00:00:00Z"
}
```

### 📅 Appointments

#### Get All Appointments

```http
GET /api/v1/appointments/
Authorization: Bearer <token>
```

**Query Parameters**:
- `doctor_id` - Filter ku dokter
- `patient_id` - Filter ku pasien
- `date` - Filter ku tanggal (YYYY-MM-DD)
- `status` - Filter ku status (scheduled, in_progress, completed, cancelled)
- `page` - Pagination

#### Get Appointment Detail

```http
GET /api/v1/appointments/{id}/
Authorization: Bearer <token>
```

#### Create Appointment

```http
POST /api/v1/appointments/
Authorization: Bearer <token>
Content-Type: application/json

{
    "patient": 1,
    "doctor": 1,
    "appointment_date": "2026-06-25",
    "appointment_time": "10:00:00",
    "reason": "Sakit kepala",
    "priority": "normal"
}
```

**Validasi**:
- Dokter teu bisa appointment dina waktu anu sarua
- Tanggal kudu di hareup
- Waktu kudu format HH:MM:SS

#### Update Appointment Status

```http
PATCH /api/v1/appointments/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
    "status": "in_progress"
}
```

### 💊 Prescriptions

#### Get All Prescriptions

```http
GET /api/v1/prescriptions/
Authorization: Bearer <token>
```

#### Get Prescription Detail

```http
GET /api/v1/prescriptions/{id}/
Authorization: Bearer <token>
```

**Response**:

```json
{
    "id": 1,
    "appointment": {
        "id": 1,
        "patient": "Andi Wijaya",
        "doctor": "Dr. Sinta Medika",
        "appointment_date": "2026-06-25",
        "appointment_time": "10:00:00"
    },
    "diagnosis": "Demam biasa",
    "treatment_notes": "Istirahat jeung minum air putih",
    "status": "written",
    "items": [
        {
            "medicine": {
                "name": "Paracetamol",
                "form": "tablet",
                "price": 5000
            },
            "dosage": "2 tablet",
            "frequency": "3 kali sehari",
            "duration": "5 hari",
            "quantity": 30
        }
    ],
    "created_at": "2026-06-25T10:30:00Z"
}
```

#### Create Prescription

```http
POST /api/v1/prescriptions/
Authorization: Bearer <token>
Content-Type: application/json

{
    "appointment": 1,
    "diagnosis": "Demam biasa",
    "treatment_notes": "Istirahat jeung minum air putih",
    "items": [
        {
            "medicine": 1,
            "dosage": "2 tablet",
            "frequency": "3 kali sehari",
            "duration": "5 hari",
            "quantity": 30
        }
    ]
}
```

### 💰 Billing

#### Get All Invoices

```http
GET /api/v1/invoices/
Authorization: Bearer <token>
```

**Query Parameters**:
- `patient_id` - Filter ku pasien
- `status` - Filter ku status (unpaid, paid, partial, cancelled)
- `date_from` - Filter ti tanggal (YYYY-MM-DD)
- `date_to` - Filter nepi ka tanggal (YYYY-MM-DD)

#### Get Invoice Detail

```http
GET /api/v1/invoices/{id}/
Authorization: Bearer <token>
```

**Response**:

```json
{
    "id": 1,
    "invoice_number": "INV-20260625-0001",
    "patient": "Andi Wijaya",
    "status": "paid",
    "payment_method": "cash",
    "subtotal": 200000,
    "discount": 20000,
    "tax": 18000,
    "total": 198000,
    "amount_paid": 198000,
    "items": [
        {
            "description": "Konsultasi",
            "quantity": 1,
            "unit_price": 150000,
            "total": 150000
        },
        {
            "description": "Resep Obat",
            "quantity": 1,
            "unit_price": 50000,
            "total": 50000
        }
    ],
    "payments": [
        {
            "amount": 198000,
            "method": "cash",
            "payment_date": "2026-06-25T11:00:00Z"
        }
    ],
    "created_at": "2026-06-25T10:30:00Z"
}
```

#### Create Invoice

```http
POST /api/v1/invoices/
Authorization: Bearer <token>
Content-Type: application/json

{
    "appointment": 1,
    "patient": 1,
    "subtotal": 200000,
    "discount": 20000,
    "tax": 18000,
    "items": [
        {
            "description": "Konsultasi",
            "quantity": 1,
            "unit_price": 150000
        },
        {
            "description": "Resep Obat",
            "quantity": 1,
            "unit_price": 50000
        }
    ]
}
```

#### Record Payment

```http
POST /api/v1/invoices/{id}/payments/
Authorization: Bearer <token>
Content-Type: application/json

{
    "method": "cash",
    "amount": 198000,
    "reference_number": "TRF123456",
    "notes": "Pembayaran tunai"
}
```

## 📊 Reports

#### Get Dashboard Statistics (Admin only)

```http
GET /api/v1/reports/dashboard/
Authorization: Bearer <token>
```

**Response**:

```json
{
    "total_patients": 150,
    "total_doctors": 10,
    "today_appointments": 25,
    "today_revenue": 3750000,
    "monthly_revenue": 45000000,
    "patients_this_month": 30,
    "prescriptions_today": 20,
    "available_doctors": 8
}
```

#### Get Revenue Report

```http
GET /api/v1/reports/revenue/
Authorization: Bearer <token>
```

**Query Parameters**:
- `period` - Period (daily, weekly, monthly, yearly)
- `start_date` - Start date (YYYY-MM-DD)
- `end_date` - End date (YYYY-MM-DD)

## 🎯 Error Handling

Semua error response ngagunakeun format standar:

```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid input data",
        "details": {
            "username": ["This field is required."]
        }
    }
}
```

### Error Codes

- `VALIDATION_ERROR` - Input validation failed
- `AUTHENTICATION_ERROR` - Invalid authentication
- `PERMISSION_DENIED` - Insufficient permissions
- `NOT_FOUND` - Resource not found
- `SERVER_ERROR` - Internal server error

## 📈 Rate Limiting

- 100 requests per minute per IP
- 1000 requests per hour per user

## 🔒 Security

- JWT authentication
- Role-based access control
- HTTPS required
- CSRF protection
- Input validation
- SQL injection protection

## 🧪 Testing

```bash
# Run API tests
python manage.py test api

# Test authentication
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Test protected endpoint
curl -X GET http://localhost:8000/api/v1/users/ \
  -H "Authorization: Bearer <token>"
```

## 📚 Dokumentasi Tambahan

- [Installation Guide](INSTALL.md)
- [Deployment Guide](DEPLOY.md)
- [Architecture Overview](ARCHITECTURE.md)
