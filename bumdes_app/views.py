from django.shortcuts import render, get_object_or_404, redirect

from django.db import models
from .models import Transaksi, Pesan
from .forms import TransaksiForm
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

def index(request):
    data = Transaksi.objects.order_by('-id')
    # Calculate total uang masuk and keluar
    total_masuk = Transaksi.objects.filter(jenis='masuk').aggregate(total=models.Sum('jumlah'))['total'] or 0
    total_keluar = Transaksi.objects.filter(jenis='keluar').aggregate(total=models.Sum('jumlah'))['total'] or 0

    # Calculate saldo
    saldo = total_masuk - total_keluar

    context = {
        'datas': data,
        'masuk': total_masuk,
        'keluar': total_keluar,
        'saldo': saldo,
    }
    return render(request, 'index.html', context)

def signout_form(request):
    logout(request)
    return redirect('index')

def sigin_form(request):
    
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Sign in Berhasil, Selamat datang {user}")
            return redirect('dashboard')
        else:
            messages.error(request, "Sign in Gagal, Silahkan coba kembali!")
            return redirect('login')
        
    # if request.user.is_authenticated:
    #     return redirect('dashboard')

    return render(request, 'login.html')

def kirim_pesan(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pesan = request.POST.get('pesan')
        Pesan.objects.create(email=email, pesan=pesan)
        messages.success(request, 'Pesan berhasil disampaikan!')
        return redirect('index')
    return render(request, 'index.html')

def hapus_pesan(request, id):
    pesan = get_object_or_404(Pesan, id=id)
    pesan.delete()
    return redirect('pesan')

def pesan(request):
    datas = Pesan.objects.all().order_by('-id')
    return render(request, 'dashboard_pesan.html', {'datas':datas})

@login_required
def dashboard(request):
    total_masuk = Transaksi.objects.filter(jenis='masuk').aggregate(total=models.Sum('jumlah'))['total'] or 0
    total_keluar = Transaksi.objects.filter(jenis='keluar').aggregate(total=models.Sum('jumlah'))['total'] or 0

    # Calculate saldo
    saldo = total_masuk - total_keluar

    context = {
        'saldo': saldo,
        'masuk': total_masuk,
        'keluar':total_keluar,
    }
    return render(request, 'dashboard.html', context)


@login_required
def transaksi_create(request):
    if request.method == 'POST':
        form = TransaksiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaksi_list')
    else:
        form = TransaksiForm()
    return render(request, 'dashboard_form.html', {'form': form})

@login_required
def transaksi_list(request):
    transaksi = Transaksi.objects.all()
    
    # Calculate total uang masuk and keluar
    total_masuk = Transaksi.objects.filter(jenis='masuk').aggregate(total=models.Sum('jumlah'))['total'] or 0
    total_keluar = Transaksi.objects.filter(jenis='keluar').aggregate(total=models.Sum('jumlah'))['total'] or 0

    # Calculate saldo
    saldo = total_masuk - total_keluar
    
    return render(request, 'dashboard_transaksi.html', {'transaksi': transaksi, 'saldo': saldo})

@login_required
def transaksi_masuk(request):
    # Calculate total uang masuk and keluar
    total_masuk = Transaksi.objects.filter(jenis='masuk').aggregate(total=models.Sum('jumlah'))['total'] or 0
    total_keluar = Transaksi.objects.filter(jenis='keluar').aggregate(total=models.Sum('jumlah'))['total'] or 0

    # Calculate saldo
    saldo = total_masuk - total_keluar
    
    transaksi = Transaksi.objects.filter(jenis='masuk')

    return render(request, 'dashboard_transaksi_masuk.html', {'transaksi': transaksi, 'saldo': saldo})

@login_required
def transaksi_keluar(request):
    # Calculate total uang masuk and keluar
    total_masuk = Transaksi.objects.filter(jenis='masuk').aggregate(total=models.Sum('jumlah'))['total'] or 0
    total_keluar = Transaksi.objects.filter(jenis='keluar').aggregate(total=models.Sum('jumlah'))['total'] or 0

    # Calculate saldo
    saldo = total_masuk - total_keluar

    transaksi = Transaksi.objects.filter(jenis='keluar')

    return render(request, 'dashboard_transaksi_keluar.html', {'transaksi': transaksi, 'saldo': saldo})

@login_required
def laporan(request):
    # Calculate total uang masuk and keluar
    total_masuk = Transaksi.objects.filter(jenis='masuk').aggregate(total=models.Sum('jumlah'))['total'] or 0
    total_keluar = Transaksi.objects.filter(jenis='keluar').aggregate(total=models.Sum('jumlah'))['total'] or 0

    # Calculate saldo
    saldo = total_masuk - total_keluar

    transaksi = Transaksi.objects.order_by('-jenis')

    return render(request, 'dashboard_laporan.html', {'transaksi': transaksi, 'saldo': saldo, 'total_masuk':total_masuk, 'total_keluar':total_keluar })

@login_required
def cetak_laporan(request):
    # Calculate total uang masuk and keluar
    total_masuk = Transaksi.objects.filter(jenis='masuk').aggregate(total=models.Sum('jumlah'))['total'] or 0
    total_keluar = Transaksi.objects.filter(jenis='keluar').aggregate(total=models.Sum('jumlah'))['total'] or 0

    # Calculate saldo
    saldo = total_masuk - total_keluar

    transaksi = Transaksi.objects.order_by('-jenis')

    return render(request, 'laporan_cetak.html', {'transaksi': transaksi, 'saldo': saldo, 'total_masuk':total_masuk, 'total_keluar':total_keluar })

@login_required
def transaksi_update(request, id):
    transaksi = get_object_or_404(Transaksi, id=id)
    if request.method == 'POST':
        form = TransaksiForm(request.POST, instance=transaksi)
        if form.is_valid():
            form.save()
            return redirect('transaksi_list')
    else:
        form = TransaksiForm(instance=transaksi)
    return render(request, 'dashboard_form.html', {'form': form})

@login_required
def transaksi_delete(request, id):
    transaksi = get_object_or_404(Transaksi, id=id)
    transaksi.delete()
    return redirect('transaksi_list')
