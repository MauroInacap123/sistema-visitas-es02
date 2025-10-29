"""
URL configuration for proyectoVisitas project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

# Deshabilitar CSRF para todo el admin
admin.site.login = csrf_exempt(admin.site.login)
admin.site.logout = csrf_exempt(admin.site.logout)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('SistemaRegistros.urls')),
]