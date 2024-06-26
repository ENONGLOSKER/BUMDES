from django import forms
from .models import Transaksi, Laporan

class TransaksiForm(forms.ModelForm):
    class Meta:
        model = Transaksi
        fields = ['tanggal', 'jumlah', 'jenis', 'deskripsi', 'status']

class LaporanForm(forms.ModelForm):
    class Meta:
        model = Laporan
        fields = ['tanggal_mulai', 'tanggal_selesai']
