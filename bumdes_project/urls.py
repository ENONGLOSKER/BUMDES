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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from bumdes_app import views
urlpatterns = [
    # tes
    path('__debug__/', include('debug_toolbar.urls')),

    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    path('login/', views.signin_form, name='login'),
    path('logout/', views.signout_form, name='logout'),

    path('pesan/kirim/', views.kirim_pesan, name='kirim_pesan'),
    path('pesan/', views.pesan, name='pesan'),
    path('pesan/<int:id>/', views.hapus_pesan, name='hapus_pesan'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('laporan/', views.laporan, name='laporan'),
    path('laporan/cetak/', views.cetak_laporan, name='cetak_laporan'),
    path('cetak_laporan_by_tanggal/', views.cetak_laporan_by_tanggal, name='cetak_laporan_by_tanggal'),

    path('transaksi/masuk/', views.transaksi_masuk, name='transaksi_masuk'),
    path('transaksi/keluar/', views.transaksi_keluar, name='transaksi_keluar'),

    path('transaksi/', views.transaksi_list, name='transaksi_list'),
    path('transaksi/create/', views.transaksi_create, name='transaksi_create'),
    path('transaksi/<int:id>/update/', views.transaksi_update, name='transaksi_update'),
    path('transaksi/<int:id>/delete/', views.transaksi_delete, name='transaksi_delete'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
