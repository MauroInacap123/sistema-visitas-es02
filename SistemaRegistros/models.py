from django.db import models
from django.contrib.auth.models import User

class Visita(models.Model):
    ESTADO_CHOICES = [
        ('EN_CURSO', 'En curso'),
        ('FINALIZADA', 'Finalizada'),
    ]

    # Información del visitante
    rut = models.CharField(
        max_length=12,
        verbose_name='RUT'
    )
    nombre = models.CharField(max_length=100, verbose_name='Nombre completo')
    motivo_visita = models.TextField(max_length=500, verbose_name='Motivo de la visita')

    # Control de horarios
    fecha_visita = models.DateField(verbose_name='Fecha de visita')
    hora_entrada = models.TimeField(verbose_name='Hora de entrada')
    hora_salida = models.TimeField(null=True, blank=True, verbose_name='Hora de salida')

    # Estado y metadata
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='EN_CURSO',
        verbose_name='Estado de la visita'
    )
    usuario_registro = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='visitas_registradas', verbose_name='Registrado por'
    )
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        ordering = ['-fecha_visita', '-hora_entrada']
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'

    def __str__(self):
        return f"{self.nombre} ({self.rut}) - {self.fecha_visita}"
