from django import forms
from django.core.exceptions import ValidationError
from .models import MensajeContacto


class FormularioContacto(forms.ModelForm):
    # Campo invisible para trampear bots (honeypot)
    # Si un bot completa este campo oculto, el formulario se descarta silenciosamente.
    website_check = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'tabindex': '-1',
            'autocomplete': 'off',
            'style': 'display:none !important;',
            'aria-hidden': 'true',
        })
    )

    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre completo',
                'autocomplete': 'name',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'tuemail@ejemplo.com',
                'autocomplete': 'email',
                'required': True,
            }),
            'asunto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Motivo del contacto o propuesta',
                'required': True,
            }),
            'mensaje': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describí tu consulta, proyecto o propuesta laboral...',
                'required': True,
            }),
        }

    def clean_website_check(self):
        """Si el campo trampa tiene contenido, es un bot."""
        honeypot = self.cleaned_data.get('website_check')
        if honeypot:
            raise ValidationError("Detección de actividad automatizada.")
        return honeypot

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if len(nombre) < 2:
            raise ValidationError("Por favor, ingresá un nombre válido.")
        return nombre

    def clean_mensaje(self):
        mensaje = self.cleaned_data.get('mensaje', '').strip()
        if len(mensaje) < 10:
            raise ValidationError("El mensaje debe contener al menos 10 caracteres.")
        return mensaje