"""
URL configuration for bumdes_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from bumdes_app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    path('login/', views.sigin_form, name='login'),
    path('logout/', views.signout_form, name='logout'),

    path('pesan/kirim/', views.kirim_pesan, name='kirim_pesan'),
    path('pesan/', views.pesan, name='pesan'),
    path('pesan/<int:id>/', views.hapus_pesan, name='hapus_pesan'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('laporan/', views.laporan, name='laporan'),
    path('laporan/cetak/', views.cetak_laporan, name='cetak_laporan'),

    path('transaksi/masuk/', views.transaksi_masuk, name='transaksi_masuk'),
    path('transaksi/keluar/', views.transaksi_keluar, name='transaksi_keluar'),

    path('transaksi/', views.transaksi_list, name='transaksi_list'),
    path('transaksi/create/', views.transaksi_create, name='transaksi_create'),
    path('transaksi/<int:id>/update/', views.transaksi_update, name='transaksi_update'),
    path('transaksi/<int:id>/delete/', views.transaksi_delete, name='transaksi_delete'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
