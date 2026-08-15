from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('portafolio/', views.portafolio, name='portafolio'),
    path('portafolio/<slug:slug>/', views.detalle_proyecto, name='detalle_proyecto'),
    path('sobre-mi/', views.sobre_mi, name='sobre_mi'),
    path('curriculum/', views.curriculum, name='curriculum'),
    path('contacto/', views.contacto, name='contacto'),
]