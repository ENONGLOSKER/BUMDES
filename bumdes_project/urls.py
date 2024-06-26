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
    path('transaksi/', views.transaksi_list, name='transaksi_list'),
    path('transaksi/create/', views.transaksi_create, name='transaksi_create'),
    path('transaksi/<int:pk>/', views.transaksi_detail, name='transaksi_detail'),
    path('transaksi/<int:pk>/update/', views.transaksi_update, name='transaksi_update'),
    path('transaksi/<int:pk>/delete/', views.transaksi_delete, name='transaksi_delete'),
    # laporan
    path('laporan/', views.laporan_list, name='laporan_list'),
    path('laporan/create/', views.laporan_create, name='laporan_create'),
    path('laporan/<int:pk>/', views.laporan_detail, name='laporan_detail'),
    path('laporan/<int:pk>/update/', views.laporan_update, name='laporan_update'),
    path('laporan/<int:pk>/delete/', views.laporan_delete, name='laporan_delete'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
