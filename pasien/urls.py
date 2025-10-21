from django.urls import path
from . import views

urlpatterns = [
    path('', views.halaman_pencarian, name='search'),

    path('pelanggan/<int:pk>/', views.detail_pelanggan, name='detail'),
    path('tambah-pelanggan/', views.tambah_pelanggan, name='tambah_pelanggan'),
    path('pelanggan/<int:pk>/edit/', views.edit_pelanggan, name='edit_pelanggan'),
    path('resep/<int:pk>/edit/', views.edit_resep, name='edit_resep'),
]
