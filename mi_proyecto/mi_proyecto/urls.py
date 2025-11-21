from django.contrib import admin
from django.urls import path
from mi_app.views import hola, registrar_estudiante, ver_compatibles

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', hola),  # raíz apunta a la vista hola
    path('hola/', hola),
    path('registrar/', registrar_estudiante),
    path('ver_compatibles/', ver_compatibles, name='ver_compatibles'),  # <--- quitar el <str:student_id>
]
