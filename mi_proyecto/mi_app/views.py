import time
from django.shortcuts import render, get_object_or_404
from .dijkstra_graph import generar_grafo_dijkstra  # tu implementación
from .mst_generator import generar_grafo_mst
from .models import Estudiante
from .algoritmo import compatibilidad
from .grafo import Grafo, DISTANCIAS_DISTRITOS
import matplotlib
matplotlib.use('Agg')  # Importante: configurar antes de importar pyplot

distritos = [
    "Miraflores", "San Miguel", "San Isidro", "La Molina",
    "Comas", "Surco", "Los Olivos", "Magdalena"
]

# Página principal
def hola(request):
    origen = request.GET.get('origen')
    destinos = []
    mst_image = None

    if origen:
        try:
            from .mst_generator import edges, generar_grafo_mst
            
            # Filtramos destinos desde el origen
            destinos = [(v, w) for u, v, w in edges if u == origen] + \
                       [(u, w) for u, v, w in edges if v == origen]

            # Generamos la imagen del MST solo si hay un distrito seleccionado
            mst_image = generar_grafo_mst()
            
        except Exception as e:
            print(f"Error en vista hola: {e}")
            mst_image = None

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


# Ver estudiantes compatibles con grafo de Dijkstra
def ver_compatibles(request, student_id=None):
    estudiantes = Estudiante.objects.all()
    tu_estudiante = None
    resultados = []
    dijkstra_image = None
    
    # Estadísticas
    total_matches = 0
    high_compatibility = 0
    closest_time = 0

    grafo = Grafo(DISTANCIAS_DISTRITOS)

    if request.method == "POST":
        student_id = request.POST.get("student_id")
        tu_estudiante = get_object_or_404(Estudiante, student_id=student_id)
        otros = estudiantes.exclude(student_id=student_id)

        for e in otros:
            try:
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
                
            except Exception as error:
                print(f"Error procesando estudiante {e.name}: {error}")
                continue

        # Ordenar por tiempo de viaje
        resultados = sorted(resultados, key=lambda x: float('inf') if x[3] is None else x[3])

        # Calcular estadísticas
        total_matches = len(resultados)
        high_compatibility = sum(1 for _, score, _, _ in resultados if score >= 75)
        closest_time = resultados[0][3] if resultados else 0

        # Generar imagen del grafo de Dijkstra desde el distrito del estudiante
        try:
            from .dijkstra_graph import generar_grafo_dijkstra
            dijkstra_image = generar_grafo_dijkstra(tu_estudiante.district)
        except Exception as e:
            print(f"Error generando grafo Dijkstra: {e}")
            dijkstra_image = None

    return render(request, 'RoomFrom/resultados.html', {
        'tu_estudiante': tu_estudiante,
        'resultados': resultados,
        'estudiantes': estudiantes,
        'dijkstra_image': dijkstra_image,
        'total_matches': total_matches,
        'high_compatibility': high_compatibility,
        'closest_time': closest_time,
    })


def benchmark_algoritmos(request):
    resultados = []

    # Lista de algoritmos que quieres medir
    algoritmos = [
        ("Dijkstra", generar_grafo_dijkstra),
        ("Kruskal", generar_grafo_mst)
    ]

    for nombre, func in algoritmos:
        start = time.perf_counter()

        if nombre == "Dijkstra":
            func()  # usa origen por defecto "San Isidro"
        else:
            func()  # Kruskal no requiere argumentos

        end = time.perf_counter()
        tiempo = end - start

        resultados.append({
            "nombre": nombre,
            "tiempo": f"{tiempo:.6f} s",
            "bigO": "O(E log V)" if nombre == "Kruskal" else "O(V^2)"  # ejemplo BigO
        })

    return render(request, "RoomFrom/benchmark.html", {"resultados": resultados})