from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Visita
from .forms import VisitaForm

def lista_visitas(request):
    visitas = Visita.objects.all().order_by('-fecha_visita', '-hora_entrada')
    return render(request, 'SistemaRegistros/lista_visitas.html', {'visitas': visitas})

def registrar_visita(request):
    if request.method == 'POST':
        form = VisitaForm(request.POST)
        if form.is_valid():
            visita = form.save(commit=False)
            if request.user.is_authenticated:
                visita.usuario_registro = request.user
            visita.save()
            messages.success(request, '✅ Visita registrada exitosamente.')
            return redirect('lista_visitas')
        messages.error(request, '❌ Corrige los errores del formulario.')
    else:
        form = VisitaForm()
    return render(request, 'SistemaRegistros/registrar_visita.html', {'form': form})

def editar_visita(request, rut):
    visita = get_object_or_404(Visita, rut=rut)
    if request.method == 'POST':
        form = VisitaForm(request.POST, instance=visita)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Visita actualizada exitosamente.')
            return redirect('lista_visitas')
    else:
        form = VisitaForm(instance=visita)
    return render(request, 'SistemaRegistros/editar_visita.html', {'form': form, 'visita': visita})

def eliminar_visita(request, rut):
    visita = get_object_or_404(Visita, rut=rut)
    if request.method == 'POST':
        visita.delete()
        messages.success(request, '✅ Visita eliminada exitosamente.')
        return redirect('lista_visitas')
    return render(request, 'SistemaRegistros/eliminar_visita.html', {'visita': visita})
