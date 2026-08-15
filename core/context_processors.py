from .models import Perfil

def perfil_global(request):
    """Hace que la variable 'perfil' esté disponible en cualquier template."""
    return {
        'perfil': Perfil.objects.prefetch_related('tecnologias_destacadas').first()
    }