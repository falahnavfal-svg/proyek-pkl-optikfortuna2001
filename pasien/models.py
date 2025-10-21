from django.db import models
from django.utils import timezone

class Pelanggan(models.Model):
    nama = models.CharField(max_length=100)
    no_hp = models.CharField(max_length=20, unique=True)
    
    alamat = models.TextField(blank=True, null=True)
    tanggal_lahir = models.DateField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nama} ({self.no_hp})"

    class Meta:
        verbose_name = "Data Pelanggan"
        verbose_name_plural = "Data Pelanggan"

class Resep(models.Model):
    
    JENIS_LENSA_CHOICES = [
        ('SV', 'Single Vision'),
        ('BF', 'Bifokal'),
        ('PG', 'Progresif'),
        ('OFF', 'Office / Baca'),
        ('LAIN', 'Lainnya'),
    ]
    COATING_LENSA_CHOICES = [
        ('CRMC', 'CRMC (Standard)'),
        ('BLR', 'Blueray'),
        ('PHC', 'Photochromic'),
        ('BLC', 'Bluechromic (Blueray + Photochromic)'),
        ('LAIN', 'Lainnya'),
    ]
    INDEKS_LENSA_CHOICES = [
        ('1.56', '1.56'),
        ('1.60', '1.60'),
        ('1.67', '1.67'),
        ('1.74', '1.74'),
        ('LAIN', 'Lainnya (misal: 1.50, 1.59)'),
    ]
    
  
    pelanggan = models.ForeignKey(Pelanggan, on_delete=models.CASCADE, related_name='resep_history')
    tanggal_periksa = models.DateField(default=timezone.now)
    
    jenis_lensa = models.CharField(
        "Jenis Lensa", max_length=5, choices=JENIS_LENSA_CHOICES, default='SV'
    )

    jenis_coating = models.CharField(
        "Jenis Coating/Bahan",
        max_length=5,
        choices=COATING_LENSA_CHOICES,
        default='CRMC'
    )

    indeks_lensa = models.CharField(
        "Indeks Lensa",
        max_length=5,
        choices=INDEKS_LENSA_CHOICES,
        default='1.56'
    )
    
    harga_frame = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    harga_lensa = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    diskon = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    total_bayar = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    lunas = models.BooleanField(default=True)
    total_bayar = models.DecimalField(
        "Total Bayar (Rp)", 
        max_digits=10, 
        decimal_places=0, 
        default=0, 
        editable=False )

    # Mata Kanan (OD)
    od_sph = models.CharField("SPH (Kanan)", max_length=10, default='Plano')
    od_cyl = models.CharField("CYL (Kanan)", max_length=10, default='-')
    od_axis = models.CharField("AXIS (Kanan)", max_length=10, default='-')
    od_add = models.CharField("ADD (Kanan)", max_length=10, default='-')

    # Mata Kiri (OS)
    os_sph = models.CharField("SPH (Kiri)", max_length=10, default='Plano')
    os_cyl = models.CharField("CYL (Kiri)", max_length=10, default='-')
    os_axis = models.CharField("AXIS (Kiri)", max_length=10, default='-')
    os_add = models.CharField("ADD (Kiri)", max_length=10, default='-')

    pd = models.CharField("PD (Pupil Distance)", max_length=10, blank=True, null=True)

    catatan = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):

        self.total_bayar = (self.harga_frame + self.harga_lensa) - self.diskon

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Resep {self.pelanggan.nama} [{self.tanggal_periksa}]"

    class Meta:
        ordering = ['-tanggal_periksa'] 
        verbose_name = "Data Resep"
        verbose_name_plural = "Data Resep"
