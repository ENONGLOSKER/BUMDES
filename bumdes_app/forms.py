from django import forms
from .models import Transaksi

class TransaksiForm(forms.ModelForm):
    class Meta:
        model = Transaksi
        fields = ['tanggal', 'jumlah', 'jenis', 'deskripsi']

        widgets = {
            'tanggal':forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'jumlah':forms.NumberInput(attrs={'class':'form-control'}),
            'jenis':forms.Select(attrs={'class':'form-control'}),
            'deskripsi':forms.Textarea(attrs={'class':'form-control'}),
            'status':forms.CheckboxInput(attrs={'class':'form-control'}),
        }
