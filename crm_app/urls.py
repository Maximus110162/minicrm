# crm_app/urls.py
from django.urls import path
from . import views  # Импортируем представления из текущего модуля

urlpatterns = [
    path('', views.complaint_list, name='complaint_list'),
    path('create/', views.complaint_create, name='complaint_create'),
    path('<int:pk>/edit/', views.complaint_edit, name='complaint_edit'),
    path('profile/', views.edit_profile, name='edit_profile'),
    path('<int:pk>/update_status/', views.complaint_update_status, name='complaint_update_status'),  # Новый маршрут,
]