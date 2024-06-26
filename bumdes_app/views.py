from django.shortcuts import render, get_object_or_404, redirect
from .models import Transaksi, Laporan
from .forms import TransaksiForm, LaporanForm

# Create your views here.
def index(request):
    data = Transaksi.objects.all()
    context = {
        'datas': data,
    }
    return render(request, 'index.html', context)

# Create a new Transaksi
def transaksi_create(request):
    if request.method == 'POST':
        form = TransaksiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaksi_list')
    else:
        form = TransaksiForm()
    return render(request, 'transaksi_form.html', {'form': form})

# Retrieve a list of Transaksi
def transaksi_list(request):
    transaksi = Transaksi.objects.all()
    return render(request, 'transaksi_list.html', {'transaksi': transaksi})

# Retrieve a single Transaksi
def transaksi_detail(request, pk):
    transaksi = get_object_or_404(Transaksi, pk=pk)
    return render(request, 'transaksi_detail.html', {'transaksi': transaksi})

# Update an existing Transaksi
def transaksi_update(request, pk):
    transaksi = get_object_or_404(Transaksi, pk=pk)
    if request.method == 'POST':
        form = TransaksiForm(request.POST, instance=transaksi)
        if form.is_valid():
            form.save()
            return redirect('transaksi_detail', pk=pk)
    else:
        form = TransaksiForm(instance=transaksi)
    return render(request, 'transaksi_form.html', {'form': form})

# Delete an existing Transaksi
def transaksi_delete(request, pk):
    transaksi = get_object_or_404(Transaksi, pk=pk)
    if request.method == 'POST':
        transaksi.delete()
        return redirect('transaksi_list')
    return render(request, 'transaksi_confirm_delete.html', {'transaksi': transaksi})


# Create a new Laporan
def laporan_create(request):
    if request.method == 'POST':
        form = LaporanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('laporan_list')
    else:
        form = LaporanForm()
    return render(request, 'laporan_form.html', {'form': form})

# Retrieve a list of Laporan
def laporan_list(request):
    laporan = Laporan.objects.all()
    return render(request, 'laporan_list.html', {'laporan': laporan})

# Retrieve a single Laporan
def laporan_detail(request, pk):
    laporan = get_object_or_404(Laporan, pk=pk)
    return render(request, 'laporan_detail.html', {'laporan': laporan})

# Update an existing Laporan
def laporan_update(request, pk):
    laporan = get_object_or_404(Laporan, pk=pk)
    if request.method == 'POST':
        form = LaporanForm(request.POST, instance=laporan)
        if form.is_valid():
            form.save()
            return redirect('laporan_detail', pk=pk)
    else:
        form = LaporanForm(instance=laporan)
    return render(request, 'laporan_form.html', {'form': form})

# Delete an existing Laporan
def laporan_delete(request, pk):
    laporan = get_object_or_404(Laporan, pk=pk)
    if request.method == 'POST':
        laporan.delete()
        return redirect('laporan_list')
    return render(request, 'laporan_confirm_delete.html', {'laporan': laporan})
