from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_visitas, name="lista_visitas"),
    path("visita/registrar/", views.registrar_visita, name="registrar_visita"),
    path("visita/editar/<str:rut>/", views.editar_visita, name="editar_visita"),
    path("visita/eliminar/<str:rut>/", views.eliminar_visita, name="eliminar_visita"),
]