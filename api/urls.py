from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'patients', views.PatientViewSet, basename='patient')
router.register(r'doctors', views.DoctorViewSet, basename='doctor')
router.register(r'appointments', views.AppointmentViewSet, basename='appointment')
router.register(r'medicines', views.MedicineViewSet, basename='medicine')
router.register(r'prescriptions', views.PrescriptionViewSet, basename='prescription')
router.register(r'invoices', views.InvoiceViewSet, basename='invoice')
router.register(r'payments', views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]
