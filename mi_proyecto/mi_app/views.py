from django.shortcuts import render, get_object_or_404
from .models import Estudiante
from .algoritmo import compatibilidad
from .mst_generator import generar_grafo_mst
from .mst_generator import edges
from .grafo import Grafo, DISTANCIAS_DISTRITOS

distritos = [
    "Miraflores", "San Miguel", "San Isidro", "La Molina",
    "Comas", "Surco", "Los Olivos", "Magdalena"
]

# Página principal
def hola(request):
    origen = request.GET.get('origen')  # viene del select del MST
    destinos = []
    mst_image = None  # inicialmente no hay imagen

    if origen:
        # Filtramos destinos desde el origen
        destinos = [(v, w) for u, v, w in edges if u == origen] + \
                   [(u, w) for u, v, w in edges if v == origen]

        # Generamos la imagen del MST solo si hay un distrito seleccionado
        mst_image = generar_grafo_mst()

    return render(request, "RoomFrom/index.html", {
        "distritos": distritos,
        "origen": origen,
        "destinos": destinos,
        "mst_image": mst_image
    })

# Registrar estudiante
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

# Ver estudiantes compatibles
def ver_compatibles(request, student_id=None):
    estudiantes = Estudiante.objects.all()
    tu_estudiante = None
    resultados = []
    mst = None

    grafo = Grafo(DISTANCIAS_DISTRITOS)

    if request.method == "POST":
        student_id = request.POST.get("student_id")
        tu_estudiante = get_object_or_404(Estudiante, student_id=student_id)
        otros = estudiantes.exclude(student_id=student_id)

        for e in otros:
            # 1) Minutos usando Dijkstra
            minutos = grafo.dijkstra(tu_estudiante.district, e.district)

            # 2) Compatibilidad
            score = compatibilidad(tu_estudiante, e)

            # 3) Color de barra según score
            if score > 0.75:
                color_class = "verde"
            elif score > 0.5:
                color_class = "amarillo"
            else:
                color_class = "rojo"

            resultados.append((e, score*100, color_class, round(minutos, 1)))

        # Ordenar por tiempo de viaje
        resultados = sorted(resultados, key=lambda x: float('inf') if x[3] is None else x[3])

        # MST usando Kruskal
        mst = grafo.kruskal()

    return render(request, 'RoomFrom/resultados.html', {
        'tu_estudiante': tu_estudiante,
        'resultados': resultados,
        'estudiantes': estudiantes,
        'mst': mst
    })
