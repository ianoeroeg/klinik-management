from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(*allowed_roles):
    """Decorator pikeun ngeureunkeun akses dumasar role.
    
    Contoh:
        @role_required('admin', 'staff')
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role not in allowed_roles:
                messages.warning(request, 'Anjeun teu gaduh izin pikeun aksés ieu halaman.')
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def admin_required(view_func):
    """Redirect non-admin ka dashboard."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.role != 'admin':
            messages.warning(request, 'Aksés ditolak. Mungkur admin.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def doctor_required(view_func):
    """Redirect non-dokter ka dashboard."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.role != 'dokter':
            messages.warning(request, 'Aksés ditolak. Mungkur dokter.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def patient_required(view_func):
    """Redirect non-pasien ka dashboard."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.role != 'pasien':
            messages.warning(request, 'Aksés ditolak. Mungkur pasien.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
