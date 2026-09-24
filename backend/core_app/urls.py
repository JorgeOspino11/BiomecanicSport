"""
Rutas URL para la aplicación core_app.
"""
from django.urls import path
from .views import AtletaListCreateView, AtletaDetailView

urlpatterns = [
    path('atletas/', AtletaListCreateView.as_view(), name='atleta-list-create'),
    path('atletas/<int:pk>/', AtletaDetailView.as_view(), name='atleta-detail'),
]
