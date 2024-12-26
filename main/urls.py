
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.base_operations, name='db'),
    path('gather_data/', views.gather_data, name='gather_data'),
    path('save_conversion/', views.save_conversion, name='save_conversion'),
    path('test/', views.test),
    path('report/', views.report)
]
