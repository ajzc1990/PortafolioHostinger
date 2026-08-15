from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError


# --- 0. MODELO AUXILIAR: HABILIDADES Y TECNOLOGÍAS ---
class Tecnologia(models.Model):
    class Categoria(models.TextChoices):
        BACKEND = 'BACK', 'Backend'
        FRONTEND = 'FRONT', 'Frontend'
        DATABASE = 'DB', 'Base de Datos'
        DEVOPS_TOOLS = 'TOOLS', 'DevOps & Herramientas'
        OTHER = 'OTHER', 'Otros'

    nombre = models.CharField(max_length=50, unique=True)
    icono_class = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Clase para FontAwesome/Devicon (ej: 'devicon-django-plain', 'fa-brands fa-python')"
    )
    categoria = models.CharField(
        max_length=10, 
        choices=Categoria.choices, 
        default=Categoria.BACKEND
    )

    class Meta:
        verbose_name = "Tecnología"
        verbose_name_plural = "Tecnologías"
        ordering = ['categoria', 'nombre']

    def __str__(self):
        return self.nombre


# --- 1. SECCIÓN SOBRE MÍ ---
class Perfil(models.Model):
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=120, help_text="Ej: Ingeniero en Sistemas de Información | Full Stack Developer")
    foto = models.ImageField(upload_to='perfil/')
    bio_corta = models.TextField(verbose_name="Introducción / Headline", help_text="1 o 2 oraciones de impacto para el hero section.")
    bio_larga = models.TextField(verbose_name="Acerca de mí")
    especializacion = models.TextField(blank=True, help_text="Áreas de foco o propuesta de valor técnica.")
    tecnologias_destacadas = models.ManyToManyField(Tecnologia, blank=True, related_name='perfiles')
    cv_pdf = models.FileField(upload_to='cv/', blank=True, null=True)
    
    # Redes y Contacto Directo
    whatsapp = models.CharField(max_length=30, blank=True, help_text="Formato internacional, ej: +549381XXXXXXX")
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    email = models.EmailField()

    class Meta:
        verbose_name = "Perfil Personal"
        verbose_name_plural = "Perfil Personal"

    def clean(self):
        # Garantiza que no se cree más de un perfil
        if not self.pk and Perfil.objects.exists():
            raise ValidationError("Solo puede existir un único perfil.")

    def __str__(self):
        return f"Perfil de {self.nombre}"


# --- 2. SECCIÓN PORTAFOLIO ---
class Proyecto(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True, help_text="Se autogenera si se deja vacío")
    subtitulo = models.CharField(max_length=250, help_text="Resumen conciso del objetivo o alcance del sistema")
    descripcion = models.TextField(help_text="Detalle del problema, solución técnica y arquitectura implementada")
    tecnologias = models.ManyToManyField(Tecnologia, related_name='proyectos')
    imagen_portada = models.ImageField(upload_to='proyectos/portadas/')
    link_deploy = models.URLField(blank=True, null=True, verbose_name="Demo en vivo")
    link_github = models.URLField(blank=True, null=True, verbose_name="Repositorio GitHub")
    link_video_demo = models.URLField(blank=True, null=True, verbose_name="Video Demo / Loom / YouTube")
    destacado = models.BooleanField(default=False, help_text="Marcar para fijar en los primeros lugares de la home")
    orden = models.PositiveIntegerField(default=0, help_text="Orden de visualización (menor número = primero)")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['orden', '-fecha_creacion']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo


# --- 3. SECCIÓN CURRÍCULUM (Experiencia y Educación) ---
class Experiencia(models.Model):
    empresa = models.CharField(max_length=200)
    puesto = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=150, blank=True, help_text="Ej: Tucumán, Argentina / Remoto")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True, help_text="Dejar en blanco si continúa en curso")
    descripcion = models.TextField(help_text="Logros clave, responsabilidades y stack utilizado")
    tecnologias = models.ManyToManyField(Tecnologia, blank=True, related_name='experiencias')

    class Meta:
        verbose_name = "Experiencia Laboral"
        verbose_name_plural = "Experiencias Laborales"
        ordering = ['-fecha_inicio']

    @property
    def es_actual(self):
        return self.fecha_fin is None

    def __str__(self):
        return f"{self.puesto} en {self.empresa}"


class Educacion(models.Model):
    institucion = models.CharField(max_length=200)
    titulo_obtenido = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True, help_text="Dejar en blanco si continúa en curso")
    descripcion = models.TextField(blank=True, help_text="Detalles relevantes, promedio, cursos aprobados o tesis")

    class Meta:
        verbose_name = "Educación"
        verbose_name_plural = "Educación"
        ordering = ['-fecha_inicio']

    @property
    def en_curso(self):
        return self.fecha_fin is None

    def __str__(self):
        return f"{self.titulo_obtenido} - {self.institucion}"


# --- 4. SECCIÓN CONTACTO ---
class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    asunto = models.CharField(max_length=200)
    mensaje = models.TextField()
    leido = models.BooleanField(default=False)
    fecha_envio = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mensaje de Contacto"
        verbose_name_plural = "Mensajes de Contacto"
        ordering = ['-fecha_envio']

    def __str__(self):
        return f"[{'Leído' if self.leido else 'Nuevo'}] {self.nombre} - {self.asunto}"