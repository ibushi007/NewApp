from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_csv, name='upload_csv'),
    path('list/', views.dataset_list, name='dataset_list'),
    path('dataset/<int:pk>/', views.dataset_detail, name='dataset_detail'),
    path('dataset/<int:pk>/delete/', views.dataset_delete, name="dataset_delete"),
]