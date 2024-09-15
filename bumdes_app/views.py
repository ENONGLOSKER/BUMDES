from django.shortcuts import render, get_object_or_404, redirect

from django.db import models
from .models import Transaksi, Pesan
from .forms import TransaksiForm
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from datetime import datetime
# perbaikan
from django.db.models import Sum, Case, When, F, DecimalField, IntegerField
from django.core.paginator import Paginator


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

def signin_form(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Sign in berhasil, selamat datang {user.username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Sign in gagal, silakan coba kembali!")
        else:
            messages.error(request, "Username dan password harus diisi!")

        return redirect('login')
    
    if request.user.is_authenticated:
        return redirect('dashboard')
    
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

# fungsi untuk kalkulasi trasaksi masuk, keluar dan saldo
def calculate_totals():
    # Gunakan Conditional Aggregation untuk menghitung total 'masuk' dan 'keluar' dalam satu query
    transaksi_aggregate = Transaksi.objects.aggregate(
        total_masuk=Sum(
            Case(
                When(jenis='masuk', then='jumlah'),
                default=0,
                output_field=IntegerField()
            )
        ),
        total_keluar=Sum(
            Case(
                When(jenis='keluar', then='jumlah'),
                default=0,
                output_field=IntegerField()
            )
        )
    )

    total_masuk = transaksi_aggregate['total_masuk'] or 0
    total_keluar = transaksi_aggregate['total_keluar'] or 0

    # Hitung saldo
    saldo = total_masuk - total_keluar

    return total_masuk, total_keluar, saldo

@login_required 
def dashboard(request):
    # total_masuk = Transaksi.objects.filter(jenis='masuk').aggregate(total=models.Sum('jumlah'))['total'] or 0
    # total_keluar = Transaksi.objects.filter(jenis='keluar').aggregate(total=models.Sum('jumlah'))['total'] or 0
    # saldo = total_masuk - total_keluar

    # Gabungkan query untuk menghitung total masuk dan keluar dalam satu langkah
    total = Transaksi.objects.aggregate(
        total_masuk=Sum(
            Case(
                When(jenis='masuk', then=F('jumlah')),
                default=0,
                output_field=DecimalField()  # Tentukan output_field sebagai DecimalField
            )
        ),
        total_keluar=Sum(
            Case(
                When(jenis='keluar', then=F('jumlah')),
                default=0,
                output_field=DecimalField()  # Tentukan output_field sebagai DecimalField
            )
        )
    )

    total_masuk = total['total_masuk'] or 0
    total_keluar = total['total_keluar'] or 0

    # Hitung saldo
    saldo = total_masuk - total_keluar

    context = {
        'saldo': saldo,
        'masuk': total_masuk,
        'keluar': total_keluar,
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
    # Ambil semua transaksi
    transaksi_list = Transaksi.objects.all().order_by('-tanggal')

    # Pagination
    paginator = Paginator(transaksi_list, 5)  # Tampilkan 10 transaksi per halaman
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Hitung total uang masuk dan keluar
    transaksi_aggregate = Transaksi.objects.aggregate(
        total_masuk=Sum(
            Case(
                When(jenis='masuk', then='jumlah'),
                default=0,
                output_field=IntegerField()
            )
        ),
        total_keluar=Sum(
            Case(
                When(jenis='keluar', then='jumlah'),
                default=0,
                output_field=IntegerField()
            )
        )
    )

    total_masuk = transaksi_aggregate['total_masuk'] or 0
    total_keluar = transaksi_aggregate['total_keluar'] or 0

    # Hitung saldo
    saldo = total_masuk - total_keluar

    return render(request, 'dashboard_transaksi.html', {
        'page_obj': page_obj,
        'saldo': saldo,
        'total_masuk': total_masuk,
        'total_keluar': total_keluar
    })

@login_required
def transaksi_masuk(request):
    total_masuk, total_keluar, saldo = calculate_totals()

    transaksi_list = Transaksi.objects.filter(jenis='masuk')
    
    paginator = Paginator(transaksi_list,5)  # Tampilkan 10 transaksi per halaman
    page_number = request.GET.get('page')
    transaksi = paginator.get_page(page_number)

    return render(request, 'dashboard_transaksi_masuk.html', {
        'transaksi': transaksi,
        'saldo': saldo,
        'total_masuk': total_masuk,
        'total_keluar': total_keluar
    })

@login_required
def transaksi_keluar(request):
    total_masuk, total_keluar, saldo = calculate_totals()

    transaksi_list = Transaksi.objects.filter(jenis='keluar')
    
    paginator = Paginator(transaksi_list, 5)  # Tampilkan 10 transaksi per halaman
    page_number = request.GET.get('page')
    transaksi = paginator.get_page(page_number)

    return render(request, 'dashboard_transaksi_keluar.html', {
        'transaksi': transaksi,
        'saldo': saldo,
        'total_masuk': total_masuk,
        'total_keluar': total_keluar
    })

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

@login_required
def laporan(request):
    total_masuk, total_keluar, saldo = calculate_totals()

    # Query untuk mengambil semua transaksi, diurutkan berdasarkan jenis
    transaksi_list = Transaksi.objects.order_by('-jenis')

    # Pagination
    paginator = Paginator(transaksi_list, 5)  # Tampilkan 10 transaksi per halaman
    page_number = request.GET.get('page')
    transaksi = paginator.get_page(page_number)

    # Ambil semua tanggal unik dari transaksi dengan optimasi
    tanggal_list = Transaksi.objects.values_list('tanggal', flat=True).distinct().order_by('tanggal')

    return render(request, 'dashboard_laporan.html', {
        'transaksi': transaksi,
        'saldo': saldo,
        'total_masuk': total_masuk,
        'total_keluar': total_keluar,
        'tanggal_list': tanggal_list
    })

@login_required
def cetak_laporan_by_tanggal(request):
    tanggal_mulai = request.GET.get('tanggal_mulai')
    tanggal_selesai = request.GET.get('tanggal_selesai')
    jenis = request.GET.get('jenis')

    if tanggal_mulai and tanggal_selesai:
        # Filter transaksi berdasarkan rentang tanggal
        transaksi = Transaksi.objects.filter(tanggal__range=[tanggal_mulai, tanggal_selesai]).order_by('tanggal')

        if jenis:
            transaksi = transaksi.filter(jenis=jenis)

        # Calculate total uang masuk and keluar untuk rentang tanggal yang dipilih
        total_masuk = transaksi.filter(jenis='masuk').aggregate(total=Sum('jumlah'))['total'] or 0
        total_keluar = transaksi.filter(jenis='keluar').aggregate(total=Sum('jumlah'))['total'] or 0

        # Calculate saldo untuk rentang tanggal yang dipilih
        saldo = total_masuk - total_keluar

        # Calculate total transaksi (masuk + keluar)
        total_transaksi = total_masuk + total_keluar

        tanggal_mulai_date = datetime.strptime(tanggal_mulai, '%Y-%m-%d')
        tanggal_selesai_date = datetime.strptime(tanggal_selesai, '%Y-%m-%d')
        
        # Format dates to the desired format
        formatted_tanggal_mulai = tanggal_mulai_date.strftime('%d %B %Y')
        formatted_tanggal_selesai = tanggal_selesai_date.strftime('%d %B %Y')
        

        return render(request, 'laporan_cetak_bytanggal.html', {
            'transaksi': transaksi,
            'saldo': saldo,
            'total_masuk': total_masuk,
            'total_keluar': total_keluar,
            'total_transaksi': total_transaksi,
            'tanggal_mulai': formatted_tanggal_mulai,
            'tanggal_selesai': formatted_tanggal_selesai,
        })
    else:
        return render(request, 'laporan_cetak_bytanggal.html', {'error': 'Tanggal mulai atau tanggal selesai tidak valid.'})
    
@login_required
def cetak_laporan(request): 
    # Calculate total uang masuk and keluar
    total_masuk = Transaksi.objects.filter(jenis='masuk').aggregate(total=Sum('jumlah'))['total'] or 0
    total_keluar = Transaksi.objects.filter(jenis='keluar').aggregate(total=Sum('jumlah'))['total'] or 0

    # Calculate saldo
    saldo = total_masuk - total_keluar

    transaksi = Transaksi.objects.order_by('-jenis')

    # Ambil semua tanggal unik dari transaksi
    tanggal_list = Transaksi.objects.values_list('tanggal', flat=True).distinct().order_by('tanggal')

    return render(request, 'laporan_cetak.html', {'transaksi': transaksi, 'saldo': saldo, 'total_masuk': total_masuk, 'total_keluar': total_keluar, 'tanggal_list': tanggal_list })

