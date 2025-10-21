from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, Max
from datetime import date, timedelta
from .models import Pelanggan, Resep
from .forms import ResepForm, PelangganForm
from .forms import ResepForm 

@login_required 
def tambah_pelanggan(request):
    if request.method == 'POST':
        form = PelangganForm(request.POST)
        if form.is_valid():
            pelanggan_baru = form.save() 
            return redirect('detail', pk=pelanggan_baru.pk)
    else:
        form = PelangganForm() 
    context = {
        'form': form,
        'title': 'Form Pelanggan Baru' 
    }
    return render(request, 'tambah_pelanggan.html', {'form': form})
@login_required
def edit_pelanggan(request, pk):
    pelanggan = get_object_or_404(Pelanggan, pk=pk)

    if request.method == 'POST':
        form = PelangganForm(request.POST, instance=pelanggan)
        if form.is_valid():
            form.save() 
            return redirect('detail', pk=pelanggan.pk) 
    else:
        form = PelangganForm(instance=pelanggan)
        context = {
        'form': form,
        'title': 'Edit Data Pelanggan' 
    }
    return render(request, 'tambah_pelanggan.html', context)
@login_required 
def halaman_pencarian(request):
    query = request.GET.get('query', '') 
    
    if query:
        
        pelanggan_list_qs = Pelanggan.objects.filter(
            Q(nama__icontains=query) | Q(no_hp__icontains=query)
        )
        is_search_result = True
    else:
        
        pelanggan_list_qs = Pelanggan.objects.order_by('-created_at')[:5]
        is_search_result = False


    
    satu_tahun_lalu = date.today() - timedelta(days=365)


    pelanggan_list = pelanggan_list_qs.annotate(
            last_periksa=Max('resep_history__tanggal_periksa')
    )

    jumlah_pasien = Pelanggan.objects.count()

    
    resep_hari_ini_qs = Resep.objects.filter(tanggal_periksa=date.today())
    resep_hari_ini = resep_hari_ini_qs.count()


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



@login_required 
def detail_pelanggan(request, pk):
    pelanggan = get_object_or_404(Pelanggan, pk=pk)
    resep_list = pelanggan.resep_history.all() 
    
    
    if request.method == 'POST':

        form = ResepForm(request.POST)
        if form.is_valid():
            resep_baru = form.save(commit=False) 
            resep_baru.pelanggan = pelanggan      
            resep_baru.save()                     
            

            return redirect('detail', pk=pelanggan.pk)
    else:
        
        form = ResepForm() 

    context = {
        'pelanggan': pelanggan,
        'resep_list': resep_list,
        'form': form, e
    }
    return render(request, 'detail.html', context)
@login_required
def edit_resep(request, pk):

    resep = get_object_or_404(Resep, pk=pk)

    if request.method == 'POST':
        form = ResepForm(request.POST, instance=resep)
        if form.is_valid():
            form.save()
           
            return redirect('detail', pk=resep.pelanggan.pk)
    else:
        form = ResepForm(instance=resep)

    context = {
        'form': form,
        'resep': resep
    }
    return render(request, 'edit_resep.html', context)
