from django.shortcuts import render, get_object_or_404
from .models import Estudiante
from .algoritmo import compatibilidad
from mi_app.graph_utils import minutos_entre_distritos
from mi_app.utils import distritos  # tu diccionario de distritos


# Vista que muestra la página principal
def hola(request):
    return render(request, "RoomFrom/index.html")


def registrar_estudiante(request):
    mensaje = ""
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        monthly_budget = request.POST.get("monthly_budget")
        district = request.POST.get("district")

        estudiante = Estudiante(
            name=name,
            age=int(age),
            gender=gender,
            monthly_budget=float(monthly_budget),
            district=district
        )
        estudiante.save()
        mensaje = f"Estudiante {name} registrado correctamente!"

    return render(request, "RoomFrom/form.html", {"mensaje": mensaje})


def ver_compatibles(request, student_id=None):
    estudiantes = Estudiante.objects.all()
    tu_estudiante = None
    resultados = []

    if request.method == "POST":
        student_id = request.POST.get("student_id")
        tu_estudiante = get_object_or_404(Estudiante, student_id=student_id)
        otros = estudiantes.exclude(student_id=student_id)

        for e in otros:
            # 1) calcular minutos entre distritos (Dijkstra ya encapsulado)
            minutos = minutos_entre_distritos(distritos, tu_estudiante.district, e.district)

            # 2) calcular compatibilidad (no modificamos la fórmula)
            score = compatibilidad(tu_estudiante, e)

            # 3) asignar color_class para la barra (mantener la lógica visual)
            if score > 0.8:
                color_class = "verde"
            elif score > 0.5:
                color_class = "amarillo"
            else:
                color_class = "rojo"

            # 4) añadir tuple: (estudiante, score_percent, color_class, minutos)
            resultados.append((e, score*100, color_class, round(minutos, 1)))

        # 5) ordenar resultados por minutos asc (sitúa inf/no disponible al final)
        resultados = sorted(resultados, key=lambda x: (float('inf') if x[3] is None else x[3]))

    return render(request, 'RoomFrom/resultados.html', {
        'tu_estudiante': tu_estudiante,
        'resultados': resultados,
        'estudiantes': estudiantes
    })
