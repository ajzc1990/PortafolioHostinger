import os
import django
from datetime import date

# Configuración del entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Perfil, Proyecto, Experiencia, Educacion

def seed_db():
    print("Iniciando carga de datos de prueba...")

    # 1. Borrar datos existentes (opcional, cuidado con esto)
    # Proyecto.objects.all().delete()
    # Experiencia.objects.all().delete()
    # Educacion.objects.all().delete()
    # Perfil.objects.all().delete()

    # 2. Crear Perfil
    perfil, created = Perfil.objects.get_or_create(
        nombre="Agustín Zelaya Cossio",
        defaults={
            'rol': "Ingeniero en Sistemas / Full Stack Developer",
            'bio_corta': "Analista en Sistemas especializado en desarrollo de soluciones SaaS y automatización de procesos.",
            'bio_larga': "Soy estudiante de Ingeniería en Sistemas en la UTN FRT. Me apasiona la tecnología aplicada al agro y la eficiencia de procesos mediante software.",
            'especializacion': "Backend con Python/Django, SQL Server y Arquitectura de Sistemas.",
            'tecnologias_skills': "Python, Django, SQL Server, JavaScript, Git, Bootstrap",
            'whatsapp': "543810000000",
            'linkedin': "https://linkedin.com/in/agustinzelaya",
            'github': "https://github.com/agustinzelaya",
            'email': "contacto@agustinzelaya.com",
        }
    )

    # 3. Crear Proyectos
    proyectos = [
        {
            'titulo': "Retail Guardian",
            'subtitulo': "SaaS de Gestión Financiera",
            'descripcion': "Aplicación para pequeños comercios que permite monitorear finanzas, ventas e inventario en tiempo real.",
            'tecnologias': "Django, SQLite, Bootstrap",
        },
        {
            'titulo': "OmniFlow",
            'subtitulo': "Automatización Omnicanal",
            'descripcion': "Sistema de mensajería unificada y automatización de flujos de trabajo para atención al cliente.",
            'tecnologias': "Python, Django, API Rest",
        },
        {
            'titulo': "Fichaje Web",
            'subtitulo': "Control de Asistencia",
            'descripcion': "Plataforma para el registro de entrada y salida de empleados con geolocalización.",
            'tecnologias': "Django, JavaScript, PostgreSQL",
        },
        {
            'titulo': "Narraciones Interactivas",
            'subtitulo': "Proyecto UTN FRT",
            'descripcion': "Aplicación web desarrollada para la Facultad Regional Tucumán que permite crear historias interactivas.",
            'tecnologias': "Django, SQL Server, CSS3",
        }
    ]

    for p in proyectos:
        Proyecto.objects.get_or_create(titulo=p['titulo'], defaults=p)

    # 4. Crear Educación
    Educacion.objects.get_or_create(
        titulo_obtenido="Ingeniería en Sistemas de Información",
        defaults={
            'institucion': "UTN - Facultad Regional Tucumán",
            'fecha_inicio': date(2020, 3, 1),
        }
    )

    # 5. Crear Experiencia
    Experiencia.objects.get_or_create(
        puesto="Analista en Sistemas de Información",
        defaults={
            'empresa': "Freelance",
            'fecha_inicio': date(2024, 1, 1),
            'descripcion': "Desarrollo de aplicaciones a medida y consultoría técnica.",
        }
    )

    print("Carga completada con éxito. ¡Ya podés revisar tu portafolio!")

if __name__ == '__main__':
    seed_db()