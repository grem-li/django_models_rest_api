from django.urls import path
from rest_api import views

urlpatterns = [
    path('', views.index),
    path('<str:app_name>/<str:model_name>/', views.api),
    path('<str:app_name>/<str:model_name>/<int:oid>/', views.api),
]
