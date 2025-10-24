from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse
import csv
from datetime import date
from .models import Visita

@admin.action(description="✅ Marcar como finalizada")
def marcar_salida(modeladmin, request, queryset):
    from datetime import datetime
    updated = 0
    for visita in queryset.filter(estado='EN_CURSO'):
        visita.hora_salida = datetime.now().time()
        visita.estado = 'FINALIZADA'
        visita.save()
        updated += 1
    
    if updated > 0:
        modeladmin.message_user(request, f"✅ {updated} visita(s) marcada(s) como finalizada(s).")
    else:
        modeladmin.message_user(request, "ℹ️ No hay visitas en curso.", level='warning')

@admin.action(description="📊 Exportar a CSV")
def exportar_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="visitas_{date.today()}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['RUT', 'Nombre', 'Motivo', 'Fecha', 'Hora Entrada', 'Hora Salida', 'Estado'])
    
    for visita in queryset:
        writer.writerow([
            visita.rut,
            visita.nombre,
            visita.motivo_visita,
            visita.fecha_visita,
            visita.hora_entrada,
            visita.hora_salida if visita.hora_salida else 'En curso',
            visita.get_estado_display()
        ])
    
    return response

@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'fecha_visita', 'hora_entrada', 'hora_salida', 'estado_badge', 'usuario_registro')
    list_filter = ('estado', 'fecha_visita', 'usuario_registro')  # Agregado filtro por usuario_registro
    search_fields = ('rut', 'nombre', 'motivo_visita')
    date_hierarchy = 'fecha_visita'
    readonly_fields = ('fecha_registro', 'usuario_registro')
    list_per_page = 25
    ordering = ('-fecha_visita', '-hora_entrada')
    actions = [marcar_salida, exportar_csv]
    
    fieldsets = (
        ('📋 Información del Visitante', {
            'fields': ('rut', 'nombre', 'motivo_visita')
        }),
        ('⏰ Control de Horarios', {
            'fields': (('fecha_visita', 'estado'), ('hora_entrada', 'hora_salida'))
        }),
        ('ℹ️ Información del Sistema', {
            'fields': ('usuario_registro', 'fecha_registro'),
            'classes': ('collapse',)
        }),
    )
    
    @admin.display(description='Estado', ordering='estado')
    def estado_badge(self, obj):
        if obj.estado == 'EN_CURSO':
            color = '#FFA500'
            texto = '🟠 En Curso'
        else:
            color = '#28A745'
            texto = '🟢 Finalizada'
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-weight: bold; font-size: 11px;">{}</span>',
            color, texto
        )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.usuario_registro = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('usuario_registro')

admin.site.site_header = "🏢 Panel de Administración - Sistema de Visitas"
admin.site.site_title = "Admin Sistema Visitas"
admin.site.index_title = "📊 Gestión de Visitas de la Empresa"
