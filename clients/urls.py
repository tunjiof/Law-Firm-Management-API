from django.urls import path, include
from .views import ClientListCreateView, ClientDetailView
from . import views

urlpatterns = [
    path('clients/', ClientListCreateView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('clients/', views.add_client, name='add_client'),
    path('clients/', views.get_all_clients, name='get_all_clients'),
    path('clients/<int:client_id>/', views.get_client, name='get_client'),
    path('clients/<int:client_id>/', views.update_client, name='update_client'),
    path('clients/<int:client_id>/', views.delete_client, name='delete_client'),
]
