from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Proyecto, Experiencia, Educacion, Tecnologia
from .forms import FormularioContacto


# 🏠 1. VISTA HOME
def home(request):
    proyectos_destacados = (
        Proyecto.objects.filter(destacado=True)
        .prefetch_related('tecnologias')[:4]
    )
    return render(request, 'core/home.html', {
        'proyectos_destacados': proyectos_destacados
    })


# 💼 2. VISTA PORTAFOLIO (Con filtrado opcional por tecnología)
def portafolio(request):
    tech_filter = request.GET.get('tech')
    proyectos = Proyecto.objects.prefetch_related('tecnologias').all()
    
    if tech_filter:
        proyectos = proyectos.filter(tecnologias__nombre__iexact=tech_filter)
        
    tecnologias = Tecnologia.objects.all()
    
    return render(request, 'core/portafolio.html', {
        'proyectos': proyectos,
        'tecnologias': tecnologias,
        'tech_actual': tech_filter
    })


# 📄 2.1 VISTA DETALLE DE PROYECTO (Por slug o pk)
def detalle_proyecto(request, slug):
    proyecto = get_object_or_404(
        Proyecto.objects.prefetch_related('tecnologias'), 
        slug=slug
    )
    proyectos_relacionados = (
        Proyecto.objects.filter(tecnologias__in=proyecto.tecnologias.all())
        .exclude(id=proyecto.id)
        .distinct()[:3]
    )
    return render(request, 'core/detalle.html', {
        'proyecto': proyecto,
        'proyectos_relacionados': proyectos_relacionados
    })


# 👤 3. VISTA SOBRE MÍ
def sobre_mi(request):
    return render(request, 'core/sobre_mi.html')


# 📚 4. VISTA CURRICULUM (Timeline)
def curriculum(request):
    experiencias = Experiencia.objects.prefetch_related('tecnologias').all()
    educacion = Educacion.objects.all()
    
    return render(request, 'core/curriculum.html', {
        'experiencias': experiencias,
        'educacion': educacion
    })


# 📩 5. VISTA CONTACTO
def contacto(request):
    if request.method == 'POST':
        form = FormularioContacto(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Gracias! Tu mensaje ha sido enviado con éxito.')
            return redirect('contacto')
    else:
        form = FormularioContacto()
        
    return render(request, 'core/contacto.html', {
        'form': form
    })