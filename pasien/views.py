# Di dalam file: pasien/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Max
from datetime import date, timedelta
from .models import Pelanggan, Resep
from .forms import ResepForm, PelangganForm
from .forms import ResepForm # Pastikan import ResepForm

#
# --- Halaman Pencarian (Halaman Utama) ---
#
@login_required # Kunci halaman ini
def tambah_pelanggan(request):
    if request.method == 'POST':
        # Jika user mengirim data (klik tombol Simpan)
        form = PelangganForm(request.POST)
        if form.is_valid():
            pelanggan_baru = form.save() # Simpan pelanggan baru
            # Arahkan user langsung ke halaman detail pelanggan baru
            return redirect('detail', pk=pelanggan_baru.pk)
    else:
        # Jika user baru membuka halaman (metode GET)
        form = PelangganForm() # Buat form kosong
    context = {
        'form': form,
        'title': 'Form Pelanggan Baru' 
    }
    # Tampilkan template 'tambah_pelanggan.html' dan kirim form-nya
    return render(request, 'tambah_pelanggan.html', {'form': form})
@login_required
def edit_pelanggan(request, pk):
    # Ambil data pelanggan yang mau di-edit
    pelanggan = get_object_or_404(Pelanggan, pk=pk)

    if request.method == 'POST':
        # 'instance=pelanggan' memberi tahu form data apa yang harus diperbarui
        form = PelangganForm(request.POST, instance=pelanggan)
        if form.is_valid():
            form.save() # Simpan perubahan
            return redirect('detail', pk=pelanggan.pk) # Kembali ke detail
    else:
        # 'instance=pelanggan' akan otomatis mengisi form dengan data lama
        form = PelangganForm(instance=pelanggan)
        context = {
        'form': form,
        'title': 'Edit Data Pelanggan' # (BARU) Kirim 'title'
    }
    return render(request, 'tambah_pelanggan.html', context)
@login_required # Kunci halaman ini
def halaman_pencarian(request):
    query = request.GET.get('query', '') 
    
    if query:
        # 1. Jika ada query, jalankan pencarian
        pelanggan_list_qs = Pelanggan.objects.filter(
            Q(nama__icontains=query) | Q(no_hp__icontains=query)
        )
        is_search_result = True
    else:
        # 2. Jika tidak ada query, tampilkan 5 pasien terbaru
        pelanggan_list_qs = Pelanggan.objects.order_by('-created_at')[:5]
        is_search_result = False
# --- (BARU) ANOTASI UNTUK FITUR JATUH TEMPO ---

    # 1. Tentukan tanggal 1 tahun lalu
    satu_tahun_lalu = date.today() - timedelta(days=365)

    # 2. "Tempeli" setiap pelanggan di queryset dengan tanggal resep terakhirnya
    # Ini akan membuat field baru bernama 'last_periksa'
    pelanggan_list = pelanggan_list_qs.annotate(
            last_periksa=Max('resep_history__tanggal_periksa')
    )
# 1. Total semua pasien
    jumlah_pasien = Pelanggan.objects.count()

    # 2. Resep yang dibuat hari ini
    resep_hari_ini_qs = Resep.objects.filter(tanggal_periksa=date.today())
    resep_hari_ini = resep_hari_ini_qs.count()

    # 3. Total penjualan hari ini
    # Kita pakai .aggregate() pada QuerySet resep hari ini
    total_penjualan_hari_ini = resep_hari_ini_qs.aggregate(
        total=Sum('total_bayar')
    )['total'] or 0
    context = {
        'pelanggan_list': pelanggan_list,
        'query': query,
        'is_search_result': is_search_result,
        'jumlah_pasien': jumlah_pasien,
        'resep_hari_ini': resep_hari_ini,
        'total_penjualan_hari_ini': total_penjualan_hari_ini,
        'satu_tahun_lalu': satu_tahun_lalu,
    }
    return render(request, 'search.html', context)

#
# --- Halaman Detail Pelanggan & Tambah Resep ---
#
@login_required # Kunci halaman ini
def detail_pelanggan(request, pk):
    pelanggan = get_object_or_404(Pelanggan, pk=pk)
    resep_list = pelanggan.resep_history.all() 
    
    # Logika Form Tambah Resep Baru
    if request.method == 'POST':
        # Jika user mengirim data (klik tombol Simpan)
        form = ResepForm(request.POST)
        if form.is_valid():
            resep_baru = form.save(commit=False) # Jangan simpan dulu
            resep_baru.pelanggan = pelanggan      # Isi 'pelanggan' secara manual
            resep_baru.save()                     # Baru simpan ke database
            
            # Redirect kembali ke halaman ini agar form bersih
            return redirect('detail', pk=pelanggan.pk)
    else:
        # Jika user baru membuka halaman (metode GET)
        form = ResepForm() # Buat form kosong

    context = {
        'pelanggan': pelanggan,
        'resep_list': resep_list,
        'form': form, # Kirim form (kosong atau terisi) ke template
    }
    return render(request, 'detail.html', context)
@login_required
def edit_resep(request, pk):
    # Ambil data resep yang mau di-edit
    resep = get_object_or_404(Resep, pk=pk)

    if request.method == 'POST':
        form = ResepForm(request.POST, instance=resep)
        if form.is_valid():
            form.save()
            # Kembali ke halaman detail pelanggan (induknya)
            return redirect('detail', pk=resep.pelanggan.pk)
    else:
        # Isi form dengan data resep yang lama
        form = ResepForm(instance=resep)

    context = {
        'form': form,
        'resep': resep # Kirim resep untuk konteks (misal: judul)
    }
    return render(request, 'edit_resep.html', context)