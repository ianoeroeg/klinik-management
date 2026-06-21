from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Sum, Count, Q
from datetime import date, timedelta, datetime
from calendar import month_name
from django.http import HttpResponse
import csv

from .models import CustomUser, PasswordResetToken
from .decorators import admin_required
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from prescriptions.models import Prescription
from billing.models import Invoice


def home_view(request):
    return render(request, 'accounts/home.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user.last_login_ip = request.META.get('REMOTE_ADDR')
            user.save(update_fields=['last_login_ip'])
            messages.success(request, 'Login berhasil!')
            return redirect('dashboard')
        messages.error(request, 'Username atawa password salah.')
    return render(request, 'accounts/login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logout berhasil!')
    return redirect('home')


@login_required
@admin_required
def dashboard(request):
    """Admin Dashboard with comprehensive statistics"""
    today = date.today()
    today_str = today.strftime('%Y-%m-%d')
    now = datetime.now()
    
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.filter(is_available=True).count()
    today_appointments = Appointment.objects.filter(appointment_date=today).count()
    today_revenue = Invoice.objects.filter(
        created_at__date=today,
        status='paid'
    ).aggregate(total=Sum('total'))['total'] or 0
    
    monthly_revenue = Invoice.objects.filter(
        created_at__month=today.month,
        created_at__year=today.year,
        status='paid'
    ).aggregate(total=Sum('total'))['total'] or 0
    
    current_month_name = month_name[today.month]
    
    patients_this_month = Patient.objects.filter(
        created_at__month=today.month,
        created_at__year=today.year
    ).count()
    
    prescriptions_today = Prescription.objects.filter(
        created_at__date=today
    ).count()
    
    total_prescriptions = Prescription.objects.count()
    
    available_doctors = Doctor.objects.filter(is_available=True).count()
    
    today_appointments_list = Appointment.objects.select_related(
        'patient', 'doctor'
    ).filter(appointment_date=today).order_by('appointment_time')
    
    recent_invoices = Invoice.objects.select_related('patient').order_by('-created_at')[:5]
    
    recent_patients = Patient.objects.order_by('-created_at')[:5]
    
    doctors = Doctor.objects.all()[:6]
    
    unpaid_invoices = Invoice.objects.filter(status='unpaid').order_by('-created_at')[:5]
    
    revenue_labels = []
    revenue_data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_str = day.strftime('%Y-%m-%d')
        day_revenue = Invoice.objects.filter(
            created_at__date=day,
            status='paid'
        ).aggregate(total=Sum('total'))['total'] or 0
        
        revenue_labels.append(day.strftime('%d %b'))
        revenue_data.append(int(day_revenue))
    
    context = {
        'now': now,
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'today_appointments': today_appointments,
        'today_revenue': today_revenue,
        'monthly_revenue': monthly_revenue,
        'current_month_name': current_month_name,
        'patients_this_month': patients_this_month,
        'prescriptions_today': prescriptions_today,
        'total_prescriptions': total_prescriptions,
        'available_doctors': available_doctors,
        'today_appointments_count': today_appointments,
        'today_appointments': today_appointments_list,
        'recent_invoices': recent_invoices,
        'recent_patients': recent_patients,
        'doctors': doctors,
        'unpaid_invoices': unpaid_invoices,
        'revenue_labels': revenue_labels,
        'revenue_data': revenue_data,
    }
    return render(request, 'accounts/dashboard.html', context)


class UserListView(ListView):
    model = CustomUser
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        qs = CustomUser.objects.all().order_by('-created_at')
        
        role = self.request.GET.get('role')
        if role:
            qs = qs.filter(role=role)
        
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_role'] = self.request.GET.get('role', '')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user'


class UserCreateView(CreateView):
    model = CustomUser
    template_name = 'accounts/user_form.html'
    fields = ['username', 'first_name', 'last_name', 'email', 'role', 'phone']
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        password = form.cleaned_data['password']
        user = form.save()
        user.set_password(password)
        user.save()
        messages.success(self.request, f"Pengguna {user.get_full_name() or user.username} berhasil ditambah.")
        return redirect(self.success_url)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class UserUpdateView(UpdateView):
    model = CustomUser
    template_name = 'accounts/user_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'avatar', 'role', 'is_active']
    success_url = reverse_lazy('user_list')


@admin_required
def user_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        username = user.get_full_name() or user.username
        user.delete()
        messages.success(request, f"Pengguna {username} berhasil dihapus.")
        return redirect('user_list')
    return render(request, 'accounts/user_confirm_delete.html', {'user': user})


@admin_required
def user_toggle_status(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        status = "diaktifkeun" if user.is_active else "dinonaktipkeun"
        messages.success(request, f"Pengguna {user.get_full_name() or user.username} berhasil {status}.")
        return redirect('user_detail', pk=pk)
    return redirect('user_detail', pk=pk)


@admin_required
def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Username', 'First Name', 'Last Name', 'Email', 'Role', 'Phone', 'Status', 'Created At'])
    
    users = CustomUser.objects.all().select_related('doctor_profile', 'patient_profile')
    for user in users:
        writer.writerow([
            user.username,
            user.first_name,
            user.last_name,
            user.email or '',
            user.get_role_display(),
            user.phone or '',
            'Aktif' if user.is_active else 'Teu Aktif',
            user.created_at.strftime('%Y-%m-%d %H:%M')
        ])
    
    return response


@login_required
def change_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request)
            messages.success(request, 'Password berhasil dirobah!')
            return redirect('dashboard')
        for error in form.errors.values():
            messages.error(request, error[0])
    else:
        form = SetPasswordForm(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})
