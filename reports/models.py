from django.db import models


class VisitReport(models.Model):
    """Laporan kunjungan pasien."""

    report_date_start = models.DateField(verbose_name='Tanggal Mimiti')
    report_date_end = models.DateField(verbose_name='Tanggal Akhir')
    total_visits = models.PositiveIntegerField(default=0, verbose_name='Total Kunjungan')
    completed_visits = models.PositiveIntegerField(default=0, verbose_name='Kunjungan Réngsé')
    cancelled_visits = models.PositiveIntegerField(default=0, verbose_name='Kunjungan Dibatalkun')
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Total Pendapatan (Rp)')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reports_visit_report'
        verbose_name = 'Laporan Kunjungan'
        verbose_name_plural = 'Laporan-laporan Kunjungan'
        ordering = ['-report_date_end']

    def __str__(self):
        return f"Laporan {self.report_date_start} s.d. {self.report_date_end}"


class DoctorPerformance(models.Model):
    """Kinerja dokter."""

    doctor = models.ForeignKey(
        'doctors.Doctor',
        on_delete=models.CASCADE,
        related_name='performance_reports',
        verbose_name='Dokter'
    )
    report_month = models.DateField(verbose_name='Bulan Laporan')
    total_appointments = models.PositiveIntegerField(default=0, verbose_name='Total Appointment')
    completed_appointments = models.PositiveIntegerField(default=0, verbose_name='Appointment Réngsé')
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Total Pendapatan (Rp)')
    patient_satisfaction = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        verbose_name='Kepuasan Pasien (1-5)'
    )

    class Meta:
        db_table = 'reports_doctor_performance'
        verbose_name = 'Kinerja Dokter'
        verbose_name_plural = 'Kinerja-kinerja Dokter'
        unique_together = ['doctor', 'report_month']
        ordering = ['-report_month']

    def __str__(self):
        return f"Kinerja Dr. {self.doctor} - {self.report_month.strftime('%B %Y')}"
