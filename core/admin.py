from django.contrib import admin
from django.utils.html import format_html
from .models import Perfil, Proyecto, Experiencia, Educacion, MensajeContacto, Tecnologia

# Configuración del encabezado del panel
admin.site.site_header = "Administración del Portafolio"
admin.site.index_title = "Panel de Gestión"
admin.site.site_title = "Admin Portafolio"


# --- 0. GESTIÓN DE TECNOLOGÍAS ---
@admin.register(Tecnologia)
class TecnologiaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'icono_preview', 'icono_class')
    list_filter = ('categoria',)
    search_fields = ('nombre', 'icono_class')
    ordering = ('categoria', 'nombre')

    def icono_preview(self, obj):
        if obj.icono_class:
            return format_html('<i class="{}" style="font-size: 1.2rem;"></i> <code style="margin-left: 8px;">{}</code>', obj.icono_class, obj.icono_class)
        return "—"
    icono_preview.short_description = "Ícono"


# --- 1. PERFIL PERSONAL (SINGLETON) ---
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rol', 'email', 'miniatura_foto')
    filter_horizontal = ('tecnologias_destacadas',)
    readonly_fields = ('miniatura_foto_detalle',)

    fieldsets = (
        ('Datos Personales', {
            'fields': ('nombre', 'rol', ('foto', 'miniatura_foto_detalle'), 'cv_pdf')
        }),
        ('Biografía y Enfoque', {
            'fields': ('bio_corta', 'bio_larga', 'especializacion', 'tecnologias_destacadas')
        }),
        ('Contacto y Redes Sociales', {
            'fields': (('email', 'whatsapp'), ('linkedin', 'github'))
        }),
    )

    def miniatura_foto(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="width: 40px; height: 40px; object-fit: cover; border-radius: 50%;" />', obj.foto.url)
        return "Sin foto"
    miniatura_foto.short_description = "Foto"

    def miniatura_foto_detalle(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="max-height: 150px; border-radius: 8px;" />', obj.foto.url)
        return "Sin foto cargada"
    miniatura_foto_detalle.short_description = "Vista previa"

    def has_add_permission(self, request):
        if Perfil.objects.exists():
            return False
        return True


# --- 2. PROYECTOS ---
@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'miniatura_portada', 'destacado', 'orden', 'fecha_creacion')
    list_filter = ('destacado', 'tecnologias', 'fecha_creacion')
    search_fields = ('titulo', 'subtitulo', 'descripcion')
    list_editable = ('destacado', 'orden')
    prepopulated_fields = {'slug': ('titulo',)}
    filter_horizontal = ('tecnologias',)
    readonly_fields = ('fecha_creacion', 'miniatura_portada_detalle')

    fieldsets = (
        ('Información Principal', {
            'fields': ('titulo', 'slug', 'subtitulo', 'descripcion', 'tecnologias')
        }),
        ('Multimedia y Enlaces', {
            'fields': (
                ('imagen_portada', 'miniatura_portada_detalle'),
                ('link_deploy', 'link_github', 'link_video_demo')
            )
        }),
        ('Visibilidad y Organización', {
            'fields': (('destacado', 'orden'), 'fecha_creacion')
        }),
    )

    def miniatura_portada(self, obj):
        if obj.imagen_portada:
            return format_html('<img src="{}" style="width: 60px; height: 35px; object-fit: cover; border-radius: 4px;" />', obj.imagen_portada.url)
        return "—"
    miniatura_portada.short_description = "Portada"

    def miniatura_portada_detalle(self, obj):
        if obj.imagen_portada:
            return format_html('<img src="{}" style="max-height: 180px; border-radius: 6px;" />', obj.imagen_portada.url)
        return "Sin portada"
    miniatura_portada_detalle.short_description = "Vista previa portada"


# --- 3. EXPERIENCIA LABORAL ---
@admin.register(Experiencia)
class ExperienciaAdmin(admin.ModelAdmin):
    list_display = ('puesto', 'empresa', 'fecha_inicio', 'fecha_fin', 'estado_actual')
    list_filter = ('empresa', 'tecnologias')
    search_fields = ('puesto', 'empresa', 'descripcion')
    filter_horizontal = ('tecnologias',)
    ordering = ('-fecha_inicio',)

    def estado_actual(self, obj):
        return "En curso" if obj.es_actual else "Finalizado"
    estado_actual.short_description = "Estado"


# --- 4. EDUCACIÓN ---
@admin.register(Educacion)
class EducacionAdmin(admin.ModelAdmin):
    list_display = ('titulo_obtenido', 'institucion', 'fecha_inicio', 'fecha_fin', 'estado_cursado')
    list_filter = ('institucion',)
    search_fields = ('titulo_obtenido', 'institucion', 'descripcion')
    ordering = ('-fecha_inicio',)

    def estado_cursado(self, obj):
        return "En curso" if obj.en_curso else "Completado"
    estado_cursado.short_description = "Estado"


# --- 5. MENSAJES DE CONTACTO ---
@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'asunto', 'leido', 'fecha_envio')
    list_filter = ('leido', 'fecha_envio')
    search_fields = ('nombre', 'email', 'asunto', 'mensaje')
    list_editable = ('leido',)
    readonly_fields = ('nombre', 'email', 'asunto', 'mensaje', 'fecha_envio')
    ordering = ('-fecha_envio',)
    actions = ['marcar_como_leido', 'marcar_como_no_leido']

    fieldsets = (
        ('Remitente', {
            'fields': (('nombre', 'email'), 'asunto')
        }),
        ('Contenido del Mensaje', {
            'fields': ('mensaje',)
        }),
        ('Estado y Auditoría', {
            'fields': (('leido', 'fecha_envio'),)
        }),
    )

    def has_add_permission(self, request):
        # Evita crear mensajes manualmente desde el admin
        return False

    @admin.action(description="Marcar mensajes seleccionados como leídos")
    def marcar_como_leido(self, request, queryset):
        queryset.update(leido=True)

    @admin.action(description="Marcar mensajes seleccionados como NO leídos")
    def marcar_como_no_leido(self, request, queryset):
        queryset.update(leido=False)