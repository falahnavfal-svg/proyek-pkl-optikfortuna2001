# Di dalam file: pasien/forms.py
from django import forms
from .models import Resep, Pelanggan

class PelangganForm(forms.ModelForm):
    class Meta:
        model = Pelanggan
        # Tentukan field yang ingin ditampilkan di form
        fields = ['nama', 'no_hp']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'no_hp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: 0812...'}),
        }

        labels = {
            'nama': 'Nama Lengkap',
            'no_hp': 'Nomor HP (WA)',
        }
class ResepForm(forms.ModelForm):
    class Meta:
        model = Resep
        # Tentukan field apa saja yang ingin kita tampilkan di form
        # Kita buang 'pelanggan' karena akan diisi otomatis
        fields = [
            'tanggal_periksa', 
            'jenis_lensa', 
            'jenis_coating', 
            'indeks_lensa', 
            'od_sph', 'od_cyl', 'od_axis', 'od_add',
            'os_sph', 'os_cyl', 'os_axis', 'os_add',
            'pd', 'catatan',
            'harga_frame', 'harga_lensa', 'diskon', 'lunas'
        ]
        
        # (Bonus) Tambahkan widget agar 'tanggal_periksa' jadi kalender
        widgets = {
            'tanggal_periksa': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            # Tambahkan 'form-control' ke field lain agar rapi
            'jenis_lensa': forms.Select(attrs={'class': 'form-select'}),
            'jenis_coating': forms.Select(attrs={'class': 'form-select'}),
            'indeks_lensa': forms.Select(attrs={'class': 'form-select'}),
            'od_sph': forms.TextInput(attrs={'class': 'form-control'}),
            'od_cyl': forms.TextInput(attrs={'class': 'form-control'}),
            'od_axis': forms.TextInput(attrs={'class': 'form-control'}),
            'od_add': forms.TextInput(attrs={'class': 'form-control'}),
            'os_sph': forms.TextInput(attrs={'class': 'form-control'}),
            'os_cyl': forms.TextInput(attrs={'class': 'form-control'}),
            'os_axis': forms.TextInput(attrs={'class': 'form-control'}),
            'os_add': forms.TextInput(attrs={'class': 'form-control'}),
            'pd': forms.TextInput(attrs={'class': 'form-control'}),
            'catatan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            # --- (BARU) Tambahkan widget untuk field finansial ---
            'harga_frame': forms.NumberInput(attrs={'class': 'form-control'}),
            'harga_lensa': forms.NumberInput(attrs={'class': 'form-control'}),
            'diskon': forms.NumberInput(attrs={'class': 'form-control'}),
            'lunas': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }