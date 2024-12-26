
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('csrf-token/', views.provide_token),
    path('api/', include('main.urls')),
    path('', views.homepage, name='home')    
]
