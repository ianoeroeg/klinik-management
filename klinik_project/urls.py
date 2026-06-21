from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as accounts_views
from patients import views as patients_views
from doctors import views as doctors_views
from appointments import views as appointments_views
from prescriptions import views as prescriptions_views
from billing import views as billing_views
from reports import views as reports_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', accounts_views.home_view, name='home'),
    path('login/', accounts_views.user_login, name='login'),
    path('logout/', accounts_views.user_logout, name='logout'),
    path('dashboard/', accounts_views.dashboard, name='dashboard'),
    path('users/', accounts_views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', accounts_views.UserDetailView.as_view(), name='user_detail'),
    path('users/new/', accounts_views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', accounts_views.UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', accounts_views.user_delete, name='user_delete'),
    path('users/<int:pk>/toggle-status/', accounts_views.user_toggle_status, name='user_toggle_status'),
    path('users/export-csv/', accounts_views.export_users_csv, name='export_users_csv'),
    path('change-password/', accounts_views.change_password, name='change_password'),
    path('patients/', patients_views.patient_list, name='patient_list'),
    path('patients/<int:pk>/', patients_views.patient_detail, name='patient_detail'),
    path('patients/<int:pk>/portal/', patients_views.patient_portal, name='patient_portal'),
    path('patients/new/', patients_views.patient_create, name='patient_create'),
    path('patients/<int:pk>/edit/', patients_views.patient_update, name='patient_edit'),
    path('doctors/', doctors_views.doctor_list, name='doctor_list'),
    path('doctors/<int:pk>/', doctors_views.doctor_detail, name='doctor_detail'),
    path('doctors/<int:pk>/dashboard/', doctors_views.doctor_dashboard, name='doctor_dashboard'),
    path('doctors/<int:pk>/toggle-availability/', doctors_views.doctor_toggle_availability, name='doctor_toggle_availability'),
    path('appointments/', appointments_views.appointment_list, name='appointment_list'),
    path('appointments/<int:pk>/', appointments_views.appointment_detail, name='appointment_detail'),
    path('appointments/new/', appointments_views.appointment_create, name='appointment_create'),
    path('appointments/new/patient/', appointments_views.patient_portal_appointment_create, name='patient_portal_appointment_create'),
    path('appointments/<int:pk>/edit/', appointments_views.appointment_update, name='appointment_edit'),
    path('appointments/<int:pk>/delete/', appointments_views.appointment_delete, name='appointment_delete'),
    path('prescriptions/medicines/', prescriptions_views.medicine_list, name='medicine_list'),
    path('prescriptions/medicines/<int:pk>/', prescriptions_views.medicine_detail, name='medicine_detail'),
    path('prescriptions/', prescriptions_views.prescription_list, name='prescription_list'),
    path('prescriptions/<int:pk>/', prescriptions_views.prescription_detail, name='prescription_detail'),
    path('prescriptions/new/', prescriptions_views.prescription_create, name='prescription_create'),
    path('prescriptions/<int:pk>/edit/', prescriptions_views.prescription_update, name='prescription_edit'),
    path('billing/invoices/', billing_views.invoice_list, name='invoice_list'),
    path('billing/invoices/<int:pk>/', billing_views.invoice_detail, name='invoice_detail'),
    path('billing/invoices/<int:pk>/pay/', billing_views.payment_create, name='payment_create'),
    path('billing/payments/', billing_views.payment_list, name='payment_list'),
    path('reports/dashboard/', reports_views.dashboard, name='report'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
