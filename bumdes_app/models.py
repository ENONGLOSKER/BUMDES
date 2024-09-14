from django.db import models

class Transaksi(models.Model):
    JENIS_TRANSAKSI = [
        ('masuk', 'Uang Masuk'),
        ('keluar', 'Uang Keluar'),
    ]

    tanggal = models.DateField()
    jumlah = models.DecimalField(max_digits=10, decimal_places=2)
    jenis = models.CharField(max_length=10, choices=JENIS_TRANSAKSI)
    deskripsi = models.TextField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.tanggal} - {self.jenis} - {self.jumlah}'

class Pesan(models.Model):
    email = models.EmailField()
    pesan = models.TextField()
    dibuat_pada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pesaan dari {self.email}'
