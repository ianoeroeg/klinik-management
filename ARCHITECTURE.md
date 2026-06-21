# Architecture Overview - Klinik Management System

## 🏗️ System Architecture

Klinik Management System ngagunakeun arsitektur **MVC (Model-View-Controller)** pikeun Django framework, kalayan struktur modular pikeun ngokolola fitur anu béda.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Layer                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Web UI    │  │  Mobile App │  │     REST API        │  │
│  │ (Django HTMX)│  │ (Future)    │  │  (Django REST FW)   │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Middleware  │  │ Authentication│ │   Security Layer    │  │
│  │  (CORS,     │  │  (JWT,       │  │  (CSRF, XSS,       │  │
│  │   Session)  │  │   Session)   │  │   HSTS)            │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Service Layer                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Views     │  │  Services   │  │   Business Logic    │  │
│  │ (HTMX/REST) │  │ (Domain    │  │   (Validation,      │  │
│  │             │  │  Logic)     │  │   Calculation)      │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Models    │  │  Migrations │  │   Database          │  │
│  │ (ORM)       │  │  (Alembic)  │  │  (SQLite/PostgreSQL)│  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Module Structure

### 1. Accounts Module (`accounts/`)

**Tanggung jawab**: User management, authentication, authorization

```
accounts/
├── models.py          # CustomUser, PasswordResetToken
├── views.py           # Login, Logout, Dashboard, User CRUD
├── forms.py           # User forms, Password forms
├── urls.py            # URL routing
├── decorators.py      # Admin-only decorators
├── services.py        # User services
├── tests.py           # Unit tests
└── templates/
    └── accounts/
        ├── login.html
        ├── dashboard.html
        ├── user_list.html
        ├── user_form.html
        └── change_password.html
```

**Key Components**:
- `CustomUser` - User model kalayan role system
- `PasswordResetToken` - Token pikeun reset password
- `admin_required` - Decorator pikeun admin-only views

### 2. Patients Module (`patients/`)

**Tanggung jawab**: Patient data management, medical records

```
patients/
├── models.py          # Patient model
├── views.py           # Patient CRUD, statistics
├── forms.py           # Patient forms
├── urls.py            # URL routing
├── services.py        # Patient services
├── tests.py           # Unit tests
└── templates/
    └── patients/
        ├── patient_list.html
        ├── patient_form.html
        └── patient_detail.html
```

**Key Components**:
- `Patient` - Patient model kalayan medical data
- Age calculation property
- NIK validation

### 3. Doctors Module (`doctors/`)

**Tanggung jawab**: Doctor profiles, availability management

```
doctors/
├── models.py          # Doctor model
├── views.py           # Doctor CRUD, availability toggle
├── forms.py           # Doctor forms
├── urls.py            # URL routing
├── services.py        # Doctor services
├── tests.py           # Unit tests
└── templates/
    └── doctors/
        ├── doctor_list.html
        ├── doctor_form.html
        ├── doctor_detail.html
        └── doctor_dashboard.html
```

**Key Components**:
- `Doctor` - Doctor model kalayan specialization
- Availability toggle
- Consultation fee management

### 4. Appointments Module (`appointments/`)

**Tanggung jawab**: Appointment booking, scheduling, conflict detection

```
appointments/
├── models.py          # Appointment model
├── views.py           # Appointment CRUD, conflict validation
├── forms.py           # Appointment forms
├── urls.py            # URL routing
├── services.py        # Appointment services
├── tests.py           # Unit tests
└── templates/
    └── appointments/
        ├── appointment_list.html
        ├── appointment_form.html
        ├── appointment_detail.html
        └── doctor_schedule.html
```

**Key Components**:
- `Appointment` - Appointment model kalayan conflict detection
- Time conflict validation
- Priority system (normal, urgent, emergency)

### 5. Prescriptions Module (`prescriptions/`)

**Tanggung jawab**: Prescription management, medicine inventory

```
prescriptions/
├── models.py          # Prescription, Medicine, PrescriptionItem
├── views.py           # Prescription CRUD, medicine management
├── forms.py           # Prescription forms
├── urls.py            # URL routing
├── services.py        # Prescription services
├── tests.py           # Unit tests
└── templates/
    └── prescriptions/
        ├── prescription_list.html
        ├── prescription_form.html
        ├── prescription_detail.html
        └── medicine_list.html
```

**Key Components**:
- `Prescription` - Prescription model kalayan status tracking
- `Medicine` - Medicine inventory management
- `PrescriptionItem` - Prescription items kalayan dosage info

### 6. Billing Module (`billing/`)

**Tanggung jawab**: Invoice management, payment processing

```
billing/
├── models.py          # Invoice, InvoiceItem, Payment
├── views.py           # Invoice CRUD, payment processing
├── forms.py           # Invoice forms
├── urls.py            # URL routing
├── services.py        # Billing services
├── tests.py           # Unit tests
└── templates/
    └── billing/
        ├── invoice_list.html
        ├── invoice_form.html
        ├── invoice_detail.html
        └── payment_list.html
```

**Key Components**:
- `Invoice` - Invoice model kalayan auto-calculation
- `InvoiceItem` - Invoice items kalayan quantity * price
- `Payment` - Payment tracking

### 7. Reports Module (`reports/`)

**Tanggung jawab**: Analytics, statistics, reporting

```
reports/
├── models.py          # Report models (if any)
├── views.py           # Report generation, statistics
├── urls.py            # URL routing
├── services.py        # Report services
├── tests.py           # Unit tests
└── templates/
    └── reports/
        ├── dashboard.html
        ├── revenue_report.html
        └── patient_report.html
```

**Key Components**:
- Revenue analytics
- Patient statistics
- Appointment analytics
- Prescription analytics

### 8. API Module (`api/`)

**Tanggung jawab**: REST API endpoints, serialization

```
api/
├── serializers.py     # DRF serializers
├── views.py           # API views
├── urls.py            # API URL routing
├── permissions.py     # API permissions
├── throttling.py      # Rate limiting
├── tests.py           # API tests
└── authentication.py  # Custom authentication
```

**Key Components**:
- JWT authentication
- Role-based permissions
- Rate limiting
- API versioning

## 🗄️ Database Schema

### Entity Relationship Diagram

```
┌─────────────────┐     ┌─────────────────┐
│  CustomUser     │     │    Patient      │
├─────────────────┤     ├─────────────────┤
│ id (PK)         │     │ id (PK)         │
│ username        │◄────│ user_id (FK)    │
│ email           │     │ nik             │
│ role            │     │ date_of_birth   │
│ password        │     │ gender          │
│ is_active       │     │ address         │
│ created_at      │     │ phone           │
└─────────────────┘     │ blood_type      │
                        └─────────────────┘
                                │
                                │
                        ┌─────────────────┐
                        │  Appointment    │
                        ├─────────────────┤
                        │ id (PK)         │
                        │ patient_id (FK) │◄──┐
                        │ doctor_id (FK)  │   │
                        │ appointment_date│   │
                        │ appointment_time│   │
                        │ status          │   │
                        │ priority        │   │
                        │ reason          │   │
                        │ notes           │   │
                        └─────────────────┘   │
                                │             │
                                │             │
                        ┌─────────────────┐   │
                        │   Prescription  │   │
                        ├─────────────────┤   │
                        │ id (PK)         │   │
                        │ appointment_id  │───┘
                        │ diagnosis       │
                        │ treatment_notes │
                        │ status          │
                        │ created_at      │
                        └─────────────────┘
                                │
                                │
                        ┌─────────────────┐
                        │ PrescriptionItem│
                        ├─────────────────┤
                        │ id (PK)         │
                        │ prescription_id │
                        │ medicine_id (FK)│
                        │ dosage          │
                        │ frequency       │
                        │ duration        │
                        │ quantity        │
                        └─────────────────┘
                                │
                                │
                        ┌─────────────────┐
                        │    Medicine     │
                        ├─────────────────┤
                        │ id (PK)         │
                        │ name            │
                        │ generic_name    │
                        │ form            │
                        │ manufacturer    │
                        │ unit            │
                        │ price           │
                        │ stock           │
                        │ expiry_date     │
                        │ is_active       │
                        └─────────────────┘
```

## 🔒 Security Architecture

### Authentication Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Client  │────▶│  Login API   │────▶│  Auth Service│
└──────────┘     └──────────────┘     └──────────────┘
                      │                       │
                      │                       ▼
                      │              ┌──────────────┐
                      │              │  JWT Token   │
                      │              │  Generation  │
                      │              └──────────────┘
                      │                       │
                      ▼                       ▼
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Client  │◀────│  Token       │◀────│  Token       │
│  Store   │     │  Response    │     │  Validation  │
└──────────┘     └──────────────┘     └──────────────┘
```

### Authorization Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Request │────▶│  Middleware  │────▶│  Permission  │
│  (JWT)   │     │  (JWT Auth)  │     │  Check       │
└──────────┘     └──────────────┘     └──────────────┘
                      │                       │
                      │                       ▼
                      │              ┌──────────────┐
                      │              │  Role-Based  │
                      │              │  Access      │
                      │              │  Control     │
                      │              └──────────────┘
                      │                       │
                      ▼                       ▼
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Response│◀────│  Response    │◀────│  Access      │
│  (Data)  │     │  (JSON)      │     │  Decision    │
└──────────┘     └──────────────┘     └──────────────┘
```

## 🚀 Performance Optimization

### Database Optimization

- **Indexing**: Strategic indexes on frequently queried fields
- **Query Optimization**: Use `select_related` jeung `prefetch_related`
- **Caching**: Redis caching pikeun statistics
- **Connection Pooling**: PostgreSQL connection pooling

### Frontend Optimization

- **Static Files**: WhiteNoise pikeun static file serving
- **CDN**: Bootstrap CDN pikeun library files
- **Lazy Loading**: Chart.js lazy loading
- **Minification**: CSS/JS minification

### API Optimization

- **Pagination**: Large datasets paginated
- **Filtering**: Query parameters pikeun filtering
- **Serialization**: Optimized DRF serializers
- **Rate Limiting**: Prevent abuse

## 📊 Monitoring & Logging

### Logging Strategy

```python
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### Monitoring Metrics

- **Application**: Response time, error rate
- **Database**: Query performance, connection count
- **Server**: CPU, memory, disk usage
- **Business**: User activity, revenue, appointments

## 🔄 Deployment Architecture

### Development

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Dev     │────▶│  Django      │────▶│  SQLite      │
│  Server  │     │  Runserver   │     │  Database    │
└──────────┘     └──────────────┘     └──────────────┘
```

### Production

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Client  │────▶│  Nginx       │────▶│  Gunicorn    │
│  (HTTPS) │     │  (Reverse    │     │  (WSGI       │
│          │     │   Proxy)     │     │   Server)    │
└──────────┘     └──────────────┘     └──────────────┘
                                          │
                                          ▼
                                   ┌──────────────┐
                                   │  PostgreSQL  │
                                   │  Database    │
                                   └──────────────┘
```

## 📚 Dokumentasi Tambahan

- [Installation Guide](INSTALL.md)
- [Deployment Guide](DEPLOY.md)
- [API Documentation](API.md)
- [README](README.md)
