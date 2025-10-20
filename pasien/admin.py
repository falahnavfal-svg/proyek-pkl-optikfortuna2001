# Di dalam file: pasien/admin.py
from django.contrib import admin
from .models import Pelanggan, Resep

class ResepInline(admin.TabularInline):
    model = Resep
    extra = 1 # Tampilkan 1 form resep baru
    ordering = ('-tanggal_periksa',)

@admin.register(Pelanggan)
class PelangganAdmin(admin.ModelAdmin):
    list_display = ('nama', 'no_hp', 'tanggal_lahir')
    search_fields = ('nama', 'no_hp')
    inlines = [ResepInline] 

@admin.register(Resep)
class ResepAdmin(admin.ModelAdmin):
    list_display = ('pelanggan', 'tanggal_periksa', 'od_sph', 'os_sph')
    list_filter = ('tanggal_periksa',)
    search_fields = ('pelanggan__nama', 'pelanggan__no_hp')
    autocomplete_fields = ['pelanggan']