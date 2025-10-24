from django import forms
from .models import Visita

class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['rut', 'nombre', 'motivo_visita', 'fecha_visita', 'hora_entrada', 'hora_salida', 'estado']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-9'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}),
            'motivo_visita': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_visita': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_entrada': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_salida': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
