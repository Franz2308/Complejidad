from django.contrib import admin
from django.urls import path
from mi_app.views import hola, registrar_estudiante, ver_compatibles

urlpatterns = [
    path('admin/', admin.site.urls),

    # Página principal
    path('', hola, name='index'),

    # Vista alternativa (opcional)
    path('hola/', hola),

    # Registrar estudiantes
    path('registrar/', registrar_estudiante, name='registrar_estudiante'),

    # Compatibilidad de estudiantes
    path('ver_compatibles/', ver_compatibles, name='ver_compatibles'),
]
